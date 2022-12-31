from Command import Command
from DatabaseConnection import DatabaseConnection
from NullaryCommands.PercentagesCommand import PercentagesCommand


class AddCategoryCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dict(dbCon.getUser(userId))

        category = commandLine[0]
        percentage = float(commandLine[1])
        categories = user["categories"]
        categoriesNames = []
        for cat in categories:
            categoriesNames.append(cat.category)

        msg = f"Adding Category: {category} And Allocating {percentage}%\n"

        if category in categoriesNames:
            msg += "Category Already Exists!\n"
            return msg

        categories.append({
            "category": category,
            "total": 0,
            "percentage": percentage,
            "locked": False,
            "limit": -1
        })

        updated = dbCon.updateUser(user)

        msg += "Successfully Added Category!\n" if updated else "Failed To Add Category!'\n"

        msg += PercentagesCommand().execute(userId, [])

        return msg
