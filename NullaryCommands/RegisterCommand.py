from Command import Command
from DatabaseConnection import DatabaseConnection


class RegisterCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        try:
            dbCon.getUser(userId)
            return "Already Registered!"
        except:
            msg = f"Registering...\n"

            registered = dbCon.registerUser(userId)

            msg += f"Registered Successfully!\n" if registered else f"Failed Registering User!\n"
            return msg
