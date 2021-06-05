from os import name
import discord
from discord import message
from discord.embeds import Embed
from discord.ext import commands
import json
import sys
sys.path.append('..')

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open('Settings/general_settings.json', 'r') as f:
        settings = json.load(f)

    with open('Settings/profile_settings.json', 'r') as f:
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
    
    #? Leveling
    @commands.Cog.listener()
    async def on_message(self, message):
        author = f'<@{message.author.id}>'

        with open('DataBase/profile_db.json', 'r') as f:
            profile = json.load(f)
        
        with open('Settings/profile_settings.json', 'r') as f:
            leveling = json.load(f)

        if(author in profile):
            profile[author]["xp"] = profile[author]["xp"] + 1

            if(profile[author]["xp"] > profile[author]["next_level"]):
                if(profile[author]["level"] + 1 <= 7):
                    profile[author]["next_level"] = int((profile[author]["next_level"] * leveling["xp_multiplier"]["easy"]) + profile[author]["next_level"])
                elif(profile[author]["level"] + 1 >= 8):
                    profile[author]["next_level"] = int((profile[author]["next_level"] * leveling["xp_multiplier"]["easy"]) + profile[author]["next_level"])
                elif(profile[author]["level"] + 1 >= 15):
                    profile[author]["next_level"] = int((profile[author]["next_level"] * leveling["xp_multiplier"]["easy"]) + profile[author]["next_level"])

                reached_level = profile[author]["level"] + 1
                profile[author]["level"] = reached_level

                embed = discord.Embed(color = bot_color)
                embed.add_field(name="🎉Congratulations🎉", value=f"Congratulations {author} you have reached ***level {reached_level}***.")
                embed.set_footer(text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                await message.channel.send(embed=embed)
            
            with open('DataBase/profile_db.json', 'w') as f:
                json.dump(profile, f, indent=2)
    
    #? Show profile info
    @commands.command(aliases=[])
    async def profile(self, ctx):
        author = ctx.author.mention

        with open('DataBase/profile_db.json', 'r') as f:
            profile_info = json.load(f)

        level = profile_info[author]["level"]
        job = profile_info[author]["job"]
        xp = profile_info[author]["xp"]
        next_xp = profile_info[author]["next_level"]

        embed = discord.Embed(color = bot_color)
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name='***🔬Level🧪***', value=f"{level}")
        # embed.add_field(name='***👷🏻‍♂️Job👷🏻‍♂️***', value=f"{job}")
        embed.add_field(name='***🕹Actual XP🎮***', value=f"{xp}")
        embed.add_field(name='***🎱Required XP for next level🎳***', value=f"{next_xp}")
        embed.set_footer(text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Profile(bot))