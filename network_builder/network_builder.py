#!/usr/bin/env python
import argparse
import logging
import os
import pdb
import sys

from config import Config as config
from filters import *
from jinja2 import DebugUndefined, Environment, FileSystemLoader, Undefined
from jinja2.meta import find_undeclared_variables
from napalm.base.exceptions import ConnectionException
from nornir import InitNornir
from nornir.core.exceptions import NornirSubTaskError
from nornir.core.task import Result, Task
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.tasks.files import write_file


def identify_device_template(task: Task, templates: list) -> dict:
    """
    Tries to find correct template for a device by matching the role and type
    of the device with a template of the same.
    :param templates: List of all templates
    :return: The template that was found as a dictionary
    """

    for template in templates:
        if (
            task.host["role"] in template["device_roles"]
            and task.host["type"] in template["device_types"]
        ):
            return template

    raise Exception(
        f"No template found for: \ndevice_role: {device['device_role']} \ndevice_type: {device['device_type']}"
    )


def load_template(task: Task, template: dict) -> str:
    """
    Takes a template as input and loads all "snippets" from config section of template.
    Returns a single jinja2 string ready to be rendered.
    :param template: Template to render
    :return: A jinja2 string ready to be rendered
    """

    try:
        # Sets character for comments.
        # Defaults to "config.COMMENT_DEFAULT" if no match is found.
        comment_char = config.COMMENT_CHARS.get(
            task.host.platform, config.COMMENT_DEFAULT
        )

        jinja_string = ""

        # Add all jinja2 snippets to config
        for filename in template["config"]:
            with open(f"{config.SNIPPETS_DIR}/{filename}", "r") as f:
                jinja_string += f"{comment_char}==========================\n"
                jinja_string += f"{comment_char}{filename}\n"
                jinja_string += f.read() + "\n"
                f.close()

        return jinja_string

    except Exception as e:
        raise Exception(f"Unable to load template {template['template_name']} - {e}")


def render_config(task: Task, render_string: str, render_vars: dict) -> str:
    """
    Takes a jinja2 string as input (template) along with variables and renders
    configuration.
    :param render_string: Jinja2 string to render
    :param render_vars: Variables to use during rendering
    :return: A string with rendered config
    """

    try:

        # Set parameters for rendering
        env = Environment(
            loader=FileSystemLoader("./"),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=DebugUndefined,
        )  # undefined=DebugUndefined UndefinedVars

        # Add all filter functions
        for func_name, func in FILTERS.items():
            env.filters[func_name] = func

        # Render Config
        j2_tmpl = env.from_string(render_string)
        host_config = j2_tmpl.render(render_vars)
        return host_config

    except:

        # Code for testing listing specific vars that were missing.
        render_verification = env.parse(host_config)
        undefined = find_undeclared_variables(render_verification)
        if undefined:
            raise Exception(f"Error Rendering Config, Undefined Vars: {undefined!r}")
        else:
            return host_config


def cleanup_configs(config_files: dict) -> list:
    """
    Removes all network configuration files that were not listed
    in the nornir inventory.
    :param render_vars: Variables to use during rendering
    :return: A list of all deleted files
    """

    deleted = []
    for file in os.listdir(config.CONFIGS_DIR):
        if file.endswith(config.CONFIG_FILE_SUFFIX):
            host = file[: -(len(config.CONFIG_FILE_SUFFIX))]
            if host not in config_files["untouched"] or config_files["updated"]:
                deleted.append(file)

    return deleted


def generate_configs(task: Task) -> Result:
    """
    Takes a Nornir task object as input and tries to generate configuration
    for the specified host.
    :Generates: A configuration file for the host
    :param task: A Nornir Task object
    :return: A Nornir Result object
    """

    templates = task.run(
        severity_level=logging.DEBUG,
        name="Load Templates",
        task=load_yaml,
        file=config.TEMPLATES_FILE,
    )
    task.host["render_vars"] = dict(task.host.items())
    task.host["render_vars"]["hostname"] = task.host.name

    # Identifies correct template and sets template variable
    template = task.run(
        name="Identify Template",
        task=identify_device_template,
        templates=templates.result,
    )
    task.host["template"] = template.result

    # Load all "snippets" from config section of template
    # And return a single jinja2 string ready to be rendered
    render_string = task.run(
        severity_level=logging.DEBUG,
        name="Load Template",
        task=load_template,
        template=task.host["template"],
    )
    task.host["render_string"] = render_string.result

    # Render config for host
    host_config = task.run(
        name="Render Jinja2 Configuration",
        task=render_config,
        render_string=task.host["render_string"],
        render_vars=task.host["render_vars"],
    )
    task.host["config"] = host_config.result

    # Write config to file
    changed = task.run(
        name="Write Config Files",
        task=write_file,
        filename=f"{config.CONFIGS_DIR}/{task.host}{config.CONFIG_FILE_SUFFIX}",
        content=task.host["config"],
    )

    return Result(
        host=task.host,
        custom_result=f"Successfully generated Configs, Changed Config: {changed.result}",
    )


def deploy_network(task: Task, dry_run=True) -> Result:
    """
    Takes a Nornir task object as input and tries to Deploy Configuration to Network
    Using Napalm with replace function.
    :Generates: Pushes configuration to host
    :param task: A Nornir Task object
    :return: A Nornir Result object with changes made to configuration.
    """

    #
    try:
        result = task.run(
            name=f"Deploying config for: {task.host.name}!",
            task=napalm_configure,
            filename=f"{config.CONFIGS_DIR}/{task.host}{config.CONFIG_FILE_SUFFIX}",
            dry_run=dry_run,
            replace=True,
        )

        message = f"Deployed config for: {task.host.name}, dry: {dry_run}"

    # "Returns:
    # changed (bool): whether the task is changing the system or not
    # diff (string): change in the system
    except NornirSubTaskError as e:
        if isinstance(e.result.exception, ConnectionException):
            error_message = e.result.exception
        else:
            error_message = e.result.exception

        message = f"Error deploying config for: {task.host.name} - {error_message}"

    return Result(
        host=task.host,
        custom_result=message,
    )


def main():
    """
    Main Function for Generating & Deploying Network Configs
    """

    nr = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": config.NR_HOST_FILE,
                "group_file": config.NR_GROUP_FILE,
                "defaults_file": config.NR_DEFAULTS_FILE,
            },
        }
    )

    # Set username/password for all hosts
    nr.inventory.defaults.username = config.SSH_USERNAME
    nr.inventory.defaults.password = config.SSH_PASSWORD

    # Generate Configs & Display Results
    if args.build_config:
        result = nr.run(name="Generate Configurations", task=generate_configs)
        print_result(result, severity_level=logging.INFO, vars=["custom_result"])

        if result.failed:
            sys.exit(1)

    # Deploy Configs to Network & Display Results
    if args.deploy:
        result = nr.run(
            name="Deploying Network", task=deploy_network, dry_run=args.dry_run
        )
        print_result(result, severity_level=logging.INFO, vars=["custom_result"])

        if result.failed:
            sys.exit(1)


if __name__ == "__main__":

    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--build_config",
        dest="build_config",
        action="store_true",
        help="Generate configs for all devices in inventory",
    )
    parser.add_argument(
        "--dry_run",
        dest="dry_run",
        action="store_true",
        help="Display potential changes but don't deploy",
    )
    parser.add_argument(
        "--deploy",
        dest="deploy",
        action="store_true",
        help="Try to push changes using napalm to devices",
    )
    parser.set_defaults(dry_run=False, generate_config=False, deploy=False)
    args = parser.parse_args()

    # Main Function
    main()
