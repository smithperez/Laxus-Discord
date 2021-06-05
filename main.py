import json 
import os 
from discord.ext import commands
import sys
sys.path.append('..')
from Tools import general_tools as gt

if(os.path.isdir('Settings') != True or os.path.isdir('DataBase' != True)):
    os.mkdir('./Settings')
    os.mkdir('./DataBase')
    
    dir = {
        "bot_name": "Project X",
        "bot_owner": "Error0x03",
        "bot_token": "DEFAULT",
        "command_prefix": "!",
        "bot_icon": "https://cdn2.iconfinder.com/data/icons/reptiles-colored/48/Animals_Reptiles_Artboard_17-512.png",
        "bot_color": 14221056,
        "bot_footer": "This is a footer"
    }

    with open('./Settings/general_settings.json', 'w') as f:
        json.dump(dir, f, indent=2)
    
    
    input("Settings & files have been created.....\nPress any key to continue...")
    input("Please go to ./Settings/ and configyre all the files there.....\nThen re-start the script.")
    exit()

with open('./Settings/general_settings.json', 'r') as f:
    settings = json.load(f)

if(settings["bot_token"] == 'DEFAULT'):
    print("Please configure the bot TOKEN before run the script.")
    input('Press any key to continue....')
    exit()
else:
    bot = commands.Bot(command_prefix=settings["command_prefix"], id=None)

    for file in os.listdir("Src"):
        if file.endswith(".py"):
            name = file[:-3]
            bot.load_extension(f"Src.{name}")
    
    token = settings["bot_token"]
    bot.run(f"{token}")