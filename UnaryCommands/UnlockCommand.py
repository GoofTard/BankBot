from Command import Command

from DatabaseConnection import DatabaseConnection


class UnlockCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        category = commandLine[0]

        msg = f"Unlocking Category: {category}\n"
        locks = user["locks"]

        if category in locks:
            msg += "Category Already Unlocked!\n"
            return msg

        updated = dbCon.remLock(userId, category)

        msg += "Successfully Unlocked Category!\n" if updated else "Failed To Unlock Category!\n"

        return msg