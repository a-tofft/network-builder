#!/usr/bin/env python
import unittest

from config import Config as config
from filters import *

from network_builder import render_config


class TestNetworkBuilder(unittest.TestCase):
    def test_render_config_input(self):

        input_tmpl = "hostname {{ hostname }}"
        input_vars = {"hostname": "test-device"}
        expected = "hostname test-device"
        task = ""
        output = render_config(task, input_tmpl, input_vars)
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
