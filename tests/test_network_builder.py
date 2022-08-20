#!/usr/bin/env python
import os
import sys
import unittest

sys.path.append(".")
from network_builder.config import Config as config
from network_builder.helpers import load_yaml_file
from network_builder.network_builder import (identify_device_template,
                                             load_template, load_templates,
                                             render_config, write_config_file)


def 

class TestNetworkBuilder(unittest.TestCase):
    def test_render_config_input(self):
        
        input_tmpl = "hostname {{ hostname }}"
        input_vars = {"hostname": "test-device"}
        expected = "hostname test-device"
        output = render_config(input_tmpl, input_vars)
        self.assertEqual(output, expected)

    def test_load_templates()

if __name__ == "__main__":
    unittest.main()
