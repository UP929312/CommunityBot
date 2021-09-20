import discord
from discord.ext import commands

import requests
from bisect import bisect

from parse_profile import get_profile_data

from utils import error, format_duration
from emojis import DUNGEON_BOSS_EMOJIS

BOSS_INDEX_DICT = {"1": "Bonzo",
                   "2": "Scarf",
                   "3": "The Professor",
                   "4": "Thorn",
                   "5": "Livid",
                   "6": "Sadan",
                   "7": "Necron"}


catacombs_levels = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140, 259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640, 3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640, 23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640, 139559640, 177559640, 225559640, 285559640, 360559640, 453559640, 569809640 ]

class dungeons_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['d', 'dungeon'])
    async def dungeons(self, ctx, username=None, profile=None):

        player_data = await get_profile_data(ctx, username, profile)
        if player_data is None:
            return
        username = player_data["username"]

        #if not player_data.get("dungeons"):
        #    return await error(ctx, "Error, this person's dungeon API is off!", "This command requires the bot to be able to see their dungeon data to work!")

        dungeon_data = player_data["dungeons"]["dungeon_types"]["catacombs"]

        if dungeon_data == {} or "tier_completions" not in dungeon_data:
            return await error(ctx, "Error, this player hasn't played enough dungeons", "The player you have looked up hasn't completed any dungeons runs, so their data can't be shown.")

        tiers_completed = max(dungeon_data["tier_completions"].keys(), key=lambda x: x)           
        level = bisect(catacombs_levels, dungeon_data['experience'])

        try:        
            secrets_found = requests.get(f"https://sky.shiiyu.moe/api/v2/dungeons/{username}/{player_data['cute_name']}").json()
            secrets_found = secrets_found["dungeons"].get("secrets_found", "???")
        except:
            secrets_found = "???"
        
        embed = discord.Embed(title=f"{username}", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        
        embed.add_field(name=f"Dungeon Data:", value=f"Catacombs Level: **{level}**\nSecrets Found: **{secrets_found}**", inline=False)

        for i in range(1, int(tiers_completed)+1):
            index = str(i)
            kills = int(dungeon_data["tier_completions"][index])
            best_runs = dungeon_data["best_runs"][index]
            best_run = max(best_runs, key=lambda x: x["score_exploration"]+x["score_speed"]+x["score_skill"]+x["score_bonus"])
            best_run_score = best_run["score_exploration"]+best_run["score_speed"]+best_run["score_skill"]+best_run["score_bonus"]
            best_run_time = format_duration(best_run["elapsed_time"], include_millis=False)

            embed.add_field(name=f"{DUNGEON_BOSS_EMOJIS[index]} {BOSS_INDEX_DICT[index]}", value=f"Kills: **{kills}**\nTop Run Score: **{best_run_score}**\nTop Run Time: **{best_run_time}**", inline=True)

        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)