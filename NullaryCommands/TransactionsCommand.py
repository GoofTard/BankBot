from Command import Command
from DatabaseConnection import DatabaseConnection
from Formatter import format


class TransactionsCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        month = dbCon.getLastMonth().strftime("%B")
        user = dbCon.getUser(userId)
        msg = f"{month}'s Transactions:\n"
        transactions = user["usages"]["transactions"]

        if len(transactions) == 0:
            return "There Were No Transactions!\n"

        categories = {}
        for entry in transactions:
            category = list(entry.keys())[0]
            funds = entry[category]
            if category in categories:
                categories.update({category: categories[category] + funds})
            else:
                categories.update({category: funds})

        msg += format(categories, ("Category", "Funds Spent"), ("Total", f"₪{user['usages']['total']}"))

        return msg