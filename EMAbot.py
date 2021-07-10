import discord
from discord import Embed
from discord import client
from discord.ext import commands
import ServerEvents
import random

client = commands.Bot(command_prefix=",")

# client events ------------------------------------------------------------------------------------------------------------

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
# This is a server admin command.
async def clr(ctx, *, arg):
    if arg == 'all':
        async for message in ctx.message.channel.history(oldest_first=True):
            await message.delete()
    else:
        async for message in ctx.message.channel.history(limit=int(arg)+1):
            await message.delete()
    # This allows the bot to delete all messages in a channel specifically.

@client.command()
async def catch(ctx, arg1, arg2, arg3):
    await ctx.send(f'{arg1}, {arg2}, {arg3}')

# Host command ----------------------------------------------------------------------------------------------------------

@client.command()
async def host(ctx, title, date, time, desc):
    print(f'{title}, {date}, {time}, {desc}')
    await ServerEvents.add_server_event(guildID=ctx.guild.id, discordID=ctx.author.id, title=title, date=date, time=time, desc=desc)
    print('new server event added')

@client.command(aliases=['hostsetup'])
async def host_setup(ctx):
    await ServerEvents.create_server_events(ctx.guild.id)
    print('created new server hosting json')

@client.command(aliases=['display'])
async def display_server_events(ctx):
    serverEvents = ServerEvents.display_events(ctx.guild.id)
    print('pulled server events')

    eventsEmbed = discord.Embed(
        title=f'Events for {ctx.guild.name}'
    )

    for eventKey in serverEvents:
        event = serverEvents[eventKey]
        eventTitle = event['Title']
        eventDate = event['Date']
        eventTime = event['Time']
        eventDesc = event['Desc']
        ownerID = client.get_user(event['Owner'])

        eventsEmbed.add_field(name=eventTitle, value=(f'```DATE:{eventDate}\TIME:{eventTime}\nDescription:{eventDesc}\nowner:{ownerID.name}\n'))

    await ctx.send(embed=eventsEmbed)


# bot start up -----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # bot_activities = ['with the DEVs', 'with her pen']
    # client = discord.Client(activity=discord.Game(random.choice(bot_activities)))
    # print('Setting discord status...')
    # This part of the code somehow bricks the bot???

    client.run('ODU3MzE2OTAxOTk3NjQxNzU4.YNN0lQ.w2flxx5EDZpG8BlHiLqUd-Wg49g')

# This bot has to be an admin for all of the features to be working. Meaning that ONLY server owners can add this bot to their servers.
# URL to add the bot https://discord.com/api/oauth2/authorize?client_id=857316901997641758&permissions=8&scope=bot