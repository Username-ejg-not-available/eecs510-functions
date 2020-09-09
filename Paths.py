from copy import deepcopy
from numpy import dot

def shortestPathLength(rel,start,fin):
    L = [1000000 for column in range(len(rel))]
    S = [0 for column in range(len(rel))]
    P = [[] for column in range(len(rel))]
    L[start] = 0
    cur = start
    while S[fin] == 0:
        mini = 1000000
        miniC = -1
        for j in range(len(rel)):
            if not S[j]:
                if L[j] < mini:
                    mini = L[j]
                    miniC = j
        S[miniC] = 1
        cur = miniC
        for i in range(len(rel)):
             if L[cur] + rel[cur][i] < L[i] and not S[i] and rel[cur][i]:
                L[i] = L[cur] + rel[cur][i]
                P[i] = []
                for j in P[cur]:
                    P[i].append(j)
                P[i].append(cur)
    P[fin].append(fin)
    return (L[fin],P[fin])
            
def numPathsBetweenVertices(arr,v1,v2,length):
    a = deepcopy(arr)
    for i in range(length - 1):
        a = dot(a,arr)
    return a[v1][v2]

#CLOSURE FUNCTIONS
def reflClose(matrix):
    m = deepcopy(matrix)
    for x in range(0, len(m)):
        m[x][x] = 1
    return m

def symmClose(matrix):
    m = deepcopy(matrix)
    for x in range(1, len(m)):
        for y in range(0, x):
            if m[x][y]:
                m[y][x] = 1
            if m[y][x]:
                m[x][y] = 1
    return m

def transClose(matrix):
    m = deepcopy(matrix)
    result = ""
    #print("Mr is: \n " + str(m).replace("[", "").replace("]", "\n").replace(",", ""))
    for k in range(0, len(m)):
        for row in range(0, len(m)):
            for col in range(0, len(m)):
                m[row][col] = m[row][col] or (m[row][k] and m[k][col])
        result += ("W" + str(k) + " is: \n " + str(m).replace("[", "").replace("]", "\n").replace(",", ""))
    #result += ("Trans Closure is: \n " + str(atrix).replace("[", "").replace("]", "\n").replace(",", ""))
    #print(result)
    return m
 
def makeEqRelation(matrix):
    m = deepcopy(matrix)
    m = reflClose(m)
    while not isSymm(m) or not isTrans(m):
        m = transClose(symmClose(m))
    return m

def isSymm(matrix):
    for x in range(1, len(matrix)):
        for y in range(0, x):
            if matrix[x][y] != matrix[y][x]:
                return 0
    return 1

def isRefl(matrix):
    for x in range(0, len(matrix)):
        if matrix[x][x] == 0:
            return 0
    return 1

def isTrans(matrix):
    for x in range(0, len(matrix)):
        for y in range(0, len(matrix)):
            for z in range(0, len(matrix)):
                if matrix[x][y] and matrix[y][z] and not matrix[x][z]:
                    return 0
    return 1

def isAntiSymm(matrix):
    for x in range(0, len(matrix)):
        for y in range(0, len(matrix)):
            if x == y:
                continue
            if matrix[x][y] and matrix[y][x]:
                return 0
    return 1

def isPartialOrdering(matrix):
    return isAntiSymm(matrix) and isTrans(matrix) and isRefl(matrix)

def convertToHasse(matrix):
    m = deepcopy(matrix)
    if not isPartialOrdering(m):
        print("Not a Partial Ordering!")
        return
    for x in range(0, len(m)):
        m[x][x] = 0
    for x in range(0, len(m)):
        for y in range(0, len(m)):
            for z in range(0, len(m)):
                if m[x][y] and m[y][z] and m[x][z]:
                    m[x][z] = 0
    return m

def isHasse(matrix):
    m = deepcopy(matrix)
    if not isPartialOrdering(transClose(reflClose(m))):
        return 0
    for x in range(0, len(m)):
        if m[x][x] == 1:
            return 0
        for y in range(0, len(m)):
            for z in range(0, len(m)):
                if m[x][y] and m[y][z] and m[x][z]:
                    return 0
    return 1

def convertToPartialOrdering(matrix):
    m = deepcopy(matrix)
    if not isHasse(m):
        print("Not a Hasse Diagram!")
        return
    return transClose(reflClose(m))
       
def listOrderedPairsRelationFromPartitions(matrix):
    for x in range(0, len(matrix)):
        for y in range(0, len(matrix[x])):
            for z in range(0, len(matrix[x])):
                print("[" + str(matrix[x][y]) + ", " + str(matrix[x][z]) + "],")

