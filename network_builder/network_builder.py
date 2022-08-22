#!/usr/bin/env python
import logging
import os
from pprint import pprint

from config import Config as config
from filters import *
from jinja2 import DebugUndefined, Environment, FileSystemLoader, Undefined
from jinja2.meta import find_undeclared_variables
from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.tasks.files import write_file


class UndefinedVars(Undefined):

    """
    Handler for undefined Vars
    """

    def _fail_with_undefined_error(self, *args, **kwargs):
        # logging.exception("JINJA2: something was undefined!")
        print(args)
        print(kwargs)
        raise Exception(f"Undefined Variables")


def identify_device_template(task: Task, templates: list) -> dict:
    """Tries to find correct template by finding matching device_type and device_role"""

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
    """Takes a template as input and loads template yml file in order
    to put together all jinja2 snippet pieces together into single string"""

    try:

        jinja_string = ""

        # Add all jinja2 snippets to config
        for filename in template["config"]:
            with open(f"{config.SNIPPETS_DIR}/{filename}", "r") as f:
                jinja_string += "!==========================\n"
                jinja_string += f"!{filename}\n"
                jinja_string += f.read() + "\n"
                f.close()

        return jinja_string

    except Exception as e:
        raise Exception(f"Unable to load template {template['template_name']} - {e}")


def render_config(task: Task, render_string: str, render_vars: dict) -> str:
    """Takes a full jinja2 string as input (template) along with render_vars
    Outputs rendered configuration."""

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
    """cleanup configs that weren't used."""
    deleted = []
    for file in os.listdir(config.CONFIGS_DIR):
        if file.endswith(config.CONFIG_FILE_SUFFIX):
            host = file[: -(len(config.CONFIG_FILE_SUFFIX))]
            if host not in config_files["untouched"] or config_files["updated"]:
                deleted.append(file)

    return deleted


def generate_configs(task: Task) -> Result:
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
    # print(template["config"])
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

    task.run(
        name="Write Config Files",
        task=write_file,
        filename=f"{config.CONFIGS_DIR}/{task.host}{config.CONFIG_FILE_SUFFIX}",
        content=task.host["config"],
    )

    return Result(
        host=task.host, result=f"Successfully generated Configs, amount of changes: 0"
    )


def deploy_network(task: Task) -> Result:

    result = task.run(
        name=f"Deploying config for: {task.host.name}!",
        task=napalm_configure,
        filename=f"{config.CONFIGS_DIR}/{task.host}{config.CONFIG_FILE_SUFFIX}",
        dry_run=True,
        replace=True,
    )


def main():

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

    result = nr.run(name="Generate Configurations", task=generate_configs)

    print_result(result, severity_level=logging.INFO, vars=["result"])

    nr.inventory.defaults.username = config.SSH_USERNAME
    nr.inventory.defaults.password = config.SSH_PASSWORD

    # result = nr.run(task=netmiko_send_command, command_string="show arp")
    result = nr.run(name="Deploying Network", task=deploy_network)
    print_result(result)

    """
    config_files["deleted"] = cleanup_configs(config_files)
    for file in config_files["deleted"]:
        os.remove(f"{config.CONFIGS_DIR}/{file}")

    print(config_files)
    """


if __name__ == "__main__":
    main()
