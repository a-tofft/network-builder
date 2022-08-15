#!/usr/bin/env python
print("hello")
'''
import sys
import os
import unittest

sys.path.append(".")
from app.service.ntm import NetworkTemplateManager
from app.config import Config as config
from app.constants import TemplateTypes

# We don't actually connect to netbox for testing scenarios
NETBOX_TOKEN = "ABC"


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
    ntm = NetworkTemplateManager(NETBOX_TOKEN)
    unittest.main()
'''
