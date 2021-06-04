import json 
import os 
from discord.ext import commands
import sys

from discord.ext.commands.core import command

if(os.path.isdir('Settings') != True):
    os.mkdir('./Settings')
    dir = {
        "name": "Project X",
        "owner": "Error0x03",
        "token": "DEFAULT",
        "color": 14221056,
        "prefix": "!"
    }

    with open('./Settings/general_settings.json', 'w') as f:
        json.dump(dir, f, indent=2)
    
    input("Settings & files have been created.....\nPress any key to continue...")
    input("Please go to ./Settings/general_settings.json and configyre everything.....\nThen re-start the script.")
    exit()

with open('./Settings/general_settings.json', 'r') as f:
    settings = json.load(f)

if(settings["token"] == 'DEFAULT'):
    print("Please configure the bot TOKEN before run the script.")
    input('Press any key to continue....')
    exit()
else:
    bot = commands.Bot(command_prefix=settings["prefix"], id=None)

    for file in os.listdir("SRC"):
        if file.endswith(".py"):
            name = file[:-3]
            bot.load_extension(f"SRC.{name}")
    
    token = settings["token"]
    bot.run(f"{token}")