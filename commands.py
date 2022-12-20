def formatRow(maxCatLen, maxPerLen, cat, val):
    return f"| {cat}{' ' * (maxCatLen - len(str(cat)))}| {val}{' ' * (maxPerLen - len(str(val)))}|\n"

def getTitle(maxCatLen, maxPerLen, cat, val):
    edge = "-" * (maxCatLen + maxPerLen + 5)

    return f"{edge}\n{formatRow(maxCatLen, maxPerLen, cat, val)}{edge}\n"

def getSizes(vals):
    catsLength = []
    valueLengths = []

    for (cat, val) in vals:
        catsLength.append(len(str(cat)))
        valueLengths.append(len(str(val)))

    spaces = 4

    categorySize = max(catsLength) + spaces
    valuesSize = max(valueLengths) + spaces

    return (categorySize, valuesSize)

def mapToTupleList(map):
    tuples = []

    for key in map.keys():
        tuples.append((key, map[key]))

    return tuples

def getCommands(id, users, user, args):
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

    map = dict(commands)
    map.update({"Command": "Description"})
    sizes = getSizes(mapToTupleList(map))
    edge = "-" * (sizes[0] + sizes[1] + 5)
    msg = getTitle(sizes[0], sizes[1], "Command", "Description")
    items = commands.items()
    for item in items:
        msg += formatRow(sizes[0], sizes[1], item[0], item[1])
    msg += f"{edge}\n"
    return msg

def getWarning(percentages):
    totalPercent = 0
    for key in percentages:
        totalPercent += float(percentages[key])

    if totalPercent == 100:
        return ""

    msg = f"WARNING! You Have Allocated {totalPercent}% Of Your Funds!\n"

    if totalPercent > 100:
        msg += f"{msg}Please Remove A Category Or Allocate {totalPercent - 100}% Less From Somewhere!\n"
    elif totalPercent < 100:
        msg += f"{msg}Please Add A Category Or Allocate {100 - totalPercent}% More To Somewhere!\n"

    return msg

def printPercentages(id, users, user, args):
    percentages = user["data"]["percentages"]

    msg = getWarning(percentages)

    map = dict(percentages)
    map.update({"Category": "Percentage"})

    sizes = getSizes(mapToTupleList(map))

    edge = "-" * (sizes[0] + sizes[1] + 5)
    msg += getTitle(sizes[0], sizes[1], "Category", "Percentage")
    for key in percentages.keys():
        msg += formatRow(sizes[0], sizes[1], key, f"{percentages[key]}%")
    msg += f"{edge}\n"

    return msg

def printTotals(id, users, user, args):
    totals = user["data"]["totals"]

    map = dict(totals)
    map.update({"Category": "Funds"})

    sizes = getSizes(mapToTupleList(map))
    msg = getTitle(sizes[0], sizes[1], "Category", "Funds")
    for key in totals.keys():
        msg += formatRow(sizes[0], sizes[1], key, f"₪{totals[key]}")
    msg += getTitle(sizes[0], sizes[1], "Total", f"₪{user['data']['total']}")

    return msg

def addMoney(id, users, user, args):
    msg = f"Adding ₪{args[0]}\n"

    percentages = user["data"]["percentages"]
    funds = float(args[0])
    totals = user["data"]["totals"]

    for key in percentages.keys():
        totals.update({f"{key}": totals[key] + funds * (percentages[key] / 100.0)})

    if len(percentages.keys()) == 0:
        msg += "Cannot Add Funds! There Are No Categories!\n"
        return msg

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {"data.totals": totals},
                "$inc": {"data.total": funds}
            }
        )
        msg += f"Successfully Added ₪{funds}!\n"
    except:
        msg += "Failed To Add Funds!\n"

    user = users.find_one({"id": id})
    msg += id, users, user, []

    return msg

def clearBank(id, users, user, args):
    msg = "Clearing Funds\n"

    totals = user["data"]["totals"]

    for key in totals.keys():
        totals.update({f"{key}": 0})

    if len(totals.keys()) == 0:
        msg += "Cannot Clear Funds! There Are No Categories!\n"
        return msg

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {"data.totals": totals, "data.total": 0}
            }
        )

        msg += f"Successfully Cleared Funds!\n"
    except:
        msg += "Failed To Clear Funds!\n"

    user = users.find_one({"id": id})
    msg += printTotals(id, users, user, [])

    return msg

