from Command import Command
from DatabaseConnection import DatabaseConnection
from NullaryCommands.FundsCommand import FundsCommand


class TransferCommand(Command):
    def execute(self, userId: str, commandLine: list = []) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        fromCat = commandLine[0]
        toCat = commandLine[1]
        funds = float(commandLine[2])
        totals = user["data"]["totals"]
        msg = f"Transferring ₪{funds} From {fromCat} To {toCat}...\n"

        if not fromCat in totals:
            msg += "The 'From' Category Doesn't Exist!"
            return msg

        if not toCat in totals:
            msg += "The 'To' Category Doesn't Exist!"
            return msg

        totals.update({
            fromCat: totals[fromCat] - funds,
            toCat: totals[toCat] + funds
        })

        updated = dbCon.updateUser(
            {
                "$set": {"data.totals": totals}
            },
            userId
        )

        msg += f"Transferred ₪{funds} From {fromCat} To {toCat}!\n" if updated else "Failed Transferring Funds!\n"

        msg += FundsCommand().execute(userId)

        return msg