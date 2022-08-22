#!/usr/bin/env python
import unittest

from config import Config as config
from filters import *

from network_builder import load_templates, render_config


class TestNetworkBuilder(unittest.TestCase):
    def test_render_config_input(self):

        input_tmpl = "hostname {{ hostname }}"
        input_vars = {"hostname": "test-device"}
        expected = "hostname test-device"
        output = render_config(input_tmpl, input_vars)
        self.assertEqual(output, expected)

    """
    def test_load_template(self):

        input = load_yaml_file("tests/templates.yml")
        output = load_template(input)
        print(output)
        template_name = output[0]["template_name"]
        expected = "test_template"
        self.assertEqual(template_name, expected)
    """


if __name__ == "__main__":
    unittest.main()
