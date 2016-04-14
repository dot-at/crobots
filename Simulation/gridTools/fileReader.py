import glob
import json
from enum import Enum

class Route:
    def __init__(self, lotSize, lotLayout, instructionsArray):
        self.lotSize = lotSize
        self.lotLayout  = lotLayout
        self.instructionsArray = instructionsArray

# Grid with 4 properties
# onNode - what kind of car is on the grid
# ndStat - What is robot doing? Is it moving, is it ready, is it moving with car etc.
# rVertical - is robot moving vertically (lifting the car up or dropping it)
# rMove - is the machine(s) on the grid moving.

class GridState:
    def __init__(self, onNode, ndStat, rVertical, rMove):
        self.onNode = onNode
        self.ndStat = ndStat
        self.rVertical = rVertical
        self.rMove = rMove

# Different onNode states
# onNode - what kind of car is on the grid
class onNode(Enum):
    em = 0
    C0 = 1
    C1 = 2
    C2 = 3
    NO = 4

# Different ndStat states
# ndStat - What is robot doing? Is it moving, is it ready, is it moving with car etc.
class ndStat(Enum):
    none = 0
    R_r = 1
    R_m = 2
    R_v = 3
    C0R_r = 4
    C0R_m = 5
    C1R_r = 6
    C1R_m = 7
    C2R_r = 8
    C2R_m = 9
    NO = 10

# Different rVertical states
# rVertical - is robot moving vertically (lifting the car up or dropping it)
class rVertical(Enum):
    lift = 0
    l1 = 1
    l2 = 2
    l3 = 3
    l4 = 4
    drop = 5
    NO = 6

# Different rMove states
# rMove - is the machine(s) on the grid moving.
class rMove(Enum):
    accE = 0
    mvE0 = 1
    accN = 2
    mvN1 = 3
    mvN0 = 4
    accW = 5
    mvW0 = 6
    accS = 7
    mvS1 = 8
    mvS0 = 9
    w0_accE = 10
    w0_mvE1 = 11
    w0_mvE0 = 12
    w0_accN = 13
    w0_mvN1 = 14
    w0_mvN2 = 15
    w0_mvN3 = 16
    w0_mvN0 = 17
    w0_accW = 18
    w0_mvW1 = 19
    w0_mvW0 = 20
    w0_accS = 21
    w0_mvS1 = 22
    w0_mvS2 = 23
    w0_mvS3 = 24
    w0_mvS0 = 25
    w1_accE = 26
    w1_mvE1 = 27
    w1_mvE0 = 28
    w1_accN = 29
    w1_mvN1 = 30
    w1_mvN2 = 31
    w1_mvN3 = 32
    w1_mvN0 = 33
    w1_accW = 34
    w1_mvW1 = 35
    w1_mvW0 = 36
    w1_accS = 37
    w1_mvS1 = 38
    w1_mvS2 = 39
    w1_mvS3 = 40
    w1_mvS0 = 41
    w2_accE = 42
    w2_mvE1 = 43
    w2_mvE0 = 44
    w2_accN = 45
    w2_mvN1 = 46
    w2_mvN2 = 47
    w2_mvN3 = 48
    w2_mvN0 = 49
    w2_accW = 50
    w2_mvW1 = 51
    w2_mvW0 = 52
    w2_accS = 53
    w2_mvS1 = 54
    w2_mvS2 = 55
    w2_mvS3 = 56
    w2_mvS0 = 57
    NO = 58

# Different pieces of grid
# noWall - robot can drive from this grid to every direction
# wall* - robot cannot drive to direction *
class gridPieces(Enum):
    wallNW = 0
    wallN = 1
    wallNE = 2
    wallE = 3
    wallSE = 4
    wallS = 5
    wallSW = 6
    wallW = 7
    noWall = 8

