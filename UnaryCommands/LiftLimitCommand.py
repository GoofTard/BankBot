from Command import Command
from DatabaseConnection import DatabaseConnection


class LiftLimitCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        category = commandLine[0]

        msg = f"Lifting Limit On Category: {category}\n"
        limits = user["limits"]

        if not category in limits:
            msg += "Category Already Unlimited!\n"
            return msg

        updated = dbCon.remLimit(userId, category)

        msg += f"Successfully Lifted Limit On Category!\n" if updated else "Failed To Lift Limit On Category!\n"

        return msg