def str_in_line(key_str, line):
    FOUND = False
    i = 0
    if(len(key_str) > len(line)):
        return FOUND
    while 1:
        x =  ''
        for j in range(len(key_str)):
            x = x + line[i + j]
        if(x == key_str):
            FOUND = True
            break
        elif(i < len(line) - len(key_str)):
            i = i + 1
        else:
            break
    return FOUND

def str_in_file(key_str, rlines):
    i = 0
    while 1:
        if(str_in_line(key_str, rlines[i])):
            return [i, rlines[i]]
        else:
            if(i < len(rlines) - 1):
                i = i + 1
            else:
                return -1
