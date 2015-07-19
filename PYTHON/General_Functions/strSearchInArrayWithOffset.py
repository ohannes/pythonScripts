def strSearchInLineWithOffset(keyStr, keyStrOffset, line, lineOffset):
    if len(keyStr) > len(line):
        return False
    if keyStrOffset >= len(keyStr):
        return False
    if lineOffset >= len(line):
        return False
    i = lineOffset
    j = keyStrOffset
    while j < len(keyStr):
        if keyStr[j] == line[i + j - keyStrOffset]:
            j = j + 1
        elif i < len(line) - len(keyStr) + keyStrOffset:
            j = keyStrOffset
            i = i + 1
        else:
            return False
    return True

def strSearchInArrayWithOffset(keyStr, keyStrOffset, array, arrayOffset):
    if keyStrOffset >= len(keyStr):
        return False
    if arrayOffset >= len(array):
        return False
    i = arrayOffset
    while True:
        if strSearchInLineWithOffset(keyStr, keyStrOffset, array[i], 0):
            return [i, array[i]]
        elif i < len(array) - 1:
            i = i + 1
        else:
            return [False, False]

print strSearchInArrayWithOffset('xxabc', 4, ['axcdefghi', 'abcdefgh', 'abcdefg', 'adcdef'], 0)
