from Command import Command
from DatabaseConnection import DatabaseConnection
from Formatter import format, formatExtended


class TransactionsCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        month = dbCon.getLastMonth().strftime("%B")
        user = dbCon.getUser(userId)
        msg = f"{month}'s Transactions:\n"
        transactions = user["usages"]["transactions"]
        is_extended = commandLine[0].casefold() == "extended"

        if len(transactions) == 0:
            return "There Were No Transactions!\n"

        if is_extended:
            msg += formatExtended(
                3,
                transactions,
                ["Category", "Funds Spent", "Message"],
                ["Total", f"₪{user['usages']['total']}", ""]
            )
            msg += "\n"

        categories = {}
        for entry in transactions:
            category = entry[0]
            funds = entry[1]
            if category in categories:
                categories.update({category: categories[category] + funds})
            else:
                categories.update({category: funds})
        msg += format(categories, ("Category", "Funds Spent"), ("Total", f"₪{user['usages']['total']}"))

        return msg