from netaddr import IPAddress, IPNetwork
from slugify import slugify


# https://github.com/un33k/python-slugify
# INPUT: Wälling Brödverkstad AB
# OUTPUT: Walling Brodverkstad AB
def slugify_string(text: str) -> str:
    """
    convert the given string to a slug
    :param text:
    :return: slugified string
    """
    return slugify(text, separator="_", lowercase=False)


# Returns Prefix Length: 192.168.0.5/24 == 24, 2001:B32:100::5/48 == 48
def prefix_to_len(prefix: str) -> int:
    net = IPNetwork(prefix)
    return int(net.prefixlen)


# Returns Wildcard 192.168.0.5/24 == 0.0.0.255
def prefix_to_wildcard(prefix: str) -> str:
    net = IPNetwork(prefix)
    return str(net.hostmask)


# Returns Netmask 192.168.0.5/24 == 255.255.255.0
def prefix_to_netmask(prefix: str) -> str:
    net = IPNetwork(prefix)
    return str(net.netmask)


# Returns version of Prefix
# 4 for IPv4
# 6 for IPv6
def prefix_to_version(prefix: str) -> int:
    net = IPNetwork(prefix)
    return int(net.version)


# Returns version of IP
def ip_to_version(prefix: str) -> str:
    net = IPAddress(prefix)
    return str(net.version)


# Returns Network 192.168.0.5/24 == 192.168.0.0, 2001:B32:100::5/48 == 2001:B32:100::
def prefix_to_network(prefix: str) -> str:
    net = IPNetwork(prefix)
    return str(net.network)


# Returns Prefix IP 192.168.0.5/24 == 192.168.0.5, 2001:B32:100::5/48 == 2001:B32:100::5
def prefix_to_ip(prefix: str) -> str:
    net = IPNetwork(prefix)
    return str(net.ip)


# Returns first host IP 192.168.0.0/24 == 192.168.0.1
def prefix_to_first_host(prefix: str) -> str:
    net = IPNetwork(prefix)
    return str(net.ip[1])


# List of all Active Filters:
FILTERS = {
    "slugify_string": slugify_string,
    "prefix_to_len": prefix_to_len,
    "prefix_to_wildcard": prefix_to_wildcard,
    "prefix_to_netmask": prefix_to_netmask,
    "prefix_to_network": prefix_to_network,
    "prefix_to_ip": prefix_to_ip,
    "prefix_to_host": prefix_to_first_host,
    "prefix_to_version": prefix_to_version,
    "ip_to_version": ip_to_version,
}
