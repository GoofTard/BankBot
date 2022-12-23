from Command import Command
from DatabaseConnection import DatabaseConnection
from Formatter import format, addPrefix


class FundsCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        totals = user["data"]["totals"]
        total = user['data']['total']
        map = addPrefix(totals, "₪")

        return format(map, ("Category", "Funds"), ("Total", f"₪{total}"))
