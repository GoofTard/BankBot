from Command import Command
from DatabaseConnection import DatabaseConnection
from Formatter import format, addPostfix, getWarning


class PercentagesCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        percentages = user["percentages"]
        map = addPostfix(percentages, "%")

        msg = getWarning(percentages)
        msg += format(map, ("Category", "Percentage"))

        return msg