def useMoney(id, users, user, args):
    msg = f"Using ₪{args[1]} From {args[0]}\n"

    category = args[0]
    funds = float(args[1])
    totals = user["data"]["totals"]

    if not category in totals:
        msg += "The Category Doesn't Exist!\n"
        return msg

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

        msg += f"Successfully Used  ₪{funds} From {category}\n"
    except:
        msg += "Failed To Use Funds!\n"

    user = users.find_one({"id": id})
    msg += printTotals(id, users, user, [])

    return msg

def addCategory(id, users, user, args):
    msg = f"Adding Category: {args[0]} And Allocating {args[1]}%\n"

    category = args[0]
    percentage = float(args[1])
    percentages = user["data"]["percentages"]

    if category in percentages.keys():
        msg += "Category Already Exists!\n"
        return msg

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

        msg += "Successfully Added Category!\n"
    except:
        msg += "Failed To Add Category!'\n"

    user = users.find_one({"id": id})
    msg += printPercentages(id, users, user, [])

    return msg

def removeCategory(id, users, user, args):
    msg = f"Removing Category: {args[0]}\n"

    category = args[0]
    percentages = user["data"]["percentages"]

    if not category in percentages.keys():
        msg += "Category Doesn't Exist!\n"
        return msg

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

        msg += "Successfully Removed Category!\n"
    except:
        msg += "Failed To Removed Category!\n"

    user = users.find_one({"id": id})
    msg += printPercentages(id, users, user, [])

    return msg

def addPercentage(id, users, user, args):
    msg = f"Allocating {args[1]}% More To {args[0]}\n"
    category = args[0]
    percentage = float(args[1])
    percentages = user["data"]["percentages"]

    if not category in percentages.keys():
        msg += "Category Doesn't Exist!\n"
        return msg

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {
                    f"data.percentages.{category}": percentages[category] + percentage
                }
            }
        )

        msg += f"Successfully Allocated {percentage}% More To {category}\n"
    except:
        msg += "Failed To Add Percentage!\n"

    user = users.find_one({"id": id})
    msg += printPercentages(id, users, user, [])

    return msg

def removePercentage(id, users, user, args):
    msg = f"Allocating {args[1]}% Less To {args[0]}\n"

    category = args[0]
    percentage = float(args[1])
    percentages = user["data"]["percentages"]

    if not category in percentages.keys():
        msg += "Category Doesn't Exist!\n"
        return msg

    try:
        users.update_one(
            {"id": id},
            {
                "$set": {
                    f"data.percentages.{category}": percentages[category] - percentage
                }
            }
        )

        msg += f"Successfully Allocated {percentage}% Less To {category}\n"
    except:
        msg += "Failed To Remove Percentage!\n"

    user = users.find_one({"id": id})
    msg += printPercentages(id, users, user, [])

    return msg

def redistribute(id, users, user, args):
    msg = "Redistributing Funds!\n"
    percentages = user["data"]["percentages"]
    total = user["data"]["total"]

    totals = dict()

    for key in percentages.keys():
        totals.update({f"data.totals.{key}": total * (percentages[key] / 100.0)})

    if len(percentages.keys()) == 0:
        msg += "Cannot Redistribute Funds! There Are No Categories!\n"
        return msg

    try:
        users.update_one(
            {"id": id},
            {
                "$set": totals
            }
        )

        msg += f"Successfully Redistributed Funds!\n"
    except:
        msg += "Failed To Redistribute Funds!\n"

    user = users.find_one({"id": id})
    msg += printTotals(id, users, user, [])

    return msg

def registerUser(id, users, user, args):
    if user is None:
        msg = f"Registering...\n"
        try:
            users.insert_one({
                "id": id,
                "data": {
                    "percentages": {},
                    "totals": {},
                    "total": 0
                }
            })
            msg += f"Registered Successfully!\n"
        except:
            msg += f"Failed Registering User!\n"
    else:
        msg = f"You Already Have A Bank"

    return msg
