import discord
from discord.ext import commands
import json
import sys
import os
sys.path.append('..')
from Tools import general_tools as gt

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open('/Settings/general_settings.json', 'r') as f:
        settings = json.load(f)
    
    with open('/Settings/banking_settings.json', 'r') as f:
        section_settings = json.load(f)
    
    global bot_name
    global bot_owner
    global bot_icon
    global bot_color
    global bot_footer
    global section_name

    if(section_settings["use_config"] == "True"):
        section_name = section_settings["section_name"]
        bot_name = section_settings["bot_name"]
        bot_owner = section_settings["bot_owner"]
        bot_icom = section_settings["bot_icon"]
        bot_color = section_settings["bot_color"]
        bot_footer = section_settings["bot_footer"]
    else:
        bot_name = settings["bot_name"]
        bot_owner = settings["bot_owner"]
        bot_icom = settings["bot_icon"]
        bot_color = settings["bot_color"]
        bot_footer = settings["bot_footer"]

    if(os.path.isfile('DataBase/profile_db.json') != True):
        gt.create_empty_db('profile')

    #Registe in the bank
    @commands.command(aliases=[])
    async def bank_create(self, ctx):
        author = ctx.author.mention

def setup(bot):
    bot.add_cog(Bank(bot))