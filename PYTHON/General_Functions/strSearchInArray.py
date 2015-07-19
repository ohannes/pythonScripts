def strSearchInLine(keyStr, line):
    if len(keyStr) > len(line):
        return False
    i = 0
    j = 0
    while j < len(keyStr):
        if keyStr[j] == line[i + j]:
            j = j + 1
        elif i < len(line) - len(keyStr):
            j = 0
            i = i + 1
        else:
            return False
    return True

def strSearchInArray(keyStr, array):
    i = 0
    while True:
        if strSearchInLine(keyStr, array[i]):
            return [i, array[i]]
        elif i < len(array) - 1:
            i = i + 1
        else:
            return [False, False]

print strSearchInArray('yycd', ['aabbcc', 'yycdsss', 'hxxsdk', 'asasll'])
