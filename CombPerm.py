from copy import deepcopy
from Util import fact
from Util import bSort

#rPermutation with no repetition
def rPermutNoRep(n,r):
    return (fact(n)/fact(n-r))

#rCombination with no repetition
def rCombinNoRep(n,r):
    return (rPermutNoRep(n,r)/fact(r))

#rPermutation with repetition
def rPermutRep(n,r):
    return math.pow(n,r)

#rCombination with repetition
def rCombinRep(n,r):
    return fact(n + r - 1)/(fact(r) * fact(n - 1))

#How many ways to put distinguishable objects in distinguishable boxes
def distObjDistBox(n,r):
    d = 1
    for x in r:
      d *= fact(x)
    return fact(n)/d

#How many ways to put indistinguishable objects in distinguishable boxes
def indistObjDistBox(n,r):
    return rCombinNoRep(n + r - 1, n - 1)

#How many ways to put distinguishable objects in indistinguishable boxes
def distObjIndistBox(n,r):
    result = 0
    for j in range(1,r + 1):
        s = 0
        for i in range(j):
            s += math.pow(-1,i) * rCombinNoRep(j,i) * math.pow(j-i,n)
        result += s / fact(j)
    return result

#How many ways to put indistinguishable objects in indistinguishable boxes
def indistObjIndistBox(n_Obj,r_Box,howmanyhavetobeineachbox = 0):
    if n_Obj < 0:
        return
    n_Obj -= r_Box * howmanyhavetobeineachbox
    sol = []
    currTest = []
    for i in range(r_Box - 1):
        currTest.append(0)
    currTest.append(n_Obj)
    arr = deepcopy(currTest)
    sol.append(arr)
    while currTest[0] != n_Obj - 1:
        incrPerm(currTest,r_Box,n_Obj)
        if (not ioibHelp(currTest,sol,r_Box)):
            summ = 0
            for i in currTest:
                summ += i
            if summ == n_Obj:
                arr = deepcopy(currTest)
                bSort(arr, r_Box)
                sol.append(arr)
    return (sol, len(sol))

def incrPerm(arr,size,maxim):
    #helper function for indistObjIndistBox
    if arr[0] == maxim:
        return
    for i in range(size - 1, -1, -1):
        if arr[i] < maxim - 1:
            arr[i] += 1
            break
        arr[i] = 0
  
def ioibHelp(arr1, arr2, size):
    #helper function for indistObjIndistBox
    arrTest = deepcopy(arr1)
    bSort(arrTest,size)
    arr2Test = deepcopy(arr2)
    for i in arr2Test:
        for k in range(size):
            if arrTest[k] != i[k]:
                break
            if arrTest[k] == i[k] and k == size - 1:
                return True
    return False