from Command import Command

from DatabaseConnection import DatabaseConnection
from NullaryCommands.PercentagesCommand import PercentagesCommand


class RemoveCategoryCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        category = commandLine[0]

        msg = f"Removing Category: {category}\n"
        percentages = user["percentages"]

        if not category in percentages.keys():
            msg += "Category Doesn't Exist!\n"
            return msg

        updated = dbCon.updateUser(
            {
                "$unset": {
                    f"percentages.{category}": 1,
                    f"totals.{category}": 1
                }
            },
            userId
        )

        msg += "Successfully Removed Category!\n" if updated else "Failed To Removed Category!\n"
        msg += PercentagesCommand().execute(userId, [])

        return msg