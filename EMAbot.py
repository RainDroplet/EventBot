import discord
from discord import Embed
from discord import client
from discord.ext import commands
import random

client = commands.Bot(command_prefix=",")

# client events ------------------------------------------------------------------------------------------------------------

@client.event
# Allows the bot to announce the user and ping them for the rules page.
async def on_member_join(member):
    channel = member.guild.text_channels[0]
    await channel.send(
        f'Welcome to {member.guild.name}, {member.mention}!')


@client.event
# This will notify users that it is an invalid command and delete the messages
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete(delay=5)
        msg = await ctx.send('Invalid command, try again.')
        await msg.delete(delay=5)

# bot commands -----------------------------------------------------------------------------------------------------------

@client.command()
async def ping(ctx):
    await ctx.send('pong')
    print(ctx.message)

@client.command(aliases=['clear'])
async def clr(ctx, *, arg):
    if arg == 'all':
        async for message in ctx.message.channel.history(oldest_first=True):
            await message.delete()
    else:
        async for message in ctx.message.channel.history(limit=int(arg)+1):
            await message.delete()
    # This allows the bot to delete all messages in a channel specifically.

# bot start up -----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # bot_activities = ['with the DEVs', 'with her pen']
    # client = discord.Client(activity=discord.Game(random.choice(bot_activities)))
    # print('Setting discord status...')
    # This part of the code somehow bricks the bot???

    client.run('ODU3MzE2OTAxOTk3NjQxNzU4.YNN0lQ.w2flxx5EDZpG8BlHiLqUd-Wg49g')
    