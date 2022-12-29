from Command import Command

from DatabaseConnection import DatabaseConnection


class LimitCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        category = commandLine[0]
        limit = float(commandLine[1])

        msg = f"Limiting Category: {category}\n"
        limits = user["limits"]

        if category in limits:
            msg += "Category Already Limited!\n"
            return msg

        updated = dbCon.addLimit(userId, category, limit)

        msg += f"Successfully Limited Category To ₪{limit}!\n" if updated else "Failed To Limit Category!\n"

        return msg