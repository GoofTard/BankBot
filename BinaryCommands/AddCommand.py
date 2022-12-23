from Command import Command

from DatabaseConnection import DatabaseConnection
from NullaryCommands.FundsCommand import FundsCommand


class AddCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        percentages = user["data"]["percentages"]
        funds = float(commandLine[0])
        totals = user["data"]["totals"]

        if len(commandLine) > 1:
            msg = f"Adding ₪{funds} To {commandLine[1]}\n"
            category = commandLine[1]
            totals.update({category: totals[category] + funds})
        else:
            msg = f"Adding ₪{funds}\n"
            for key in percentages.keys():
                totals.update({key: totals[key] + funds * (percentages[key] / 100.0)})

            if len(percentages.keys()) == 0:
                msg += "Cannot Add Funds! There Are No Categories!\n"
                return msg

        updated = dbCon.updateUser(
            {
                "$set": {"data.totals": totals},
                "$inc": {"data.total": funds}
            },
            userId
        )

        msg += "Failed To Add Funds!\n" if not updated else \
            (f"Successfully Added ₪{funds} To {commandLine[1]}!\n" if len(commandLine) > 1 else
             f"Successfully Added ₪{funds}!\n")

        msg += FundsCommand().execute(userId, [])

        return msg