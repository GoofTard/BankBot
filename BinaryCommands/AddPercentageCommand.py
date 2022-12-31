from Command import Command

from DatabaseConnection import DatabaseConnection
from NullaryCommands.PercentagesCommand import PercentagesCommand


class AddPercentageCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        category = commandLine[0]
        percentage = float(commandLine[1])
        percentages = user["percentages"]
        msg = f"Allocating {percentage}% More To {category}\n"

        if not category in percentages.keys():
            msg += "Category Doesn't Exist!\n"
            return msg

        updated = dbCon.updateUser(
            {
                "$set": {
                    f"percentages.{category}": percentages[category] + percentage
                }
            },
            userId
        )

        msg += f"Successfully Allocated {percentage}% More To {category}\n" if updated else "Failed To Add Percentage!\n"

        msg += PercentagesCommand().execute(userId, [])

        return msg