assignments = {}

import os
local = os.getenv("LOCALAPPDATA")
DATA_PATH = local + "\\assignments_data.txt"

def load_context() -> None:
    try:
        with open(DATA_PATH) as file:
            data = file.read().split(", ")
            if len(data) < 3: return
            for i in range(len(data) // 3):
                writeAssignment(data[2+i*3], data[i*3], data[i*3+1])
    except OSError:
        print("No assignments")


def saveData() -> None:
    with open(DATA_PATH, "w") as file:
        for month in assignments:
            for day in assignments[month]:
                for name in assignments[month][day]:
                    file.write(month + ", " + day + ", " + name + ", ")


def writeAssignment(name: str, month: str, day: str) -> bool:
    if month not in assignments:
        assignments[month] = {}
    if day not in assignments[month]:
        assignments[month][day] = []
    if name not in assignments[month][day]:
        assignments[month][day] += [name]
        return True
    return False

def sortAssignments(target: dict[dict[int:[]]]) -> dict[dict[int : []]]:
    monthList = []
    result = {}
    for month in target:
        monthList += [int(month)]
    monthList.sort()
    for month in monthList:
        days = {}
        dayList = []
        for day in target[str(month)]:
            dayList += [int(day)]
        dayList.sort()                          # Sort days
        for day in dayList:
            aList = target[str(month)][str(day)]
            aList.sort()                        # Sort assignments
            days[str(day)] = aList
        result[str(month)] = days
    return result


def removeAssignment(name: str, month: str, day: str) -> bool:
    if (month in assignments and
        day in assignments[month] and
        name in assignments[month][day]):
        assignments[month][day].remove(name)
        if assignments[month][day] == []:
            assignments[month].pop(day)
        if assignments[month] == {}:
            assignments.pop(month)
        return True
    return False

def displayAssignments() -> None:
    if assignments == {}:
        print("No assignments!")
    for month in assignments:
        print(("" if int(month) > 9 else "0") + month + " ______")
        for day in assignments[month]:
            print(("   " if int(day) > 9 else "   0") + day)
            for name in assignments[month][day]:
                print("     [] " + name)


def processInput() -> bool:
    value = input("Command (Enter 'help' for options): ")
    inputs = value.split(" ")
    if len(inputs) == 4:
        if inputs[0] == "add":
            if 1 <= int(inputs[2]) <= 12 and 1 <= int(inputs[3]) <= 31:
                if writeAssignment(inputs[1], str(int(inputs[2])), str(int(inputs[3]))):
                    print("Assignment added")
                else:
                    print("Assignment with name", inputs[1], "already exists")
            else:
                print("Invalid date")
        elif inputs[0] == "remove":
            name = inputs[1]
            month = inputs[2]
            day = inputs[3]
            if 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
                if removeAssignment(name, month, day):
                    print("Removed", name)
                else:
                    print("No assignment named '" + name + "' exists")
            else:
                print("Invalid date")
    elif len(inputs) == 1:
        if inputs[0] == "display":
            displayAssignments()
        elif inputs[0] == "help":
            print("-'add [name] [MM] [DD]': Add assignment to track",
                  "\n-'remove [name] [MM] [DD]': Remove tracked assignment",
                  "\n-'display': Display tracked assignments",
                  "\n-Press 'Enter': Quit Assignment Tracker")
        elif inputs[0] == "":
            confirmation = input("Exit? (Press 'Enter' again to exit)")
            if confirmation == "":
                return False
    return True

print("== Assignment Tracker v1.0 ==")
load_context()
assignments = sortAssignments(assignments)
displayAssignments()
while(processInput()):
    assignments = sortAssignments(assignments)
    saveData()
    pass
saveData()
