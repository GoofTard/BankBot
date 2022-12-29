from Command import Command

from DatabaseConnection import DatabaseConnection
from NullaryCommands.FundsCommand import FundsCommand


class AddCommand(Command):
    def execute(self, userId: str, commandLine: list) -> str:
        dbCon = DatabaseConnection.instance()
        user = dbCon.getUser(userId)
        percentages = user["data"]["percentages"]
        funds = float(commandLine[0])
        totals = user["data"]["totals"]
        limits = user["limits"]

        if len(commandLine) > 1:
            msg = f"Adding ₪{funds} To {commandLine[1]}\n"
            category = commandLine[1]

            if category in limits.keys() and totals[category] + funds > limits[category]:
                return f"Cannot Add ₪{funds} To {category}! It Will Go Over Its Limit Of ₪{limits[category]}!"

            totals.update({category: totals[category] + funds})
        else:
            msg = f"Adding ₪{funds}\n"
            overflow = 0
            limitedPercentage = 0
            limitedCatAmount = 0

            for key in percentages.keys():
                categoryFunds = funds * (percentages[key] / 100.0)
                if key in limits.keys() and totals[key] >= limits[key]:
                    overflow = categoryFunds
                    limitedPercentage += percentages[key] / 100.0
                    limitedCatAmount += 1
                elif key in limits.keys() and totals[key] + categoryFunds >= limits[key]:
                    diff = limits[key] - totals[key]
                    overflow = categoryFunds - diff
                    limitedPercentage += percentages[key] / 100.0
                    limitedCatAmount += 1
                    totals.update({key: limits[key]})
                else:
                    totals.update({key: totals[key] + categoryFunds})

            while overflow > 0.1:
                print(overflow)
                percent = limitedPercentage / limitedCatAmount
                limitedPercentage = 0
                limitedCatAmount = 0
                tempOverflow = 0
                for key in percentages.keys():
                    categoryFunds = overflow * percent
                    if key in limits.keys() and totals[key] + categoryFunds == limits[key]:
                        pass
                    if key in limits.keys() and totals[key] + categoryFunds >= limits[key]:
                        diff = limits[key] - totals[key]
                        tempOverflow = categoryFunds - diff
                        limitedPercentage += percentages[key] / 100.0
                        limitedCatAmount += 1
                        totals.update({key: limits[key]})
                    else:
                        totals.update({key: totals[key] + categoryFunds})

                overflow = tempOverflow

            if len(percentages.keys()) == 0:
                msg += "Cannot Add Funds! There Are No Categories!\n"
                return msg

        updated = dbCon.updateUser(
            {
                "$set": {"data.totals": totals},
                "$inc": {"data.total": funds}
            },
            userId
        )

        msg += "Failed To Add Funds!\n" if not updated else \
            (f"Successfully Added ₪{funds} To {commandLine[1]}!\n" if len(commandLine) > 1 else
             f"Successfully Added ₪{funds}!\n")

        msg += FundsCommand().execute(userId, [])

        return msg