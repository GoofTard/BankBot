spaces = 1

def formatRow(sizes, values):
    return f"| {values[0]}{' ' * (sizes[0] - len(str(values[0])))}| {values[1]}{' ' * (sizes[1] - len(str(values[1])))} |\n"

def formatRowExtended(sizes, values):
    row = ""
    for index in range(len(sizes)):
        row += f"| {values[index]}{' ' * (sizes[index] - len(str(values[index])))} "
    row += " |\n"

    return row

def getTitle(sizes, values):
    edge = "-" * (sizes[0] + sizes[1] + spaces + 5)

    return f"{edge}\n{formatRow(sizes, values)}{edge}\n"

def getTitleExtended(sizes, values):
    space = 1
    count = 0
    for size in sizes:
        count += size
    count += 2 * len(sizes) + space * len(sizes) + 2
    edge = "-" * count

    return f"{edge}\n{formatRowExtended(sizes, values)}{edge}\n"

def getSizes(vals):
    catsLength = []
    valueLengths = []

    for (cat, val) in vals:
        catsLength.append(len(str(cat)))
        valueLengths.append(len(str(val)))

    categorySize = max(catsLength) + spaces
    valuesSize = max(valueLengths) + spaces

    return (categorySize, valuesSize)

def getSizesExtended(vals, amount):
    sizes = []
    for col in range(amount):
        sizes.append([])

    for val in vals:
        for col in range(amount):
            sizes[col].append(len(str(val[col])))

    maxes = []
    for col in range(amount):
        maxes.append(max(sizes[col]))

    return maxes


def mapToTupleList(map):
    tuples = []

    for key in map.keys():
        tuples.append((key, map[key]))

    return tuples

def addPrefix(map: dict, prefix: str) -> dict:
    newMap = dict(map)
    for key in newMap.keys():
        newMap.update({key: f"{prefix}{newMap[key]}"})
    return newMap

def addPrefixExtended(list: list, prefix: str):
    for index in range(len(list)):
       list[index] = f"{prefix}{list[index]}"

def addPostfixExtended(list: list, postfix: str):
    for index in range(len(list)):
        list[index] = f"{list[index]}{postfix}"

def addPostfix(map: dict, postfix: str) -> dict:
    newMap = dict(map)
    for key in newMap.keys():
        newMap.update({key: f"{newMap[key]}{postfix}"})
    return newMap

def getWarning(percentages):
    totalPercent = 0
    for key in percentages.keys():
        totalPercent += float(percentages[key])

    if totalPercent == 100:
        return ""

    msg = f"WARNING! You Have Allocated {totalPercent}% Of Your Funds!\n"

    if totalPercent > 100:
        msg += f"{msg}Please Remove A Category Or Allocate {totalPercent - 100}% Less From Somewhere!\n"
    elif totalPercent < 100:
        msg += f"{msg}Please Add A Category Or Allocate {100 - totalPercent}% More To Somewhere!\n"

    return msg

def format(map: dict, upperTitle: tuple, lowerTitle: tuple = None) -> str:
    mapWithTitle = dict(map)
    mapWithTitle.update({upperTitle[0]: upperTitle[1]})

    if not lowerTitle is None:
            mapWithTitle.update({lowerTitle[0]: lowerTitle[1]})

    if len(map.keys()) == 0:
        map.update({"": ""})

    sizes = getSizes(mapToTupleList(mapWithTitle))

    msg = getTitle(sizes, upperTitle)
    for key in map.keys():
        msg += formatRow(sizes, (key, map[key]))

    if not lowerTitle is None:
        msg += getTitle(sizes, lowerTitle)
    else:
        msg += ("-" * (sizes[0] + sizes[1] + spaces + 5))

    return msg

def formatExtended(columns: int, items: list, upperTitle: list, lowerTitle: list = None) -> str:
    values = []
    for item in items:
        values.append(list(item))
    values.append(upperTitle)
    if not lowerTitle is None:
        values.append(lowerTitle)
    space = []
    for col in range(columns):
        space.append("")
    values.append(space)

    if len(items) == 0:
        values.append(["", ""])

    sizes = getSizesExtended(values, columns)
    msg = getTitleExtended(sizes, upperTitle)
    for val in items:
        msg += formatRowExtended(sizes, val)

    if not lowerTitle is None:
        msg += getTitleExtended(sizes, lowerTitle)
    else:
        space = 1
        count = 0
        for size in sizes:
            count += size
        count += 2 * len(sizes) + space * len(sizes) + 2
        msg += f"{'-' * count}\n"

    return msg
