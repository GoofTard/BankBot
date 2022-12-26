from Command import Command
from Formatter import format


class CommandsCommand(Command):
    def __init__(self):
        self.commands = {
            "clear": "Clears User's Funds",
            "funds": "Shows Each Category's Allocated Funds",
            "percentages": "Shows Each Category's Allocated Percentages",
            "redistribute": "Redistributes The Funds By Percentages",
            "register": "Registers The User",
            "transactions": "Shows This Month's Transactions",
            "rem-cat [category]": "Removes [category] From The Categories",
            "add [amount] [category](Optional) \"message goes here\"": "Adds [amount] To [category](Optional)",
            "add-cat [category] [percentage]": "Adds [category] And Allocates [Percentage] To It",
            "add-percent [category] [percentage]": "Adds [percentage] To [category]",
            "rem-percent [category] [percentage]": "Removes [percentage] From [category]",
            "use [category] [amount]": "Uses [amount] From [category]",
            "transfer [from] [to] [amount]": "Transfers [amount] To [to] From [from]"
        }

    def execute(self, userId: str, commandLine: list) -> str:
        return format(self.commands, ("Command Format", "Description"))