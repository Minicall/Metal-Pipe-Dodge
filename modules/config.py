import os
import configparser


#ToDo create config if not exist
def load_config():
    cfg_parser = configparser.RawConfigParser()
    cfg_path = os.path.join(os.path.dirname(__file__), '../config.cfg')
    cfg_parser.read(cfg_path)

    # load resolution settings
    device_resolution = cfg_parser.get("resolution", "device_resolution")
    display_width = cfg_parser.get("resolution", "display_width")
    display_height = cfg_parser.get("resolution", "display_height")

    return {'device_resolution': device_resolution, 'display_width': int(display_width),
            'display_height': int(display_height)}
