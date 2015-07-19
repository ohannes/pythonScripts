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

print strSearchInLineWithBound('xxabc', 0, 1, 'abcdefghijklmnopqrstuvwxyz', 0, 23)
