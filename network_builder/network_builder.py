#!/usr/bin/env python
from helpers import load_yaml_file
from filters import *
import glob
import logging
from jinja2 import (
    Environment,
    FileSystemLoader,
    Undefined,
    meta,
    PackageLoader,
    Template,
    DebugUndefined,
)
from jinja2.meta import find_undeclared_variables
from config import Config as config
from pprint import pprint
import pdb


class UndefinedVars(Undefined):

    """
    Handler for undefined Vars
    """

    def _fail_with_undefined_error(self, *args, **kwargs):
        # logging.exception("JINJA2: something was undefined!")
        print(args)
        print(kwargs)
        raise NTMException(f"Undefined Variables")


class NTMException(Exception):
    """base exception for all NetworkTemplateManager exceptions"""

    def __init__(self, msg=""):
        self.logger = logging.getLogger(__name__)
        self.msg = msg
        self.logger.error(self.msg, exc_info=True)

    def __str__(self):
        return self.msg


def load_templates(short=False):
    """Returns all templates
    Short keyword return a list with all the name of all templates"""

    templates_file = load_yaml_file(config.TEMPLATES_FILE)

    if short:
        templates = list(templates_file.keys())
    else:
        templates = []
        for tmpl in templates_file:
            templates.append(tmpl)

    return templates_file


def load_vars(host: dict) -> dict:

    """
    Loads all local vars in the following order:
    1. global_vars
    3. host_vars
    """

    vars = {}
    vars.update(load_yaml_file(config.GROUP_VARS))
    vars.update(host)
    # vars.update(load_yaml_file(f"{config.VARS_DIR}/{LocalVarFiles.VARS_SECRET}")) os.env for secret vars

    return vars


def identify_device_template(templates: list, device: dict) -> dict:
    """Tries to find correct template by finding matching device_type and device_role
    on the device in netbox and returns correct template"""

    for template in templates:
        # pdb.set_trace()
        if (
            device["device_role"] in template["device_roles"]
            and device["device_type"] in template["device_types"]
        ):
            return template

    raise NTMException(
        f"No template found for: \ndevice_role: {device['device_role']} \ndevice_type: {device['device_type']}"
    )


def load_template(template: dict) -> str:
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
        raise NTMException(f"Unable to load template {template['template_name']} - {e}")


def write_config_file(hostname: str, host_config: str) -> bool:

    with open(f"{config.CONFIGS_DIR}/{hostname}.conf", "w") as f:
        f.write(host_config)
        f.close()

    return True


def render_config(template: str, render_vars: dict) -> str:
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
        j2_tmpl = env.from_string(template)
        host_config = j2_tmpl.render(render_vars)

    except:

        # Code for testing listing specific vars that were missing.
        render_verification = env.parse(host_config)
        undefined = find_undeclared_variables(render_verification)
        if undefined:
            raise NTMException(f"Error Rendering Config, Undefined Vars: {undefined!r}")
        else:
            return host_config

    return host_config


if __name__ == "__main__":
    print("hello")
    inventory = load_yaml_file(config.INVENTORY)
    # pprint(inventory)

    templates = load_templates()
    pprint(templates)

    for site, hosts in inventory.items():

        for host in hosts:

            # Find template to use for host:
            template = identify_device_template(templates, host)

            # Loads all variables into a single dictionary
            render_vars = load_vars(host)
            pprint(render_vars)

            # Load all "snippets" from config section of template
            # And return a single jinja2 string ready to be rendered
            print(template["config"])
            template_string = load_template(template)

            # Render config by combining variables and jinja2 string
            host_config = render_config(template_string, render_vars)

            # Print config
            print(host_config)

            # Write Config to File
            write_config_file(host["hostname"], host_config)

    # for site in inventory:
    #    for
