import json 
import os 
from discord.ext import commands
import sys

if(os.path.isdir('Settings') != True):
    os.mkdir('./Settings')
    dir = {
        "name": "Project X",
        "owner": "Error0x03",
        "token": "DEFAULT",
        "color": 14221056
    }

    with open('./Settings/general_settings.json', 'w') as f:
        json.dump(dir, f, indent=2)
    
    input("Settings & files have been created.....\nPress any key to continue...")
    os.execv(sys.argv[0], sys.argv)
    print("Okey")