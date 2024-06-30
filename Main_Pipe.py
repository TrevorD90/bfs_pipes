import re

pipeOpeningsMap = {
    '═': {'left': True, 'right': True, 'up': False, 'down': False},
    '║': {'left': False, 'right': False, 'up': True, 'down': True},
    '╔': {'left': False, 'right': True, 'up': False, 'down': True},
    '╗': {'left': True, 'right': False, 'up': False, 'down': True},
    '╚': {'left': False, 'right': True, 'up': True, 'down': False},
    '╝': {'left': True, 'right': False, 'up': True, 'down': False},
    '╠': {'left': False, 'right': True, 'up': True, 'down': True},
    '╣': {'left': True, 'right': False, 'up': True, 'down': True},
    '╦': {'left': True, 'right': True, 'up': False, 'down': True},
    '╩': {'left': True, 'right': True, 'up': True, 'down': False},
    '*': {'left': True, 'right': True, 'up': True, 'down': True},
}

def getNeighbors(coord,listOfDirections, grid):
    if listOfDirections is None:
        return []
    listOfNeighbors = []
    for neighbor in listOfDirections:
        x = coord[0] + neighbor[0]
        y = coord[1] + neighbor[1]
        if (x,y) in grid:
            listOfNeighbors.append((x,y))

    return listOfNeighbors


def getDirectionsFromPipe(pipe):
    if pipe not in pipeOpeningsMap:
        return []  # Return empty list if coord doesn't exist in pipeOpeningsMap

    directions = pipeOpeningsMap[pipe]
    result = []

    if directions['left']:
        result.append((-1, 0))  # Move left
    if directions['right']:
        result.append((1, 0))   # Move right
    if directions['up']:
        result.append((0, -1))  # Move up
    if directions['down']:
        result.append((0, 1))   # Move down

    return result

def createGrid(filePath):
    grid = {}
    with open(filePath, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            char = parts[0]
            x = int(parts[1])
            y = int(parts[2])
            grid[(x, y)] = char
    return grid

def isAConnectedPipe(currentCoord, newCoord, grid):
    currentPipe = getPipeCharacter(currentCoord,grid)
    newPipe = getPipeCharacter(newCoord,grid)
    if validEndOfPipe(newPipe):
        return True
    currentPipeDirections = pipeOpeningsMap[currentPipe]
    newPipeDirections = pipeOpeningsMap[newPipe]

    currentPipeX = currentCoord[0]
    currentPipeY = currentCoord[1]
    newPipeX = newCoord[0]
    newPipeY = newCoord[1]

    if currentPipeX > newPipeX:  # Moving left
        if currentPipeDirections.get('left') and newPipeDirections.get('right'):
            return True
    elif currentPipeX < newPipeX:  # Moving right
        if currentPipeDirections.get('right') and newPipeDirections.get('left'):
            return True
    elif currentPipeY > newPipeY:  # Moving up
        if currentPipeDirections.get('up') and newPipeDirections.get('down'):
            return True
    elif currentPipeY < newPipeY:  # Moving down
        if currentPipeDirections.get('down') and newPipeDirections.get('up'):
            return True
    return False


def findStartingPoint(grid):
    for coord,char in grid.items():
        if char == '*':
            return coord
    return None

def getPipeCharacter(coord, grid):
    if coord not in grid:
        return []
    return grid[coord]

def validEndOfPipe(pipeChar):
    return bool(re.match(r'[a-zA-Z]',pipeChar))

def createFinalString(connectedPipes):
    return ''.join(sorted(connectedPipes))

def validNeighboringPipes(currentCoord,neighboringPipes,grid):
    validPipes = []
    for coord in neighboringPipes:
        if isAConnectedPipe(currentCoord,coord,grid):
            validPipes.append((coord))
    return validPipes

def printMap(grid):
    maxX = findMaxX(grid)
    maxY = findMaxY(grid)
    startingPoint = (0,0)

    map_grid = [[' ' for _ in range(maxY + 1)] for _ in range(maxX + 1)]
    for i in range(maxX):
        for j in range(maxY):
            if (i,j) in grid:
                map_grid[i][j] = getPipeCharacter((i,j),grid)

    for line in map_grid:
        print(''.join(line))

def findMaxX(grid):
    maxX = 0
    for num in grid:
        if num[0] > maxX:
            maxX = num[0]
    return maxX

def findMaxY(grid):
    maxY = 0
    for num in grid:
        if num[1] > maxY:
            maxY = num[1]
    return maxY

def findAllConnectedPipes(file_Path):
    grid = createGrid(file_Path)
    printMap(grid)
    startingPoint = findStartingPoint(grid)
    queue = [startingPoint]
    visitedCoords = []
    connectedPipes = []
    debug_mark = 0

    while queue:
        coord = queue.pop(0)
        if coord in visitedCoords:
            continue
        visitedCoords.append(coord)
        pipeChar = getPipeCharacter(coord,grid)
        if validEndOfPipe(pipeChar):
            connectedPipes.append(pipeChar)
        else:
            validPipeOpenings = getDirectionsFromPipe(pipeChar)
            neighbors = getNeighbors( coord, validPipeOpenings, grid)
            validNewPipes = validNeighboringPipes(coord,neighbors,grid)

            for newCoord in validNewPipes:
                queue.append(newCoord)

    return createFinalString(sorted(connectedPipes))

file_Path = ""
connectedPipes = findAllConnectedPipes(file_Path)
print(connectedPipes)


