import discord, os, json
from discord.ext import commands

def read_file(file):
    with open(file) as json_file:
        json_data = json.load(json_file)
        json_file.close()
        return json_data

def has_roles(member: discord.Member, roles: list):
    for role in member.roles:
        if role.id in roles:
            return True

    return False

class Moderation(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command(name = "kick")
    @commands.guild_only()
    async def kick_command(self, ctx, member: discord.Member, *, reason: str = "No reason provided."):
        settings = read_file('./data.json')
        if has_roles(ctx.message.author, settings[str(ctx.message.guild.id)]["moderation-roles"]):
            embed = discord.Embed(
                title = f"{member} kicked!",
                description = f"Kicked by: {ctx.author}\n Reason: {reason}"
            )
            await member.kick(reason=f"'{reason}' - {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name = "ban")
    @commands.guild_only()
    async def ban_command(self, ctx, member: discord.Member, *, reason: str = "No reason provided."):
        settings = read_file('./data.json')
        if has_roles(ctx.message.author, settings[str(ctx.message.guild.id)]["moderation-roles"]):
            embed = discord.Embed(
                title = f"{member} banned!",
                description = f"Banned by: {ctx.author}\n Reason: {reason}"
            )
            await member.ban(reason=f"'{reason}' - {ctx.author}")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("🤡")

    @commands.command(name = "unban")
    @commands.guild_only()
    async def unban_command(self, ctx, id: int, *, reason: str = "No reason provided"):
        settings = read_file('./data.json')
        if has_roles(ctx.message.author, settings[str(ctx.message.guild.id)]["moderation-roles"]):
            banned_users = await ctx.guild.bans()
            for ban_entry in banned_users:
                user_id = ban_entry.user.id
                if (int(id) == int(user_id)):
                    await ctx.guild.unban(ban_entry.user, reason=f"'{reason}' - {ctx.author}")
                    embed = discord.Embed(
                        title = f"{ban_entry.user} unbanned!",
                        description = f"unanned by: {ctx.author}\n Reason: {reason}"
                    )
                    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))