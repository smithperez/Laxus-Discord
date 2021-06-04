from datetime import datetime
from discord.ext import commands
import sys
sys.path.append('..')
from tqdm import tqdm
from Tools import general_tools as gt

class Start(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        for i in tqdm(range(0,100), desc="Loading all modules...."):
            pass
    
    @commands.Cog.listener()
    async def on_ready(self):
        date = datetime.now()
        gt.clear(2)

        print(f"""
*****************
* Logged in as: *
*****************
        |
        v
{self.bot.user}
******************
*Date: {date.strftime('%Y-%m-%d')}*
******************
        """)

def setup(bot):
    bot.add_cog(Start(bot))