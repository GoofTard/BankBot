spaces = 4

def formatRow(sizes, values):
    return f"| {values[0]}{' ' * (sizes[0] - len(str(values[0])))}| {values[1]}{' ' * (sizes[1] - len(str(values[1])))}|\n"

def getTitle(sizes, values):
    edge = "-" * (sizes[0] + sizes[1] + spaces + 1)

    return f"{edge}\n{formatRow(sizes, values)}{edge}\n"

def getSizes(vals):
    catsLength = []
    valueLengths = []

    for (cat, val) in vals:
        catsLength.append(len(str(cat)))
        valueLengths.append(len(str(val)))

    categorySize = max(catsLength) + spaces
    valuesSize = max(valueLengths) + spaces

    return (categorySize, valuesSize)

def mapToTupleList(map):
    tuples = []

    for key in map.keys():
        tuples.append((key, map[key]))

    return tuples

def addPrefix(map: dict, prefix: str) -> dict:
    newMap = dict(map)
    for key in newMap.keys():
        newMap.update({key: prefix + newMap[key]})
    return newMap

def addPostfix(map: dict, postfix: str) -> dict:
    newMap = dict(map)
    for key in newMap.keys():
        newMap.update({key: newMap[key] + postfix})
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

    sizes = getSizes(mapToTupleList(mapWithTitle))

    msg = getTitle(sizes, upperTitle)
    for key in map.keys():
        msg += formatRow(sizes, (key, map[key]))

    if not lowerTitle is None:
        msg += getTitle(sizes, lowerTitle)
    else:
        msg += ("-" * (sizes[0] + sizes[1] + spaces + 1))

    return msg