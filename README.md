# Network Configuration Generator
 - Yes, another one! 
Wrote this a while back to demo some concepts relating to generation of configurations for device configs. 

## Design Decisions
Having a working SoT should always be priority #1. Trying to automate/generate configs for the network without this can quickly become messy. 
The idea is that you generate full configurations, and push either full configurations (replace) to devices or see (extnesions) push the difference in configs. 
With this approach, you don't need to take any backups of device configurations, as your SoT for configs is kept fully within this repository. 

## Ansible vs Python 
Even with ansible, code will be required for certain extensions/issues. 
Speed 
Therefore, as with the concept of usin... 
Verify fast, can generate configurations for 1000 devices within a minute on github

## Templating Concepts

## Picture 
 - Insert picture that displays design 


## Walkthrough 
 1. CI/CD runs 
 2. If any changes were made in below files, run:
    1. - adsd
    2. adds
    3. asd
 3. dsad
 4.  

# Configuration Templates & Snippets 
As the vendors in your network grow and the different device types grow, it becomes hard to maintain the templates 
for all the different devices... 

### Templates 
Templates are used to describe a complete device/service configuration. Templates are specified using yaml. Each device template has different sections used to differentiate what they are used for. See below for all sections in a template and an example. 

<details>
<summary>Example</summary>

```YAML
router_huawei_s6720:
  device_roles: 
    - core-router
  device_types:
    - huawei_s6720
  ports: 
    - huawei_vrp_intf-infra-l3-s6720.j2
  main_config:
    - huawei_vrp_mgmt-pe.j2
    - huawei_vrp_banner.j2
    - huawei_vrp_acls.j2
    - huawei_vrp_prefix-lists.j2
    - huawei_vrp_bgp-communities.j2 
    - huawei_vrp_route-policies.j2
    - huawei_vrp_ipv6.j2
```

</details>

### Snippet 
Snippets are Jinja2 files which contain small configuration snippets, that may be common for many different device/service templates. See below for an example. 

<details>
<summary>Example</summary>

```JINJA
ip access-list standard IPV4-MGMT-SSH
 {% for entry in ssh_acl_entries_v4 %}
 remark {{ entry.comment }}
 {% for network in entry.networks %}
 permit {{ network }}
 {% endfor %}
 {% endfor %}
```

</details>

# Tests 

# Develop locally 
 - Follow below steps to setup locally
 - Use poetry 

# Filters 
 * The fewer variables, the better! 
 * Filters are available at ```filters.py``` and more can be added as needed. Avoid using variables such as "mask/network/hsrp_ip" etc and instead specify prefix and use various filters to convert variable to correct format. 
 * Examples:
```
neighbor {{ interfaces.lan.prefix_v4|lan_prefix_to_bgp(cpe.redundancy.type) }}
ip address {{ management.prefix_v4|prefix_to_ip }} {{ management.prefix_v4|prefix_to_netmask }}
```

# Extensions
Configuration provisioning/management can be done in many different ways and often depends 
on your organization, your requirements and what your current setup looks like. 
The /extensions directory contains example code of how the config management can be extended 
in certain ways. 


#### Integrate Resource Management 
extensions/resource-service.py
extensions/resource-template.j2
{{ name|get_resource_loopback_ipv4 }}
{{ name|get_resource_loopback_ipv4 }}
{{ name|get_resource_loopback_ipv4 }}
Showcases some examples of how resources such as VLANs, IP addresses etc can be fetched by contacting an external resource management system 
directly, rather than having the resources already delegated to the device in question.

#### External Inventory 
extensions/netbox-inventory.py
Showcases an example of how inventory.yml could be replaced with a dynamic inventory, in this example it fetches data from Netbox, transforms it into variables
and then runs as normally. 

#### CI/CD that pushes configuration on changes 
extensions/push-config.py
extensions/push-config-ci.yml
Showcases a CI/CD workflow that could be used in conjunction with config generation. This workflow will be run everytime there are changes in configs/ directory. 
It will then utilize nornir and napalm to detect the difference in configs and try and push this difference to each device in question. 

#### Validate Configurations with Batfish / netq
extensions/validate-config.py
extensions/validate-config-ci.yml
Showcases a CI/CD workflow that could be used to validate rendered configurations to make sure any changes....


#### Netconf Configuration Generation 
extensions/netconf/ 
Showcases examples of how a mix of devices, some using CLI and some using Netconf can be used 




'''
1. Load templates 
2. Load common vars 
3. Load inventory 
4. Go through inventory - Utilizing Threading 
    Generate templates and if they don't exist - Create them 
    If they exist, only overwrite existing file if there is a change (load it)
    
# Other Things:
Have Tests for each function 
Use toml for config file 
Run github action when a change is made to certain files 
Use python decorators for logging as well as debugging. 
j2lint - Lint the jinj2 config 

# Tests 
Can inventory be read correctly?
Has same interface been assigned multiple times? 



# Thoughts 
Run Tests on any commit 
CI/CD Logging? 
Draw.io picture that Displays hierarchy of templates and snippets 
and the reasoning behind it/usability 
Use definitions for everything. def blabla(template: str, vars: dict) -> str
Let CI/CD Create an issue in case of failure? 

Use some form of check to make sure that each host has 
every parameter required in the inventory.yml file. 

https://pc.nanog.org/static/published/meetings/NANOG75/1879/20190218_Garros_Managing_Network_Device_v1.pdf

https://www.reddit.com/r/networking/comments/i827qq/network_automation_is_a_fractured_mess/

CICD: https://github.com/marketplace/actions/verify-changed-files



site: pot-gla
  name: rtr1-pot-gla
  ipv4: 
  ASN:
  device_type: c6500
  role: core-router
  network: 
    lo0.0:
      ips:
        - addr: 
        - addr: 
  ports:
   - name: eth1/2 
     peer: 
     ipv4: 
     mtu:
   - name: eth1/3 
  services:
    bgp_peers:


rtr2-pot-gla.example.net:


rtr3-pot-gla.example.net:


sw1-pot-gla.example.net:


# Check that checks if it is v4 or v6 address? 


'''