# getParkingLot takes the size of the lot and the layout string from the file and will convert it to two-dimensional
# table that will later be used to track the machines' movement.
def getParkingLot(lotSize, layoutString):
    layouts = [layoutString[i:i+lotSize[1]] for i in range(0, len(layoutString), lotSize[1])]
    decodedLevels = []
    for level in layouts:
        decodedLevel = []
        for char in level:
            if char == 'D':
                decodedLevel.append(gridPieces(0))
            elif char == 'H':
                decodedLevel.append(gridPieces(1))
            elif char == 'G':
                decodedLevel.append(gridPieces(2))
            elif char == 'O':
                decodedLevel.append(gridPieces(3))
            elif char == 'M':
                decodedLevel.append(gridPieces(4))
            elif char == 'N':
                decodedLevel.append(gridPieces(5))
            elif char == 'J':
                decodedLevel.append(gridPieces(6))
            elif char == 'L':
                decodedLevel.append(gridPieces(7))
            elif char == 'P':
                decodedLevel.append(gridPieces(8))
            else:
                print("Character " + char + " not in library!!!")
        decodedLevels.append(decodedLevel)
    return decodedLevels

# getRoute will get the file name of the .robroute (parking lot instruction set) as an input
# As an output Route class object will be returned that is the basis for all the movements.
def getRoute(filename):
    with open(filename, "r") as input:
        array = []
        for line in input:
            array.append(line)

    lotSize = list(map(int, array[4].rstrip().split(" ")))
    parkingLotLayout = getParkingLot(lotSize,array[5].rstrip())
    instructionsLength = int(array[6])
    instructionsArray  = array[7:(instructionsLength + 7)]
    decodedInstructions = []
    for instrLines in instructionsArray:
        decodedInstructions.append(gridStates(instrLines.rstrip()))
    return Route(lotSize, parkingLotLayout, decodedInstructions)

# decodeGrid will decode one piece of parking layout and will return the states and other values of that grid as a
# GridState object.
def decodeGrid(grid):
    onNodeValue = onNode(ord(grid[0]) - ord('c'))
    ndStatValue = ndStat(ord(grid[1]) - ord('A'))
    if (ndStatValue == ndStat.none):
        ndStatValue = ndStat.NO
    rVerticalValue = rVertical(ord(grid[2]) - ord('v'))
    rMoveValue = rMove(ord(grid[3]) - ord('!'))
    return GridState(onNodeValue, ndStatValue, rVerticalValue, rMoveValue)

# gridStates is a helper function that takes the instruction string from the file as an input and will return instructions
# as an array of GridState objects.
def gridStates (instructionString):
    instructions = [instructionString[i:i+4] for i in range(0, len(instructionString), 4)]
    instructionsDecoded = []
    for instr in instructions:
        instructionsDecoded.append(decodeGrid(instr))
    return instructionsDecoded


# getCoordinates takes the route object as an input and will return the coordinates of all the machines on one instruction
# level as an array of arrays.
def getCoordinates(route, level, instructionsMaker = False):
    instructions = route.instructionsArray[level]
    locationArray = []
    lotWidth = route.lotSize[1]
    carID = 0
    robotID = 0

    for i in range(0, len(instructions)):
        if (instructions[i].onNode == onNode.C0 or instructions[i].onNode == onNode.C1 or instructions[i].onNode == onNode.C2 or
            instructions[i].ndStat == ndStat.C0R_r or instructions[i].ndStat == ndStat.C0R_m or
            instructions[i].ndStat == ndStat.C1R_r or instructions[i].ndStat == ndStat.C1R_m or
            instructions[i].ndStat == ndStat.C2R_r or instructions[i].ndStat == ndStat.C2R_m):

            placeStr = str(i)
            if len(placeStr) == 1:
                level = 0
                place = i
            else:
                level = int(placeStr[0])
                place = int(placeStr[1])

            if instructionsMaker == True:
                locationArray.append([instructions[i].onNode.name, level, place, "C" + str(carID),instructions[i]])
            else:
                locationArray.append([instructions[i].onNode.name, level, place, "C" + str(carID)])
            carID += 1

        if (instructions[i].ndStat != ndStat.none and instructions[i].ndStat != ndStat.NO):
            placeStr = str(i)
            if len(placeStr) == 1:
                level = 0
                place = i
            else:
                level = int(placeStr[0])
                place = int(placeStr[1])

            if instructionsMaker == True:
                locationArray.append(["R", level, place, "R" + str(robotID), instructions[i]])
            else:
                locationArray.append(["R", level, place, "R" + str(robotID)])

            robotID += 1
    return locationArray

