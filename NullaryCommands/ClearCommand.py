from Command import Command
from DatabaseConnection import DatabaseConnection
from NullaryCommands.FundsCommand import FundsCommand


class ClearCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        msg = "Clearing Funds\n"
        user = dbCon.getUser(userId)
        totals = user["data"]["totals"]

        for key in totals.keys():
            totals.update({f"{key}": 0})

        if len(totals.keys()) == 0:
            msg += "Cannot Clear Funds! There Are No Categories!\n"
            return msg

        updated = dbCon.updateUser(
            {
                "$set": {"data.totals": totals, "data.total": 0}
            },
            userId
        )

        msg += f"Successfully Cleared Funds!\n" if updated else "Failed To Clear Funds!\n"

        msg += FundsCommand().execute(userId, [])

        return msg