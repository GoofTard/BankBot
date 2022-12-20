async def sendCommands(id, users, user, channel, args):
    commands = {
        "percentages": "Shows all percentages",
        "totals": "Shows all totals",
        "add": "Format: add 'amount', adds amount to total funds",
        "clear": "Clears funds",
        "use": "Format: use 'category' 'amount', uses amount from category",
        "add-cat": "Format: add-cat 'category' 'percentage', adds category and allocate percentage",
        "rem-cat": "Format: add-cat 'category', removes category",
        "add-percent": "Format: add-percent 'category' 'percentage', adds percentage to category",
        "rem-percent": "Format: rem-percent 'category' 'percentage', removes percentage from category",
        "rides": "Redistribute funds",
        "register": "Register a user"
    }
    msg = ""
    items = commands.items()

    for item in items:
        msg += f"{item[0]}: {item[1]}\n"

    await channel.send(msg)

async def sendWarning(channel, percentages):
    totalPercent = 0
    for key in percentages:
        totalPercent += float(percentages[key])

    if totalPercent == 100:
        return;

    msg = f"WARNING! You Have Allocated {totalPercent}% Of Your Funds!\n"

    if totalPercent > 100:
        await channel.send(f"{msg}Please Remove A Category Or Allocate {totalPercent - 100}% Less From Somewhere!")
    elif totalPercent < 100:
        await channel.send(f"{msg}Please Add A Category Or Allocate {100 - totalPercent}% More To Somewhere!")

def formatRow(maxCatLen, maxPerLen, cat, per):
    return f"| {cat}{' ' * (maxCatLen - len(str(cat)))}| {per}{' ' * (maxPerLen - len(str(per)))}|\n"

async def printPercentages(id, users, user, channel, args):
    percentages = user["data"]["percentages"]

    await sendWarning(channel, percentages)

    categoryLengths = [len("Category")]
    valueLengths = [len("Percentage")]

    for key in percentages.keys():
        categoryLengths.append(len(key))
        valueLengths.append(len(str(percentages[key])))

    spaces = 4

    categorySize = max(categoryLengths) + spaces
    valuesSize = max(valueLengths) + spaces
    edge = "-" * (categorySize + valuesSize + 5)
    msg = "```\n"
    msg += f"{edge}\n"
    msg += formatRow(categorySize, valuesSize, "Category", "Percentage")
    for key in percentages.keys():
        msg += formatRow(categorySize, valuesSize, key, percentages[key])
    msg += f"{edge}\n"
    msg += "```"

    await channel.send(msg)

async def printTotals(id, users, user, channel, args):
    totals = user["data"]["totals"]

    msg = "Totals:\n"
    for key in totals.keys():
        msg += f"{key}: ₪{totals[key]}\n"
    msg += f"-------------\nTotal: ₪{user['data']['total']}\n"

    await channel.send(msg)


async def addMoney(id, users, user, channel, args):
    await channel.send(f"Adding ₪{args[0]}")

    percentages = user["data"]["percentages"]
    funds = float(args[0])
    totals = user["data"]["totals"]

    for key in percentages.keys():
        totals.update({f"{key}": totals[key] + funds * (percentages[key] / 100.0)})

    if len(percentages.keys()) == 0:
        await channel.send("Cannot Add Funds! There Are No Categories!")

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {"data.totals": totals},
                "$inc": {"data.total": funds}
            }
        )
        await channel.send(f"Successfully Added ₪{funds}!")
    except:
        await channel.send("Failed To Add Funds!")

    user = users.find_one({"id": id})
    await printTotals(id, users, user, channel, [])


async def clearBank(id, users, user, channel, args):
    await channel.send("Clearing Funds")

    totals = user["data"]["totals"]

    for key in totals.keys():
        totals.update({f"{key}": 0})

    if len(totals.keys()) == 0:
        await channel.send("Cannot Clear Funds! There Are No Categories!")

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {"data.totals": totals, "data.total": 0}
            }
        )

        await channel.send(f"Successfully Cleared Funds!")
    except:
        await channel.send("Failed To Clear Funds!")

    user = users.find_one({"id": id})
    await printTotals(id, users, user, channel, [])


