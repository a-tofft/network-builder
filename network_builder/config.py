import os


class Config(object):

    # General Settings
    TEMPLATES_FILE = "templates.yaml"
    SNIPPETS_DIR = "config_snippets"
    CONFIGS_DIR = "configs"
    CONFIG_FILE_SUFFIX = ".conf"

    # NORNIR
    NR_HOST_FILE = "hosts.yaml"
    NR_GROUP_FILE = "groups.yaml"
    NR_DEFAULTS_FILE = "defaults.yaml"
    NR_WORKERS = 100

    # SSH
    SSH_USERNAME = os.getenv("SSH_USERNAME")
    SSH_PASSWORD = os.getenv("SSH_PASSWORD")

    # Comment Character for Network OS
    COMMENT_CHARS = {"eos": "!", "huawei-vrp": "#"}
    COMMENT_DEFAULT = "!"
