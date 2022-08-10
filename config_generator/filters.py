"""
 https://gemfury.com/offerpop/python:Jinja2/-/content/jinja2/filters.py
 This file contains filters that can be used in jinja2 templates 
 List of useful filters: https://ttl255.com/jinja2-tutorial-part-4-template-filters/
"""

from netaddr import IPNetwork
from slugify import slugify


# https://github.com/un33k/python-slugify
# INPUT: Björns Städverkstad AB 
# OUTPUT: Bjorns_Stadsverkstad_AB
def slugify_string(text):
    """
    convert the given string to a slug
    :param text:
    :return:
    """
    return slugify(text, separator="_", lowercase=False)


# Returns Prefix Length: 192.168.0.5/24 == 24, 2001:9B0:1:606::0/48 == 48
def prefix_to_len(prefix):
    try:
        net = IPNetwork(prefix)
        return net.prefixlen
    except:
        return prefix.replace("prefix", "len")


# Returns Wildcard 192.168.0.5/24 == 0.0.0.255
def prefix_to_wildcard(prefix):
    try:
        net = IPNetwork(prefix)
        return net.hostmask
    except:
        return prefix.replace("prefix", "wildcard")


# Returns Netmask 192.168.0.5/24 == 255.255.255.0
def prefix_to_netmask(prefix):
    try:
        net = IPNetwork(prefix)
        return net.netmask
    except:
        return prefix.replace("prefix", "netmask")


# Returns Network 192.168.0.5/24 == 192.168.0.0, 2001:9B0:1:606::4/48 == 2001:9B0:1:606::
def prefix_to_network(prefix):
    try:
        net = IPNetwork(prefix)
        return net.network
    except:
        return prefix.replace("prefix", "network")


# Returns Prefix IP 192.168.0.5/24 == 192.168.0.5, 2001:9B0:1:606::4/48 == 2001:9B0:1:606::4
def prefix_to_ip(prefix):
    try:
        net = IPNetwork(prefix)
        return net.ip
    except:
        return prefix.replace("prefix", "ip")

# Returns first host IP 192.168.0.0/24 == 192.168.0.1
def prefix_to_host(prefix):
    try:
        net = IPNetwork(prefix)
        return net.ip[1]
    except:
        return prefix.replace("prefix", "host")


# List of all Active Filters:
FILTERS = {
        'slugify_string': slugify_string,
        'prefix_to_len': prefix_to_len,
        'prefix_to_wildcard': prefix_to_wildcard,
        'prefix_to_netmask': prefix_to_netmask,        
        'prefix_to_network': prefix_to_network,
        'prefix_to_ip': prefix_to_ip,
        'prefix_to_host': prefix_to_host
        }