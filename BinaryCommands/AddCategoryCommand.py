from Command import Command
from DatabaseConnection import DatabaseConnection
from NullaryCommands.PercentagesCommand import PercentagesCommand


class AddCategoryCommand(Command):
    def execute(self, userId: str, commandLine: list = []) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        category = commandLine[0]
        percentage = float(commandLine[1])
        percentages = user["data"]["percentages"]
        msg = f"Adding Category: {category} And Allocating {percentage}%\n"

        if category in percentages.keys():
            msg += "Category Already Exists!\n"
            return msg

        updated = dbCon.updateUser(
            {
                "$set": {
                    f"data.percentages.{category}": percentage,
                    f"data.totals.{category}": 0
                }
            },
            userId
        )

        msg += "Successfully Added Category!\n" if updated else "Failed To Add Category!'\n"

        msg += PercentagesCommand().execute(userId)

        return msg
