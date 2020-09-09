import math
from Util import fact
from CombPerm import rCombinNoRep

def isPrime(num):
    for i in range(2, int(math.floor(math.sqrt(num))) + 1):
        if num % i == 0:
            return False
    return True

def primeFactorization(num):
    result = []
    x = num
    i = 1
    while not isPrime(x):
        i += 1
        if not isPrime(i):
            continue
        if x % i == 0:
            result.append(i)
            x /= i
            i -= 1
    result.append(int(x))
    return result

def generalPidgeonHole(objects, boxes):
    return "There is at least one box with " + str(math.ceil(objects/boxes)) + " objects in it."

def expandBinomial(exPow, xPow = 1, yPow = 1, xCoeff = 1, yCoeff = 1):
    result = ""
    for i in range(exPow + 1):
        coeff = int(rCombinNoRep(exPow,i) * math.pow(xCoeff,exPow-i) * math.pow(yCoeff,i))
        if (coeff != 1):
            result += str(coeff)
        if ((exPow-i) * xPow > 1):
            result += "x^" + str((exPow-i) * xPow)
        elif ((exPow-i) * xPow == 1):
            result += "x"
        if (i * yPow > 1):
            result += "y^" + str(i * yPow)
        elif i * yPow == 1:
            result += "y"
        if (i != exPow):
            result += " + "
    return result

def getCoeff(exPow, x, y, xPow = 1, yPow = 1, xCoeff = 1, yCoeff = 1):
    for i in range(exPow+1):
        if ((exPow-i) * xPow == x and i * yPow == y):
            return (int(rCombinNoRep(exPow,i) * math.pow(xCoeff,exPow-i) * math.pow(yCoeff,i)))
    return 0

def probOfDerang(num):
    s = 1
    for i in range(1,num + 1):
        s += (math.pow(-1,i) * (1/fact(i)))
    return s

def numOfDerang(num):
    return fact(num) * probOfDerang(num)

def gcd(low, upp):
    #returns gcd, the bezout coefficients
    if low == 0:
        return (upp, 0, 1)
    else:
        egcd, x, y = gcd(upp % low, low)
        return (egcd, y - (upp//low) * x, x)

def lcm(num1, num2):
    if num1 > num2:
        greater = num1
    else:
        greater = num2
    while(True):
        if((greater % num1 == 0) and (greater % num2 == 0)):
            lcm = greater
            break
        greater += 1
    return (lcm, primeFactorization(lcm))

"""#expands (4(x^2)+5(y^3))^6
print(expandBinomial(6,2,3,4,5))
#gets coefficient of (x^8)(y^6) from that same binomial
print(getCoeff(6,8,6,2,3,4,5))""" 