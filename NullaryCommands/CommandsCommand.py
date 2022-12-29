from Command import Command
from Formatter import format


class CommandsCommand(Command):
    def __init__(self):
        self.commands = {
            "clear": "Clears User's Funds",
            "funds": "Shows Each Category's Allocated Funds",
            "limits": "Prints All Limits",
            "locks": "Prints Locks",
            "percentages": "Shows Each Category's Percentages",
            "redistribute": "Redistributes The Funds",
            "register": "Registers The User",
            "transactions": "Shows This Month's Transactions",
            "add [amount]": "Adds [amount] To Funds",
            "lift-limit [category]": "Lifts A Limit From [category]",
            "lock [category]": "Locks Using Funds From [category]",
            "unlock [category]": "Removes Lock From [category]",
            "rem-cat [category]": "Removes [category] From The Categories",
            "add-cat [category] [percentage]": "Adds [category] And [Percentage] To It",
            "add-percent [category] [percentage]": "Adds [percentage] To [category]",
            "limit [category] [amount]": "Adds A [amount] Fund limit To [category]",
            "rem-percent [category] [percentage]": "Removes [percentage] From [category]",
            "use [category] [amount]": "Uses [amount] From [category]",
            "transfer [from] [to] [amount]": "Transfers [amount] To [to] From [from]"
        }

    def execute(self, userId: str, commandLine: list) -> str:
        return format(self.commands, ("Command Format", "Description"))