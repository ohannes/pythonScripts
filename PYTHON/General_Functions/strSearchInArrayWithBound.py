def strSearchInLineWithBound(keyStr, keyStrLowBound, keyStrUpBound, line, lineLowBound, lineUpBound):
    if keyStrUpBound - keyStrLowBound > lineUpBound - lineLowBound:
        return False
    if keyStrLowBound >= keyStrUpBound:
        return False
    if lineLowBound >= lineUpBound:
        return False
    if keyStrUpBound - keyStrLowBound > len(keyStr):
        return False
    if lineUpBound - lineLowBound > len(line):
        return False
    i = lineLowBound
    j = keyStrLowBound
    while j < keyStrUpBound:
        if keyStr[j] == line[i + j - keyStrLowBound]:
            j = j + 1
        elif i < lineUpBound - keyStrUpBound + keyStrLowBound :
            j = keyStrLowBound
            i = i + 1
        else:
            return False
    return True


def strSearchInArrayWithBound(keyStr, keyStrLowBound, keyStrUpBound, array, arrayLowBound, arrayUpBound):
    if keyStrLowBound >= keyStrUpBound:
        return [False, False]
    if arrayLowBound >= arrayUpBound:
        return [False, False]
    if keyStrUpBound - keyStrLowBound > len(keyStr):
        return [False, False]
    if arrayUpBound - arrayLowBound > len(array):
        return [False, False]
    i = arrayLowBound
    while True:
        if strSearchInLineWithBound(keyStr, keyStrLowBound, keyStrUpBound, array[i], 0, len(array[i])):
            return [i, array[i]]
        elif i < arrayUpBound - 1:
            i = i + 1
        else:
            return [False, False]

print strSearchInArrayWithBound('xxabcd', 4, 6, ['axcdefghi', 'axcdefgh', 'abcdefg', 'adcdef'], 0, 4)
