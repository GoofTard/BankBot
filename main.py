import discord
import pymongo
from dotenv import load_dotenv
import os
from commands import *
from datetime import datetime
from dateutil import relativedelta

load_dotenv(".env")

intents = discord.Intents.default()
intents.message_content = True

try:
    dbClient = pymongo.MongoClient(os.environ.get('MONGO_KEY'))
    if not 'admin' in dbClient.list_database_names():
        raise Exception("DB Does'nt Esists")

    db = dbClient["admin"]
    users = db["users"]
    last_month = db["last_month"].find_one()["date"]

    # users.update_many(
    #     {},
    #     {
    #         "$set": {
    #             "usages": {
    #                 "total": 0,
    #                 "transactions": []
    #             }
    #         }
    #     }
    # )

    print("Successfully Connected to DB!")
    print(users.find_one({}))

    if relativedelta.relativedelta(datetime.now(), last_month).months > 1:
        users.update_many(
            {},
            {
                "$set": {
                    "usages": {
                        "total": 0,
                        "transactions": []
                    }
                }
            }
        )
        db["last_month"].update_one(
            {},
            {
                "$set": {
                    "last_month": datetime(datetime.now().year, datetime.now().month, 1)
                }
            }
        )

except Exception as e:
    print(e)

client = discord.Client(intents=intents)

commands = {
    "percentages": printPercentages,
    "funds": printTotals,
    "add": addMoney,
    "clear": clearBank,
    "use": useMoney,
    "add-cat": addCategory,
    "rem-cat": removeCategory,
    "add-percent": addPercentage,
    "rem-percent": removePercentage,
    "redistribute": redistribute,
    "register": registerUser,
    "transfer": transferFunds
}


async def handleCommands(message):
    global user, id
    try:
        channel = message.channel
        id = str(message.author.id)
        user = users.find_one({"id": id})
        message = message.content.casefold()
        args = message.split(" ")
        command = args[0]

        if (command != "register") and (user is None):
            await channel.send("You Are Not Registered!")
            return

        if command == "help":
            await channel.send(f"```ini\n{getCommands()}\n```")
        elif not command in commands:
            return
        else:
            await channel.send(f"```\n{commands[command](id, users, user, args[1:])}\n```")

        with open('logs.txt', 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} LOG: {id} - {message}\n')
    except IndexError:
        with open('logs.txt', 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} ERROR: {id} - {message}\n')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await handleCommands(message)


client.run(os.environ.get('BOT_KEY'))
