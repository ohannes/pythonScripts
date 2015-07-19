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

print strSearchInLineWithOffset('xxabc', 3, 'abcdefghijklmnopqrstuvwxyz', 1)
