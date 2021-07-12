import discord
from discord import Embed
from discord import client
from discord import message
from discord.ext import commands
import ServerEvents
import random
from os import path

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
    await ctx.send('`Event added!`')
    await ServerEvents.add_server_event(guildID=ctx.guild.id, discordID=ctx.author.id, title=title, date=date, time=time, desc=desc)
    print('new server event added')

@client.command(aliases=['hostsetup'])
async def host_setup(ctx):
    if path.isfile(f'./server_data/{ctx.guild.id}.json'):
        await ctx.send('`This server already has an event file!`')
    else:
        await ctx.send('`Host setup complete!`')
        await ServerEvents.create_server_events(ctx.guild.id)

@client.command(aliases=['display'])
async def display_server_events(ctx):
    serverEvents = await ServerEvents.display_events(ctx.guild.id)

    eventsEmbed = discord.Embed(
        title=f'Events for {ctx.guild.name}'
    )

    for eventKey in serverEvents:
        event = serverEvents[eventKey]
        eventTitle = event['Title']
        eventDate = event['Date']
        eventTime = event['Time']
        eventDesc = event['Desc']
        eventOwner = await client.fetch_user(int(event['Owner']))
        eventMemberSize = len(event['Members'])

        eventsEmbed.add_field(name=eventTitle, value=(f'```md\n<EventID: {eventKey}>\n<Owner: {eventOwner.name}>\n<Participants: {eventMemberSize}>\n<DATE: {eventDate}>\n<TIME: {eventTime}>\n<Description:\n{eventDesc}>\n```'), inline=False)

    await ctx.send(embed=eventsEmbed)

@client.command(aliases=['events'])
async def direct_message_server_events(ctx):
    serverEvents = await ServerEvents.display_events(ctx.guild.id)

    eventsEmbed = discord.Embed(
        title=f'Events for {ctx.guild.name}'
    )

    for eventKey in serverEvents:
        event = serverEvents[eventKey]
        eventTitle = event['Title']
        eventDate = event['Date']
        eventTime = event['Time']
        eventDesc = event['Desc']
        eventOwner = await client.fetch_user(int(event['Owner']))
        eventMemberSize = len(event['Members'])

        eventsEmbed.add_field(name=eventTitle, value=(f'```md\n<EventID: {eventKey}>\n<Owner: {eventOwner.name}>\n<Participants: {eventMemberSize}>\n<DATE: {eventDate}>\n<TIME: {eventTime}>\n<Description:\n{eventDesc}>\n```'), inline=False)

    await ctx.author.send(embed=eventsEmbed)

@client.command(aliases=['join'])
async def join_server_event(ctx, eventID):
    # print('join command used')
    eventBoolean = await ServerEvents.join_server_event_check(ctx.guild.id, ctx.author.id, eventID)
    # print('pulled boolean')

    if eventBoolean:
        #if this is true then they are in the list already.
        await ctx.send('`You\'re already in the event!`')
    else:
        #they should join the event
        await ctx.send('`Successfully joined the event!`')
        await ServerEvents.join_server_event(ctx.guild.id, ctx.author.id, eventID)

@client.command(aliases=['cancel'])
async def cancel_server_event(ctx, eventID):
    ownerStatus = await ServerEvents.check_event_owner(ctx.guild.id, ctx.author.id, eventID)
    if ownerStatus:
        await ServerEvents.cancel_server_event(ctx.guild.id, ctx.author.id, eventID)
        await ctx.send('`Event `'+ str(eventID) +'` deleted.`')
    else:
        await ctx.send('`Error: You are not the event host.`')

@client.command(aliases=['remove'])
async def remove_event_member(ctx, eventID, discordID):
    ownerStatus = await ServerEvents.check_event_owner(ctx.guild.id, ctx.author.id, eventID)
    if ownerStatus:
        if str(ctx.author.id) == str(discordID):   
            await ctx.send('`Cannot remove yourself from event. If you wish to delete the event use the ,cancel command`')
        else:
            await ServerEvents.remove_event_member(ctx.guild.id, discordID, eventID)
            user = await client.fetch_user(int(discordID))
            await ctx.send(user.name+ '` removed from event.`')
    else:
        await ctx.send('`Error: You are not the event host.`')
        
@client.command(aliases=['leave'])
async def leave_server_event(ctx, eventID):
    eventBoolean = await ServerEvents.join_server_event_check(ctx.guild.id, ctx.author.id, eventID)

    if eventBoolean:
        #if this is true then they are in the list already.
        await ctx.send('`Successfully left the event!`')
        await ServerEvents.leave_server_event(ctx.guild.id, ctx.author.id, eventID)
    else:
        #they are not in the event
        await ctx.send('`You\'re not in the event!`')

@client.command(aliases=['who'])
async def who_is_in_event(ctx, eventID):
    serverEvents = await ServerEvents.display_events(ctx.guild.id)
    # print(serverEvents)

    eventsEmbed = discord.Embed(
        title=f'Events for {ctx.guild.name}'
    )

    eventMembersList = []
    eventMemberSize = len(serverEvents[eventID]['Members'])
    eventOwner = await client.fetch_user(int(serverEvents[eventID]['Owner']))
    # print(eventMembersList)
    eventTitle = serverEvents[eventID]['Title']

    for memberID in serverEvents[eventID]['Members']:
        user = await client.fetch_user(int(memberID))
        eventMembersList.append(user.name)

    # print(eventMembersList)

    eventsEmbed.add_field(name=eventTitle, value=(f'```md\n<EventID: {eventID}>\n<Owner: {eventOwner.name}>\n<Participants: {eventMemberSize}>\n<MemberList: {eventMembersList}>```'), inline=False)

    await ctx.author.send(embed=eventsEmbed)
        
# bot start up -----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # bot_activities = ['with the DEVs', 'with her pen']
    # client = discord.Client(activity=discord.Game(random.choice(bot_activities)))
    # print('Setting discord status...')
    # This part of the code somehow bricks the bot???

    client.run('ODU3MzE2OTAxOTk3NjQxNzU4.YNN0lQ.w2flxx5EDZpG8BlHiLqUd-Wg49g')

# This bot has to be an admin for all of the features to be working. Meaning that ONLY server owners can add this bot to their servers.
# URL to add the bot https://discord.com/api/oauth2/authorize?client_id=857316901997641758&permissions=8&scope=bot