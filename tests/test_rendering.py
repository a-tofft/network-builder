#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(".")
from network_builder.network_builder import *
from network_builder.config import Config as config


class TestTemplates(unittest.TestCase):
    def test_1_device_templates_short(self):
        """Try to get all template keys"""
        short = True  # Just fetch keys
        templates_short = ntm.get_templates(short)

    def test_2_device_templates(self):
        """Try to get all full templates"""
        short = False  # Fetch full templates
        templates_full = ntm.get_templates(short)

    def test_3_local_variables(self):
        """Try to load all local variables"""
        default_vars = True  # Use default vars
        local_vars = ntm.load_local_vars(default_vars)

    def test_4_template_rendering(self):
        """Try to render all templates using local variables only"""

        templates_short = ntm.get_templates(True)
        local_vars = ntm.load_local_vars(True)

        for tmpl in templates_short:
            template = ntm.load_template(tmpl, tp_type=TemplateTypes.DEVICES)
            config = ntm.render_config(template["main"], local_vars)


if __name__ == "__main__":
    unittest.main()


"""
    # Find template to use for host:
    template = identify_device_template(templates, host)

    # Loads all variables into a single dictionary
    render_vars = load_vars(host)
    # pprint(render_vars)

    # Load all "snippets" from config section of template
    # And return a single jinja2 string ready to be rendered
    # print(template["config"])
    template_string = load_template(template)

    # Render config by combining variables and jinja2 string
    host_config = render_config(template_string, render_vars)

    # Print config
    # print(host_config)

    # Write Config to File
    changed_config = write_config_file(host["hostname"], host_config)
"""