async def useMoney(id, users, user, channel, args):
    await channel.send(f"Using ₪{args[1]} From {args[0]}")

    category = args[0]
    funds = float(args[1])
    totals = user["data"]["totals"]

    if not category in totals:
        await channel.send("The Category Doesn't Exist!")
        return

    totals.update({category: totals[category] - funds})

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {
                    "data.totals": totals,
                    "data.total": user["data"]["total"] - funds
                },
            }
        )

        await channel.send(f"Successfully Used  ₪{funds} From {category}")
    except:
        await channel.send("Failed To Use Funds!")

    user = users.find_one({"id": id})
    await printTotals(id, users, user, channel, [])


async def addCategory(id, users, user, channel, args):
    await channel.send(f"Adding Category: {args[0]} And Allocating {args[1]}%")

    category = args[0]
    percentage = float(args[1])
    percentages = user["data"]["percentages"]

    if category in percentages.keys():
        await channel.send("Category Already Exists!")
        return

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {
                    f"data.percentages.{category}": percentage,
                    f"data.totals.{category}": 0
                }
            }
        )

        await channel.send("Successfully Added Category!")
    except:
        await channel.send("Failed To Add Category!")

    user = users.find_one({"id": id})
    await printPercentages(id, users, user, channel, [])


async def removeCategory(id, users, user, channel, args):
    await channel.send(f"Removing Category: {args[0]}")

    category = args[0]
    percentages = user["data"]["percentages"]

    if not category in percentages.keys():
        await channel.send("Category Doesn't Exist!")
        return

    try:
        users.update_one(
            {"id": id},
            {
                "$unset": {
                    f"data.percentages.{category}": 1,
                    f"data.totals.{category}": 1
                }
            }
        )

        await channel.send("Successfully Removed Category!")
    except:
        await channel.send("Failed To Removed Category!")

    user = users.find_one({"id": id})
    await printPercentages(id, users, user, channel, [])


async def addPercentage(id, users, user, channel, args):
    await channel.send(f"Allocating {args[1]}% More To {args[0]}")
    category = args[0]
    percentage = float(args[1])
    percentages = user["data"]["percentages"]

    if not category in percentages.keys():
        await channel.send("Category Doesn't Exist!")
        return

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {
                    f"data.percentages.{category}": percentages[category] + percentage
                }
            }
        )

        await channel.send(f"Successfully Allocated {percentage}% More To {category}")
    except:
        await channel.send("Failed To Add Percentage!")

    user = users.find_one({"id": id})
    await printPercentages(id, users, user, channel, [])


async def removePercentage(id, users, user, channel, args):
    await channel.send(f"Allocating {args[1]}% Less To {args[0]}")

    category = args[0]
    percentage = float(args[1])
    percentages = user["data"]["percentages"]

    if not category in percentages.keys():
        await channel.send("Category Doesn't Exist!")
        return

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {
                    f"data.percentages.{category}": percentages[category] - percentage
                }
            }
        )

        await channel.send(f"Successfully Allocated {percentage}% Less To {category}")
    except:
        await channel.send("Failed To Remove Percentage!")

    user = users.find_one({"id": id})
    await printPercentages(id, users, user, channel, [])


async def redistribute(id, users, user, channel, args):
    await channel.send("Redistributing Funds!")
    percentages = user["data"]["percentages"]
    total = user["data"]["total"]

    totals = dict()

    for key in percentages.keys():
        totals.update({f"data.totals.{key}": total * (percentages[key] / 100.0)})

    if len(percentages.keys()) == 0:
        await channel.send("Cannot Redistribute Funds! There Are No Categories!")

    try:
        users.update_one(
            {"id": id},
            {
                "$set": totals
            }
        )

        await channel.send(f"Successfully Redistributed Funds!")
    except:
        await channel.send("Failed To Redistribute Funds!")

    user = users.find_one({"id": id})
    await printTotals(id, users, user, channel, [])


async def registerUser(id, users, user, channel, args):
    if user is None:
        await channel.send(f"Registering...")
        try:
            users.insert_one({
                "id": id,
                "data": {
                    "percentages": {},
                    "totals": {},
                    "total": 0
                }
            })
            await channel.send(f"Registered Successfully!")
        except:
            await channel.send(f"Failed Registering User!")
    else:
        await channel.send(f"You Already Have A Bank")
