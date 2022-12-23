import discord

from dotenv import load_dotenv
import os
from DatabaseConnection import DatabaseConnection
from datetime import datetime
from dateutil import relativedelta
import re

from BinaryCommands.AddCategoryCommand import AddCategoryCommand
from BinaryCommands.AddCommand import AddCommand
from BinaryCommands.AddPercentageCommand import AddPercentageCommand
from BinaryCommands.RemovePercentageCommand import RemovePercentageCommand
from BinaryCommands.UseCommand import UseCommand
from NullaryCommands.ClearCommand import ClearCommand
from NullaryCommands.CommandsCommand import CommandsCommand
from NullaryCommands.FundsCommand import FundsCommand
from NullaryCommands.PercentagesCommand import PercentagesCommand
from NullaryCommands.RedistributeCommand import RedistributeCommand
from NullaryCommands.RegisterCommand import RegisterCommand
from NullaryCommands.TransactionsCommand import TransactionsCommand
from ThreeArgsCommands.TransferCommand import TransferCommand
from UnaryCommands.RemoveCategoryCommand import RemoveCategoryCommand

load_dotenv(".env")

intents = discord.Intents.default()
intents.message_content = True

try:
    dbCon = DatabaseConnection.instance()
    if relativedelta.relativedelta(datetime.now(), dbCon.getLastMonth()).months >= 1:
        dbCon.updateUsers(
            {
                "$set": {
                    "usages": {
                        "total": 0,
                        "transactions": []
                    }
                }
            }
        )
        dbCon.updateLastMonth()
    print(dbCon.getUser("TEST"))

except Exception as e:
    print(e)

client = discord.Client(intents=intents)

commands = {
    "help": CommandsCommand(),
    "percentages": PercentagesCommand(),
    "funds": FundsCommand(),
    "add": AddCommand(),
    "clear": ClearCommand(),
    "use": UseCommand(),
    "add-cat": AddCategoryCommand(),
    "rem-cat": RemoveCategoryCommand(),
    "add-percent": AddPercentageCommand(),
    "rem-percent": RemovePercentageCommand(),
    "redistribute": RedistributeCommand(),
    "register": RegisterCommand(),
    "transfer": TransferCommand(),
    "transactions": TransactionsCommand()
}

def splitCommandLine(message: str) -> tuple:
    command = re.findall("^([\w\-]+)", message)[0]
    args = re.findall("(-[\w]*)|\"(.*?)\"", message)

    return (command, args)

async def handleCommands(message):
    id = None
    try:
        channel = message.channel
        id = str(message.author.id) if not bool(os.environ.get("IS_TEST")) else "TEST"
        message = message.content.casefold()
        (command, args) = splitCommandLine(message)

        print(command)
        print(args)

        if bool(os.environ.get("IS_TEST")):
            await channel.send(f"```\nNOTICE!!!!\nTHE BOT IS IN TEST MODE AT THE MOMENT\n```")

        await channel.send(f"```\n{commands[command].execute(id, args)}\n```")

        with open('logs.txt', 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} LOG: {id} - {message}\n')
    except Exception as e:
        with open('logs.txt', 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} ERROR: {id} - {message} - {e}\n')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await handleCommands(message)


client.run(os.environ.get('BOT_KEY'))
