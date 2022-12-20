import discord
import pymongo
from commands import *
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

try:
    dbClient = pymongo.MongoClient(
        "mongodb://admin:admin@129.159.130.195:1028/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.1")
    if not 'admin' in dbClient.list_database_names():
        raise Exception("DB Does'nt Esists")

    db = dbClient["admin"]
    users = db["users"]
    print("Successfully Connected to DB!")
except Exception as e:
    print(e)

client = discord.Client(intents=intents)

commands = {
    "percentages": printPercentages,
    "totals": printTotals,
    "add": addMoney,
    "clear": clearBank,
    "use": useMoney,
    "add-cat": addCategory,
    "rem-cat": removeCategory,
    "add-percent": addPercentage,
    "rem-percent": removePercentage,
    "redis": redistribute,
    "help": sendCommands,
    "register": registerUser
}


async def handleCommands(message):
    global user
    try:
        channel = message.channel
        id = str(message.author.id)
        user = users.find_one({"id": id})
        message = message.content.casefold()
        args = message.split(" ")
        command = args[0]

        if not command in commands:
            return

        if (command != "register") and (user is None):
            await channel.send("You Are Not Registered!")
            return

        await commands[command](id, users, user, channel, args[1:])
        with open('../../Downloads/logs.txt', 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} LOG: {user} - {message}\n')
    except IndexError:
        with open('../../Downloads/logs.txt', 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} ERROR: {user} - {message} (Not Enough Arguments)\n')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await handleCommands(message)


client.run("MTA1MzY3Njg4NTY3MTk0MDE4OA.GDrrzO.hA_4cqx1upyeODe1eTHmev0RIJnLD2-Tk9XZlc")