# getParkingLayout will return the layout and the initial machine positioning as a JSON object - used by client.
def getParkingLayout(route):
    lotWidth = route.lotSize[1]
    lotHeight = route.lotSize[0]
    layoutArray = []
    machineArray = getCoordinates(route, 0)

    for i in range(0, lotHeight):
        level = []
        for j in range(0, lotWidth):
            level.append("P")
        layoutArray.append(level)
    return (json.dumps({'width' : lotWidth, 'height' : lotHeight, 'layout' : layoutArray, 'machines' : machineArray}, separators=(',',':')))

# returns list of routes (.robroute files in Examples directory)
def getRouteList():
    routes = glob.glob("../Examples/*.robroute")
    return routes

# returns the list of routes as a JSON objects
def getJSONRouteList():
    routes = getRouteList()
    routeArray = []
    for i in range(0, len(routes)):
        routeArray.append({'name' : "Route " + str(i+1), 'value' : str(i)})
    return (json.dumps(routeArray, separators=(',',':')))

# Crucial part of the program - getInstructions will transform the instructions from file to implicit instructions
# where a machine will be given ID and a list of instructions  - for example C1 (car ID 1), 'W', 2 would mean that
# car object with ID 1 should at this step move west with the speed of 2 (number means how many steps it takes to move
# from a grid to adjacent grid.
def getInstructions(route):
    initialMachines = getCoordinates(route,0,True)
    instructionsArray = []
    for i in range(0, len(route.instructionsArray)):
        instructionsArray.append([])
    for machine in initialMachines:
        y = machine[1]
        x = machine[2]
        id = machine[3]
        state = machine[4]
        type = 'C'
        if machine[0] == 'R':
            type = 'R'
        for i in range(1,len(route.instructionsArray)):
            nextState = getCoordinates(route, i, True)
            if type == 'R':
                if state.rMove != rMove.NO:
                    if state.rMove == rMove.mvW0 or state.rMove == rMove.accW:
                        instructionsArray[i].append([id,'W',1])
                        #print("West")
                        x -= 1
                    elif state.rMove == rMove.mvE0 or state.rMove == rMove.accE:
                        instructionsArray[i].append([id,'E',1])
                        #print("East")
                        x += 1
                    elif state.rMove == rMove.mvN1:
                        #print("North")
                        y += 1
                    elif state.rMove == rMove.mvS1:
                        #print("South")
                        y -= 1
                    elif state.rMove == rMove.w0_mvN3 or state.rMove == rMove.w1_mvN3 or state.rMove == rMove.w2_mvN3:
                        #print("North w/ car")
                        y += 1
                    elif state.rMove == rMove.w0_mvS3 or state.rMove == rMove.w1_mvS3 or state.rMove == rMove.w2_mvS3:
                        #print("South w/ car")
                        y -= 1
                    elif state.rMove == rMove.w0_mvE1 or state.rMove == rMove.w1_mvE1 or state.rMove == rMove.w2_mvE1:
                        #print("East w/ car")
                        x += 1
                    elif state.rMove == rMove.w0_mvW1 or state.rMove == rMove.w1_mvW1 or state.rMove == rMove.w2_mvW1:
                        #print("West w/ car")
                        x -= 1

                    if state.rMove == rMove.accN or state.rMove == rMove.mvN1 or state.rMove == rMove.mvN0:
                        instructionsArray[i].append([id,'N',2])
                    elif state.rMove == rMove.accS or state.rMove == rMove.mvS1 or state.rMove == rMove.mvS0:
                        instructionsArray[i].append([id,'S',2])
                    elif state.rMove == rMove.w0_mvN0 or state.rMove == rMove.w0_mvN1 or state.rMove == rMove.w0_mvN2 or state.rMove == rMove.w0_mvN3 or \
                        state.rMove == rMove.w1_mvN0 or state.rMove == rMove.w1_mvN1 or state.rMove == rMove.w1_mvN2 or state.rMove == rMove.w1_mvN3 or \
                        state.rMove == rMove.w2_mvN0 or state.rMove == rMove.w2_mvN1 or state.rMove == rMove.w2_mvN2 or state.rMove == rMove.w2_mvN3 or \
                        state.rMove == rMove.w0_accN or state.rMove == rMove.w1_accN or state.rMove == rMove.w1_accN:
                        instructionsArray[i].append([id,'N',4])
                    elif state.rMove == rMove.w0_mvS0 or state.rMove == rMove.w0_mvS1 or state.rMove == rMove.w0_mvS2 or state.rMove == rMove.w0_mvS3 or \
                        state.rMove == rMove.w1_mvS0 or state.rMove == rMove.w1_mvS1 or state.rMove == rMove.w1_mvS2 or state.rMove == rMove.w1_mvS3 or \
                        state.rMove == rMove.w2_mvS0 or state.rMove == rMove.w2_mvS1 or state.rMove == rMove.w2_mvS2 or state.rMove == rMove.w2_mvS3 or \
                        state.rMove == rMove.w0_accS or state.rMove == rMove.w1_accS or state.rMove == rMove.w1_accS:
                        instructionsArray[i].append([id,'S',4])
                    elif state.rMove == rMove.w0_accE or state.rMove == rMove.w0_mvE0 or state.rMove == rMove.w0_mvE1 or \
                        state.rMove == rMove.w1_accE or state.rMove == rMove.w1_mvE0 or state.rMove == rMove.w1_mvE1 or \
                        state.rMove == rMove.w2_accE or state.rMove == rMove.w2_mvE0 or state.rMove == rMove.w2_mvE1:
                        instructionsArray[i].append([id,'E',2])
                    elif state.rMove == rMove.w0_accW or state.rMove == rMove.w0_mvW0 or state.rMove == rMove.w0_mvW1 or \
                        state.rMove == rMove.w1_accW or state.rMove == rMove.w1_mvW0 or state.rMove == rMove.w1_mvW1 or \
                        state.rMove == rMove.w2_accW or state.rMove == rMove.w2_mvW0 or state.rMove == rMove.w2_mvW1:
                        instructionsArray[i].append([id,'W',2])

                else:
                    if state.rVertical != rVertical.NO:
                        if state.rVertical == rVertical.lift:
                            instructionsArray[i].append([id,'L',0])
                            #print("Starting to lift")
                        elif state.rVertical == rVertical.l1:
                            instructionsArray[i].append([id,'L',1])
                            #print("Lift level 1")
                        elif state.rVertical == rVertical.l2:
                            instructionsArray[i].append([id,'L',2])
                            #print("Lift level 2")
                        elif state.rVertical == rVertical.l3:
                            instructionsArray[i].append([id,'L',3])
                            #print("Lift level 3")
                        elif state.rVertical == rVertical.l4:
                            instructionsArray[i].append([id,'L',4])
                           #print("Lift level 4")
                        elif state.rVertical == rVertical.drop:
                            instructionsArray[i].append([id,'D',0])
                            #print("Dropping car")
            else:
                if state.rMove != rMove.NO:
                    if state.rMove == rMove.w0_mvN3 or state.rMove == rMove.w1_mvN3 or state.rMove == rMove.w2_mvN3:
                        #print("North w/ car")
                        y += 1
                    elif state.rMove == rMove.w0_mvS3 or state.rMove == rMove.w1_mvS3 or state.rMove == rMove.w2_mvS3:
                        #print("South w/ car")
                        y -= 1
                    elif state.rMove == rMove.w0_mvE1 or state.rMove == rMove.w1_mvE1 or state.rMove == rMove.w2_mvE1:
                        #print("East w/ car")
                        x += 1
                    elif state.rMove == rMove.w0_mvW1 or state.rMove == rMove.w1_mvW1 or state.rMove == rMove.w2_mvW1:
                        #print("West w/ car")
                        x -= 1

                    if state.rMove == rMove.w0_mvN0 or state.rMove == rMove.w0_mvN1 or state.rMove == rMove.w0_mvN2 or state.rMove == rMove.w0_mvN3 or \
                        state.rMove == rMove.w1_mvN0 or state.rMove == rMove.w1_mvN1 or state.rMove == rMove.w1_mvN2 or state.rMove == rMove.w1_mvN3 or \
                        state.rMove == rMove.w2_mvN0 or state.rMove == rMove.w2_mvN1 or state.rMove == rMove.w2_mvN2 or state.rMove == rMove.w2_mvN3 or \
                        state.rMove == rMove.w0_accN or state.rMove == rMove.w1_accN or state.rMove == rMove.w1_accN:
                        instructionsArray[i].append([id,'N',4])
                    elif state.rMove == rMove.w0_mvS0 or state.rMove == rMove.w0_mvS1 or state.rMove == rMove.w0_mvS2 or state.rMove == rMove.w0_mvS3 or \
                        state.rMove == rMove.w1_mvS0 or state.rMove == rMove.w1_mvS1 or state.rMove == rMove.w1_mvS2 or state.rMove == rMove.w1_mvS3 or \
                        state.rMove == rMove.w2_mvS0 or state.rMove == rMove.w2_mvS1 or state.rMove == rMove.w2_mvS2 or state.rMove == rMove.w2_mvS3 or \
                        state.rMove == rMove.w0_accS or state.rMove == rMove.w1_accS or state.rMove == rMove.w1_accS:
                        instructionsArray[i].append([id,'S',4])
                    elif state.rMove == rMove.w0_accE or state.rMove == rMove.w0_mvE0 or state.rMove == rMove.w0_mvE1 or \
                        state.rMove == rMove.w1_accE or state.rMove == rMove.w1_mvE0 or state.rMove == rMove.w1_mvE1 or \
                        state.rMove == rMove.w2_accE or state.rMove == rMove.w2_mvE0 or state.rMove == rMove.w2_mvE1:
                        instructionsArray[i].append([id,'E',2])
                    elif state.rMove == rMove.w0_accW or state.rMove == rMove.w0_mvW0 or state.rMove == rMove.w0_mvW1 or \
                        state.rMove == rMove.w1_accW or state.rMove == rMove.w1_mvW0 or state.rMove == rMove.w1_mvW1 or \
                        state.rMove == rMove.w2_accW or state.rMove == rMove.w2_mvW0 or state.rMove == rMove.w2_mvW1:
                        instructionsArray[i].append([id,'W',2])

            stateHolder = getMachineState(nextState,y,x,type)
            if stateHolder != None:
                state = stateHolder
            else:
                print ("!!!No state found!!!")

    return (json.dumps(instructionsArray, separators=(',',':')))



