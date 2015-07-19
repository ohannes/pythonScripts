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
