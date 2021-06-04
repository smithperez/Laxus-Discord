import string
import random

from discord.ext.commands.core import command
from Tools import general_tools as gt
import discord
from discord.ext import commands
import json
import sys
import os
sys.path.append('..')


class Bank(commands.Cog):

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

    if(os.path.isfile('DataBase/profile_db.json') != True):
        gt.create_empty_db('profile')
    elif(os.path.isfile('DataBase/bank_accounts_db.json') != True):
        gt.create_empty_db('bank_accounts')

    # Registe in the bank
    @commands.command(aliases=[])
    async def bank_create(self, ctx):
        author = ctx.author.mention

        with open('DataBase/profile_db.json', 'r') as f:
            financial_info = json.load(f)

        if(author in financial_info):
            if("bank_balance" in financial_info[author]):
                embed = discord.Embed(color = bot_color)
                embed.add_field(name='❌Error❌', value='You are already registered in the Bank🏦.')
                embed.set_footer(text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                await ctx.send(embed=embed)

            else:
                with open('DataBase/bank_accounts_db.json', 'r') as f:
                    bank_accounts = json.load(f)
                
                for i in range(200):
                    random_bank = random.randint(123453, 999999)
                    if(random_bank not in bank_accounts):
                        bank_accounts[random_bank] = f"{ctx.author.name}#{ctx.author.discriminator}"

                        financial_info[author]["bank_balance"] = 10
                        financial_info[author]["bank_account"] = random_bank

                        with open('DataBase/bank_accounts_db.json', 'w') as f:
                            json.dump(bank_accounts, f, indent=2)

                        with open('DataBase/profile_db.json', 'w') as f:
                            json.dump(financial_info, f, indent=2)

                        embed = discord.Embed(color = bot_color)
                        embed.add_field(name='✅Success✅', value='Congratulations you got your Bank Account 🏦.')
                        embed.set_footer(text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                        await ctx.send(embed=embed)

                        break
                    else:
                        pass
        else:
            embed = discord.Embed(color=bot_color)
            embed.add_field(
                name='❌Error❌', 
                value=f'You are not in the DataBase, please use ***{command_prefix}register*** to get registered.')
            embed.set_footer(
                text=f'{section_name} {bot_footer}', icon_url=f'{bot_icon}')
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Bank(bot))