def hasseAnalysis(matrix):
    if not isHasse(matrix):
        print("Not a Hasse Diagram")
        return
    maximal = []
    minimal = []
    for x in range(0, len(matrix)):
        maximal.append(0)
        minimal.append(0)
    fullOfZeros = False
    prevM = deepcopy(matrix)
    while not fullOfZeros:
        fullOfZeros = True
        m = dot(prevM, matrix)
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix)):
                if m[x][y] != 0:
                    fullOfZeros = False
                    break
        if not fullOfZeros:
            prevM = deepcopy(m)
    
    for x in range(0, len(prevM)):
        for y in range(0, len(prevM)):
            if prevM[x][y] != 0:
                minimal[x] = 1
                maximal[y] = 1
    sum1, sum2 = 0, 0
    for x in range(0, len(prevM)):
        if minimal[x]:
            sum1 += 1
        if maximal[x]:
            sum2 += 1
            
    print("Maximal Elements: " + str(maximal) + "\nMinimal Elements: " + str(minimal))
    if sum2 != 1:
        print("No greatest element.")
    else:
        print("Greatest ELement: " + str(maximal))
    if sum1 != 1:
        print("No least element.")
    else:
        print("Least ELement: " + str(minimal))

def upperBounds(matrix, subset):
    m = deepcopy(matrix)
    paths = reflClose(deepcopy(m))
        
    fullOfZeros = False
    it = 1
    while not fullOfZeros:
        it += 1
        fullOfZeros = True
        m = dot(m, matrix)
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix)):
                if m[x][y]:
                    fullOfZeros = False
                    paths[x][y] += it
    upperBound = []
    for x in range(0, len(m)):
        upperBound.append(1)
    for x in range(0, len(m)):
        if not subset[x]:
            continue
        for y in range(0, len(m)):
            upperBound[y] = upperBound[y] and paths[x][y]
    for x in range(0, len(m)):
        if subset[x] and upperBound[x]:
            upperBound[x] = .5
    return upperBound

def leastUpperBound(matrix, subset):
    upperBound = upperBounds(matrix, subset)
    result = []
    for x in range(0, len(upperBound)):
        result.append(0)
    for x in range(0, len(upperBound)):
        if upperBound[x] == .5:
            result[x] = 1
            return result
    notLeast = True
    suM = 0
    i = 0
    while notLeast:
        i += 1
        for x in range(0, len(upperBound)):
            if upperBound[x] == i:
                notLeast = False
                suM += 1
    if suM != 1:
        return False
    else:
        for x in range(0, len(upperBound)):
            if upperBound[x] == i:
                result[x] = 1
                return result

def lowerBounds(matrix, subset):
    m = deepcopy(matrix)
    paths = reflClose(deepcopy(m))
        
    fullOfZeros = False
    it = 1
    while not fullOfZeros:
        it += 1
        fullOfZeros = True
        m = dot(m, matrix)
        for x in range(0, len(m)):
            for y in range(0, len(m)):
                if m[x][y]:
                    fullOfZeros = False
                    paths[x][y] += it
    for x in range(0, len(m)):
        for y in range(0, len(m)):
            m[x][y] = paths[y][x]
    lowerBound = []
    for x in range(0, len(m)):
        lowerBound.append(1)
    for x in range(0, len(m)):
        if not subset[x]:
            continue
        for y in range(0, len(m)):
            lowerBound[y] = lowerBound[y] and m[x][y]
    for x in range(0, len(m)):
        if subset[x] and lowerBound[x]:
            lowerBound[x] = .5
    return lowerBound

def greatestLowerBound(matrix, subset):
    lowerBound = lowerBounds(matrix, subset)
    result = []
    for x in range(0, len(lowerBound)):
        result.append(0)
    for x in range(0, len(lowerBound)):
        if lowerBound[x] == .5:
            result[x] = 1
            return result
    notGreat = True
    i = 0
    suM = 0
    while notGreat:
        i += 1
        for x in range(0, len(lowerBound)):
            if lowerBound[x] == i:
                notGreat = False
                suM += 1
    if suM != 1:
        return False
    else:
        for x in range(0, len(lowerBound)):
            if lowerBound[x] == i:
                result[x] = 1
                return result

def isLattice(matrix):
    if not isHasse(matrix):
        return False
    test = []
    for x in range(0, len(matrix)):
        test.append(0)
    for x in range(0, len(matrix)):
        for y in range(0, len(matrix)):
            for z in range(0, len(matrix)):
                test[z] = 0
            test[x] = 1
            test[y] = 1
            if not leastUpperBound(matrix, test):
                return False
            if not greatestLowerBound(matrix, test):
                return False
    return True

#example 2 of Dijkstra's algorithm from slides
#input is adjacency matrix except 1s are replaced with the weights
#it doesn't matter which vertices are assigned with indices in the matrix as long as you are consistent for rows and columns
#in this example, index 0 = a, index 1 = b, etc.
"""graph = [[0,4,2, 0,0, 0],
            [4,0,1, 5,0, 0],
            [2,1,0, 8,10,0],
            [0,5,8, 0,2, 6],
            [0,0,10,2,0, 3],
            [0,0,0, 6,3, 0],]
   #second 2 params refer to the starting and ending vertices
   print(shortestPathLength(graph,0,5))"""

#Example 15 from isomorphism slides
#Calculates number of paths of a certain length between two vertices given an adjacency matrix
"""arr = [[0,1,1,0],
          [1,0,0,1],
          [1,0,0,1],
          [0,1,1,0]]
   print(numPathsBetweenVertices(arr,0,3,4))"""