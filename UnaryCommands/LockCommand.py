from Command import Command

from DatabaseConnection import DatabaseConnection


class LockCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        category = commandLine[0]

        msg = f"Locking Category: {category}\n"
        locks = user["locks"]

        if category in locks:
            msg += "Category Already Locked!\n"
            return msg

        updated = dbCon.addLock(userId, category)

        msg += "Successfully Locked Category!\n" if updated else "Failed To Lock Category!\n"

        return msg