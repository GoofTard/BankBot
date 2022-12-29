from Command import Command
from DatabaseConnection import DatabaseConnection
from Formatter import format


class LimitsCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        limits = user["limits"]

        return format(limits, ("Category", "Amount"))
