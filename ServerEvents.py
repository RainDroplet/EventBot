import json

def create_server_events(guildID):
# Initial command to create an empty event file, needs to be called once per server by the admin.
    server_events = {}

    with open(f'./server_data/{guildID}.json', 'w') as fileOut:
        json.dump(server_events, fileOut, indent=2)

async def add_server_event(guildID, discordID, title, date, time, desc, members):
    return

def load_server_event(guildID):
# This is to retrieve the JSON file that has all the events in a particular server.
    with open(f'./server_data/{guildID}.json', 'w') as fileIn:
        return json.load(fileIn)

def save_server_event(guildID, server_events):
# This is to save the JSON file for all the events in a particular server.
    with open(f'./server_data/{guildID}.json', 'w') as fileOut:
        json.dump(server_events, fileOut, indent=2)