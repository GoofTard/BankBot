from Command import Command
from DatabaseConnection import DatabaseConnection
from NullaryCommands.PercentagesCommand import PercentagesCommand


class RemovePercentageCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        category = commandLine[0]
        percentage = float(commandLine[1])
        percentages = user["data"]["percentages"]
        msg = f"Allocating {percentage}% Less To {category}\n"

        if not category in percentages.keys():
            msg += "Category Doesn't Exist!\n"
            return msg

        updated = dbCon.updateUser(
            {
                "$set": {
                    f"data.percentages.{category}": percentages[category] - percentage
                }
            },
            userId
        )

        msg += f"Successfully Allocated {percentage}% Less To {category}\n" if updated else "Failed To Remove Percentage!\n"

        msg += PercentagesCommand().execute(userId, [])

        return msg