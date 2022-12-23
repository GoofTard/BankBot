from Command import Command

from DatabaseConnection import DatabaseConnection
from NullaryCommands.FundsCommand import FundsCommand


class UseCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        category = commandLine[0]
        funds = float(commandLine[1])
        totals = user["data"]["totals"]
        msg = f"Using ₪{funds} From {category}\n"

        if not category in totals:
            msg += "The Category Doesn't Exist!\n"
            return msg

        totals.update({category: totals[category] - funds})

        updated = dbCon.updateUser(
            {
                "$set": {
                    "data.totals": totals,
                    "data.total": user["data"]["total"] - funds,
                    "usages.total": user["usages"]["total"] + funds
                },
                "$push": {
                    "usages.transactions": {category: funds}
                }
            },
            userId
        )

        msg += f"Successfully Used  ₪{funds} From {category}\n" if updated else "Failed To Use Funds!\n"

        msg += FundsCommand().execute(userId, [])

        return msg