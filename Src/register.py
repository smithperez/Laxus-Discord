import discord
from discord.ext import commands
import json

from discord.ext.commands.core import Command 

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open('Settings/general_settings.json', 'r') as f:
        settings = json.load(f)

    with open('Settings/banking_settings.json', 'r') as f:
        section_settings = json.load(f)
    
    global bot_name
    global bot_owner
    global bot_icon
    global bot_color
    global bot_footer
    global section_name
    global command_prefix
    command_prefix = settings["command_prefix"]

    if(section_settings["use_config"] == "True"):
        section_name = section_settings["section_name"]
        bot_name = section_settings["bot_name"]
        bot_owner = section_settings["bot_owner"]
        bot_icon = section_settings["bot_icon"]
        bot_color = section_settings["bot_color"]
        bot_footer = section_settings["bot_footer"]
    else:
        section_name = settings["bot_name"]
        bot_name = settings["bot_name"]
        bot_owner = settings["bot_owner"]
        bot_icon = settings["bot_icon"]
        bot_color = settings["bot_color"]
        bot_footer = settings["bot_footer"]

    @commands.command(aliases=[])
    async def register(self, ctx):
        author = ctx.author.mention
        author_name = f"{ctx.author.name}#{ctx.author.discriminator}"
        with open('DataBase/profile_db.json', 'r') as f:
            profile_data = json.load(f)
        
        if(author in profile_data):
            embed = discord.Embed(color = bot_color)
            embed.add_field(name='❌Error❌', value='You are already registered in the DataBase.')
            embed.set_footer(text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
            await ctx.send(embed=embed)
        else:
            profile_data[author] = {
                "user_id": f"{author_name}",
                "xp": 0,
                "level": 1,
                "next_level": 15,
                "casino_balance": 0,
                "job": "Unemployed",
            }

            with open('DataBase/profile_db.json', 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            embed = discord.Embed(color = bot_color)
            embed.add_field(name='✅Success✅', value='You have been registered in the DataBase.')
            embed.set_footer(text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Register(bot))