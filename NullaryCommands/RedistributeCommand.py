from Command import Command

from DatabaseConnection import DatabaseConnection
from FundsCommand import FundsCommand


class RedistributeCommand(Command):
    def execute(self, userId: str, commandLine: list = []) -> str:
        dbCon = DatabaseConnection.instance()
        msg = "Redistributing Funds!\n"
        user = dbCon.getUser(userId)
        percentages = user["data"]["percentages"]
        total = user["data"]["total"]

        totals = dict()

        for key in percentages.keys():
            totals.update({f"{key}": total * (percentages[key] / 100.0)})

        if len(percentages.keys()) == 0:
            msg += "Cannot Redistribute Funds! There Are No Categories!\n"
            return msg

        updated = dbCon.updateUser(
            {
                "$set": {"data.totals": totals}
            },
            {"id": userId}
        )

        msg += f"Successfully Redistributed Funds!\n" if updated else "Failed To Redistribute Funds!\n"

        msg += FundsCommand().execute(userId)

        return msg