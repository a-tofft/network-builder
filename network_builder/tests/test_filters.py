#!/usr/bin/env python
import os
import sys
import unittest

from filters import *


class TestFilters(unittest.TestCase):
    """
    Tests input/output from jinja2 filters
    """

    def test_slugify_str(self):
        input_str = "Björnes Ölfabrik AB"
        expected = "Bjornes_Olfabrik_AB"
        output = slugify_string(input_str)
        self.assertEqual(output, expected)

    def test_prefix_to_len(self):
        input_str = "192.168.0.5/24"
        expected = 24
        output = prefix_to_len(input_str)
        self.assertEqual(output, expected)

    def test_prefix_to_wildcard(self):
        input_str = "192.168.0.5/24"
        expected = "0.0.0.255"
        output = prefix_to_wildcard(input_str)
        self.assertEqual(output, expected)

    def test_prefix_to_netmask(self):
        input_str = "192.168.0.5/24"
        expected = "255.255.255.0"
        output = prefix_to_netmask(input_str)
        self.assertEqual(output, expected)

    def test_prefix_to_version_4(self):
        input_str = "192.168.0.5/24"
        expected = 4
        output = prefix_to_version(input_str)
        self.assertEqual(output, expected)

    def test_prefix_to_version_6(self):
        input_str = "2001:B32:100::5/48"
        expected = 6
        output = prefix_to_version(input_str)
        self.assertEqual(output, expected)

    def test_prefix_to_network(self):
        input_str = "192.168.0.5/24"
        expected = "192.168.0.0"
        output = prefix_to_network(input_str)
        self.assertEqual(output, expected)

    def test_prefix_to_ip(self):
        input_str = "192.168.0.5/24"
        expected = "192.168.0.5"
        output = prefix_to_ip(input_str)
        self.assertEqual(output, expected)

    """
    def test_prefix_to_first_host(self):
        input_str = "192.168.0.0/24"
        expected = "192.168.0.1"
        output = prefix_to_first_host(input_str)
        self.assertEqual(output, expected)
    """


if __name__ == "__main__":
    unittest.main()
