from Command import Command
from DatabaseConnection import DatabaseConnection
from Formatter import formatExtended


class LocksCommand(Command):
    def toListList(self, locks: list) -> list:
        list = []
        for lock in locks:
            list.append([lock])

        return list

    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        locks = user["locks"]

        return formatExtended(1, self.toListList(locks), ["Locks"])
