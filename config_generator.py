

class NTMException(Exception):
    """ base exception for all NetworkTemplateManager exceptions """
    def __init__(self, msg=''):
        self.logger = logging.getLogger(__name__)
        self.msg = msg
        self.logger.error(self.msg, exc_info=True)

    def __str__(self):
        return self.msg



def get_templates(self, short):
    """ API Function that returns all device templates  """

    tp_type = TemplateTypes.DEVICES
    templates = self.load_templates(tp_type, short)
    return templates



def get_snippet(self, snippet_name):
    """ Returns a single, unrendered snippet """ 

    try:

        files = glob.glob(config.SNIPPETS_DIR + f"/**/{snippet_name}", recursive = True)
        if len(files) > 1:
            raise NTMException(f"Found more than one snippet matchning: {snippet_name}")
        elif len(files) == 0:
            raise NTMException(f"No snippet found with name: {snippet_name}")

        with open(files[0], "r") as f:
            snippet = f.read()

        return snippet

    except Exception as e:
        raise NTMException(f"Error getting snippet - {e.args}")



def render_device(self, object_id, template_name, default_vars, override_vars):
    """ API Function that renders config for a specific device located in netbox """

    # Determine the template to use 
    if template_name:
        self.template_name = template_name
    else: 
        self.template_name = self.identify_device_template(object_id, TemplateTypes.DEVICES)

    # Collect all template details
    template = self.load_template(self.template_name, tp_type=TemplateTypes.DEVICES)

    # Assemble all variables to be used for rendering
    local_vars = self.load_local_vars(default_vars)
    render_vars = self.load_netbox_vars(object_id, local_vars)
    render_vars.update(override_vars)

    # Render Configuration and add to content:
    content = { "main": "", 
                "extras": []
                }

    content["main"] = self.render_config(template["main"], render_vars)

    for extra in template["extras"]:
        rendered_config = self.render_config(extra["content"], render_vars)
        content["extras"].append({ "name": extra["name"], "content": rendered_config})

    # Notify mattermost of configuration render
    # Currently disabled. Should be changed to notify when config has been uploaded to ZTP. 
    '''
    mm_message = f"**Summary**: Configuration has been rendered for [{render_vars['hostname']}]({config.NETBOX_URL}/dcim/devices/{object_id}), {render_vars['serial']}, {render_vars['device_type']}"
    self.mm.send_message(MatterMostEventTypes.EVENT_RENDER_CONFIG, 
                        mm_message)
    '''

    # Returns Content
    return content 

    '''
    content = {
        "main": "..........."
        "extras": [
            {
            "name": "iptv_config", 
            "content": ".........."
            },
            {
            "name": "service_config", 
            "content": ".........."
            },
        ]
    }
    '''








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



# Thoughts 
Run Tests on any commit 
CI/CD Logging? 
Draw.io picture that Displays hierarchy of templates and snippets 
and the reasoning behind it/usability 
Use definitions for everything. def blabla(template: str, vars: dict) -> str
Let CI/CD Create an issue in case of failure? 

Use some form of check to make sure that each host has 
every parameter required in the inventory.yml file. 



'''