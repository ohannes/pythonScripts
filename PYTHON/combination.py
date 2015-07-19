import sys

USR_INP = [
    "N",
    "Y"
    ]

IND_MSG = [
    "Enter number: ",
    "C(",
    ", ",
    ") = ",
    "continue... (y/n)"
    ]

ERR_MSG = [
    "Invalid number, please try again",
    "Invalid number: negative numbers' factorial does not exist",
    "Invalid Numbers: negative inputs are not accepted",
    "Invalid Numbers: first number cannot be less than the second"
    ]

def getInputNumber():
    while True:
        inp = raw_input(IND_MSG[0])
        try:
            number = int(inp, 10)
            return number
        except:
            print ERR_MSG[0]

def factorial(n):
    if n < 0:
        print ERR_MSG[1]
        return -1
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def combination(n1, n2):
    checkInputs(n1, n2)
    f1 = factorial(n1)
    f2 = factorial(n2)
    f1_2 = factorial(n1 - n2)
    return f1 / (f2 * f1_2)

def checkInputs(n1, n2):
    if n1 < 0 or n2 < 0:
        sys.exit(ERR_MSG[2])
    if n1 < n2:
        sys.exit(ERR_MSG[3])

def printResult(n1, n2):
    print IND_MSG[1] + str(n1) + IND_MSG[2] + str(n2) + IND_MSG[3] + str(combination(n1, n2))

def calculateCombination():
    n1 = getInputNumber()
    n2 = getInputNumber()

    printResult(n1, n2)

while True:
    calculateCombination()
    inp = raw_input(IND_MSG[4])
    if inp.upper() == USR_INP[0]:
        break
