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

print strSearchInLine('ad', 'aaabbbcccaaaddd')