#  Will return the state of the machine that is on grid coordinates x,y. Helper function for getCoordinates().
def getMachineState(machines, x, y, type):
   for machine in machines:
        if machine[1] == x and machine[2] == y:
            if type == 'C' and machine[0] != 'R':
                return machine[4]
            elif type == 'R' and machine[0] == 'R':
                return machine[4]

# Helper function for debugging, will return human readable instructions
def printGrid(route, level):
    instructions = route.instructionsArray[level]
    parkingLotString = ""
    for i in range(0, route.lotSize[0]):
        instr = ""
        for j in range(0, route.lotSize[1]):
            instr += "|"
            instr += instructions[i * 10 + j].onNode.name
            instr += "|"
            instr += instructions[i * 10 + j].ndStat.name
            instr += "|"
            instr += instructions[i * 10 + j].rVertical.name
            instr += "|"
            instr += instructions[i * 10 + j].rMove.name
            instr += "\t"
        instr += "\n"
        parkingLotString += instr
    parkingLotString += "\n\n"
    return (parkingLotString)

# writes abovementioned instructions to a file
def writeInstructions(route):
    f = open('instructions.txt', 'w')
    for i in range(0, len(route.instructionsArray)):
        f.write(printGrid(route, i))
    f.close()

#route = getRoute(getRouteList()[0])

#getInstructions(route)

