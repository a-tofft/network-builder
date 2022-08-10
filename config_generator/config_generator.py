#!/usr/bin/env python
from helpers import load_yaml_file
from filters import *
import glob 
import logging
from jinja2 import Environment, FileSystemLoader, Undefined, meta, PackageLoader, Template, DebugUndefined
from jinja2.meta import find_undeclared_variables
from config import Config as config
from pprint import pprint

class NTMException(Exception):
    """ base exception for all NetworkTemplateManager exceptions """
    def __init__(self, msg=''):
        self.logger = logging.getLogger(__name__)
        self.msg = msg
        self.logger.error(self.msg, exc_info=True)

    def __str__(self):
        return self.msg


def load_templates(short=False):
    """ Returns all templates
    Short keyword return a list with all the name of all templates """
    
    templates_file = load_yaml_file(config.TEMPLATES_FILE)

    if short:
        templates = list(templates_file.keys())
    else:
        templates = []
        for tmpl in templates_file.items():
            templates.append(tmpl)

    return templates



def get_snippet(snippet_name):
    """ Returns a single, unrendered snippet """ 

    try:

        files = glob.glob(config.SNIPPETS_DIR + f"/**/{snippet_name}", recursive = True)
        if len(files) > 1:
            raise NTMException(f"Found more than one snippet matchning: {snippet_name}")
        elif len(files) == 0:
            raise NTMException(f"No snippet found with name: {snippet_name}")

        with open(files[0], "r") as f:
            snippet = f.read()

        return snippet

    except Exception as e:
        raise NTMException(f"Error getting snippet - {e.args}")



def load_local_vars(default_vars):

    """
    Loads all local vars in the following order: 
    1. global_vars 
    3. host_vars 
    """

    vars = { "management": {}}
    vars.update(load_yaml_file(f"{config.VARS_DIR}/{LocalVarFiles.VARS_GLOBAL}"))
    vars.update(load_yaml_file(f"{config.VARS_DIR}/{LocalVarFiles.VARS_SECRET}"))

    return vars


def render_device(template, host_vars):
    """ Renders configuration for a single device """

    # Determine the template to use 
    if template_name:
        self.template_name = template_name
    else: 
        self.template_name = self.identify_device_template(object_id, TemplateTypes.DEVICES)

    # Collect all template details
    template = self.load_template(self.template_name, tp_type=TemplateTypes.DEVICES)

    # Assemble all variables to be used for rendering
    local_vars = self.load_local_vars(default_vars)
    render_vars = self.load_netbox_vars(object_id, local_vars)
    render_vars.update(override_vars)

    # Render Configuration and return it
    configuration = self.render_config(template["main"], render_vars)
    return configuration 


def render_config(template, render_vars):
    """ Takes a full jinja2 string as input (template) along with render_vars 
    Outputs rendered configuration. """

    
    # Set parameters for rendering
    env = Environment(loader=FileSystemLoader("./"), 
                    trim_blocks=True, 
                    lstrip_blocks=True, 
                    undefined=UndefinedVars) # undefined=DebugUndefined UndefinedVars

    # Add all filter functions
    for func_name, func in FILTERS.items():
        env.filters[func_name] = func

    # Render Config
    j2_tmpl = env.from_string(template)
    config = j2_tmpl.render(render_vars)

    '''
    Code for testing listing specific vars that were missing.
    print(config)
    render_verification = env.parse(config)
    undefined = find_undeclared_variables(render_verification)
    if undefined:
        raise NTMException(f'Error Rendering Config, Undefined Vars: {undefined!r}')
    else:
        return config 
    '''

    return config





if __name__ == "__main__":
    print("hello")
    inventory = load_yaml_file(config.INVENTORY)
    pprint(inventory)
    
    templates = load_templates()
    pprint(templates)
    
    #for site in inventory:
    #    for 