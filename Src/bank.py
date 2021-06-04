import string
import random
from discord.embeds import Embed

from discord.ext.commands.core import command
from discord.ext.commands.errors import ExtensionNotLoaded
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
    async def bank_register(self, ctx):
        author = ctx.author.mention

        with open('DataBase/profile_db.json', 'r') as f:
            financial_info = json.load(f)

        if(author in financial_info):
            if("bank_balance" in financial_info[author]):
                embed = discord.Embed(color=bot_color)
                embed.add_field(
                    name='❌Error❌', value='You are already registered in the Bank🏦.')
                embed.set_footer(
                    text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                await ctx.send(embed=embed)
            else:
                if("bank_balance" not in financial_info[author]):
                    with open('DataBase/profile_db.json', 'r') as f:
                        profile_info =  json.load(f)
                    
                    profile_info[author]["bank_balance"] = 0

                    with open('DataBase/profile_db.json', 'w') as f:
                        json.dump(profile_info, f, indent=2)

                    embed = discord.Embed(color=bot_color)
                    embed.add_field(
                        name='✅Success✅', value='Congratulations you got your Bank Account 🏦.')
                    embed.set_footer(
                        text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
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

                            embed = discord.Embed(color=bot_color)
                            embed.add_field(
                                name='✅Success✅', value='Congratulations you got your Bank Account 🏦.')
                            embed.set_footer(
                                text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
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

    # ? Show Balance
    @commands.command(aliases=[])
    async def bank_balance(self, ctx):
        author = ctx.author.mention

        with open('DataBase/profile_db.json', 'r') as f:
            balance_info = json.load(f)

        if(author in balance_info):
            if("bank_balance" in balance_info[author]):
                balance = balance_info[author]["bank_balance"]
                embed = discord.Embed()
                embed.set_footer(
                    text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                embed.add_field(name='Balance🏧',
                                value=f"You have {balance}💰 in your account.")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=bot_color)
                embed.set_footer(
                    text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                embed.add_field(
                    name='❌Error❌', value=f'Please open a Bank Account🏦 with the command ***{command_prefix}bank_register***.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=bot_color)
            embed.add_field(
                name='❌Error❌',
                value=f'You are not in the DataBase, please use ***{command_prefix}register*** to get registered.')
            embed.set_footer(
                text=f'{section_name} {bot_footer}', icon_url=f'{bot_icon}')
            await ctx.send(embed=embed)

    # ? Make Transfer
    @commands.command(aliases=[])
    async def bank_transfer(self, ctx, amount, user: discord.User):
        author = ctx.author.mention
        user = user.mention

        # Read the database
        with open('DataBase/profile_db.json', 'r') as f:
            financial_info = json.load(f)

        if(author in financial_info and "bank_balance" in financial_info[author]):
            if(author == user):
                embed = discord.Embed(color=bot_color)
                embed.add_field(
                    name='❌Error❌', value=f"Sorry, you can't make a transfer to yourself.")
                embed.set_footer(
                    text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                await ctx.send(embed=embed)
            elif(int(amount) > financial_info[author]["bank_balance"]):
                embed = discord.Embed()
                embed.add_field(
                    name='❌Error❌', value="You don't have enough money for this transaction💸.")
                embed.set_footer(
                    text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                await ctx.send(embed=embed)
            elif(int(amount) < 0):
                embed = discord.Embed()
                embed.add_field(
                    name='❌Error❌', value="You can't make negative transactions💸.")
                embed.set_footer(
                    text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                await ctx.send(embed=embed)
            elif(user in financial_info):
                if("bank_account" in financial_info[user]):
                    # Read the database
                    with open('DataBase/profile_db.json', 'r') as f:
                        financial_info = json.load(f)

                    # Make the balance transfer
                    financial_info[author]["bank_balance"] = financial_info[author]["bank_balance"] - int(
                        amount)
                    financial_info[user]["bank_balance"] = int(
                        amount) + financial_info[user]["bank_balance"]

                    with open('DataBase/profile_db.json', 'w') as f:
                        json.dump(financial_info, f, indent=2)

                    # Print the receipt
                    embed = discord.Embed(color=bot_color)
                    embed.add_field(name='✅Transaction Successful✅',
                                    value=f"{author} has transfered {int(amount)}💲 to {user}")
                    embed.set_footer(
                        text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                    await ctx.send(embed=embed)
            elif(user not in financial_info):
                embed = discord.Embed(color=bot_color)
                embed.add_field(
                    name='❌Error❌', value=f"Sorry, {user} doesn't have a bank account.")
                embed.set_footer(
                    text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.add_field(
                name='❌Error❌', value=f"Sorry, you don't have a bank account. Use the command ***!bank_register*** for create one.")
            embed.set_footer(
                text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
            await ctx.send(embed=embed)

    # ? Close account
    @commands.command(aliases=[])
    async def bank_delete(self, ctx):
        with open('DataBase/profile_db.json', 'r') as f:
            financial_info = json.load(f)

        author = ctx.author.mention
        if("bank_balance" in financial_info[author]):
            embed = discord.Embed()
            embed.add_field(name='***⚠️Caution⚠️***',
                            value='''If you delete your account all the founds are going to a donation account. Please use the command ***!delete_confirm*** for delete your bank account.''')
            embed.set_footer(
                text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.add_field(
                name='❌Error❌', value=f"Sorry, you don't have a bank account. Use the command ***!bank_create*** for create one.")
            embed.set_footer(
                text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
            await ctx.send(embed=embed)
    
    @commands.command(aliases=[])
    async def delete_confirm(self, ctx):
        author = ctx.author.mention
        
        if(os.path.isfile('DataBase/charity_db.json') != True):
            gt.create_empty_db('charity')

            charity_info = {
                "bank_balance": 0,
                "deleted_accounts": 0
            }
            with open('DataBase/charity_db.json', 'w') as f:
                json.dump(charity_info, f, indent=2)
        else:
            pass
        
        with open('DataBase/profile_db.json', 'r') as f:
            financial_info = json.load(f)

        with open('DataBase/charity_db.json', 'r') as f:
            charity_info = json.load(f)
        
        if("bank_balance" in financial_info[author]):
            charity_info["bank_balance"] = financial_info[author]["bank_balance"] + charity_info["bank_balance"]
            charity_info["deleted_accounts"] = charity_info["deleted_accounts"] + 1
            
            del financial_info[author]["bank_balance"]
            
            with open('DataBase/charity_db.json', 'w') as f:
                json.dump(charity_info, f, indent=2)

            with open('DataBase/profile_db.json', 'w') as f:
                json.dump(financial_info, f, indent=2)

            embed = discord.Embed()
            embed.add_field(name='⚠️Account Deleted⚠️', value='We are hoping to see you soon. All your founds have been transfered to the Charity')
            embed.set_footer(text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.add_field(name='❌Error❌', value=f"Sorry, you don't have a bank account. Use the command ***!bank_create*** for create one.")
            embed.set_footer(text=f'{bot_name} {bot_footer}', icon_url=f'{bot_icon}')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Bank(bot))
