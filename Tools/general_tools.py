import os
import time
import platform
import json

def clear(wait):
    if(platform.system() == 'Windows'):
        time.sleep(wait)
        os.system('cls')
    else:
        time.sleep(wait)
        os.system('clear')

def create_settings(name, type):

    if(name == 'none'):
        name = 'NAME OF THIS SECTION'
    data = {
        "use_config": "False",
        "section_name": f"{name}",
        "bot_name": "Proyecto X",
        "bot_owner": "Error0x03",
        "bot_color": 1791,
        "bot_icon": "https://cdn2.iconfinder.com/data/icons/reptiles-colored/48/Animals_Reptiles_Artboard_17-512.png",
        "bot_footer": "This is a footer"
    }

    if(type == 1):
        default = ["banking", "profile", "admin"]
        for settings_name in default:
            with open(f"Settings/{settings_name}_settings.json", 'w') as f:
                json.dump(data, f, indent=2)
    else:
        with open(f"/Settings/{name}_settings.json", 'w') as f:
            json.dump(data, f, indent=2)

def create_empty_db(name):
    data = {}

    with open(f"DataBase/{name}_db.json") as f:
        json.dump(data, f, indent=2)