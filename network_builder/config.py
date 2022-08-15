class Config(object):

    # General Settings
    GROUP_VARS = "vars/main.yml"
    TEMPLATES_FILE = "templates.yml"
    SNIPPETS_DIR = "config_snippets"
    INVENTORY = "inventory.yml"
    CONFIGS_DIR = "configs"

    # LOGGING
    LOG_LEVEL = "DEBUG"  # DEBUG>INFO>WARNING>ERROR>CRITICAL
    DEBUG = True

    # ENVIRONMENT
    ENVIRONMENT = "STAGE"

    COMMENT_CHAR = {"ceos": "!"}

    # NAPALM
    NAPALM_DRIVERS = {
        "cisco-ios": "ios",
        "cisco-ios-xe": "ios",
        "ios": "ios",
        "huawei-vrp-v5": "huawei_vrp",
        "huawei-vrp-v8": "ce",
        "cisco-ios-xr": "iosxr",
        "asa": "asa",
        "cisco-asa": "asa",
        "cisco-nx-os": "nxos_ssh",
    }

    NAPALM_USERNAME = ""
    # NAPALM_PASSWORD = os.getenv('NAPALM_PASSWORD')
    NAPALM_SSH_TIMEOUT = 60
    NAPALM_GLOBAL_DELAY_FACTOR = 1  # Default 1, see: netmiko "global_delay_factor"
    NAPALM_SSH_CONFIG = "app/.ssh/ssh_config"
