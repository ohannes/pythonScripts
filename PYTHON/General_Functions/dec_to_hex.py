def dec_to_hex(n):
    if((n / 16) < 10):
        temp = str(n / 16)
    elif((n / 16) == 10):
        temp = 'A'
    elif((n / 16) == 11):
        temp = 'B'
    elif((n / 16) == 12):
        temp = 'C'
    elif((n / 16) == 13):
        temp = 'D'
    elif((n / 16) == 14):
        temp = 'E'
    elif((n / 16) == 15):
        temp = 'F'
    if((n % 16) < 10):
        temp = temp + str(n % 16)
    elif((n % 16) == 10):
        temp = temp + 'A'
    elif((n % 16) == 11):
        temp = temp + 'B'
    elif((n % 16) == 12):
        temp = temp + 'C'
    elif((n % 16) == 13):
        temp = temp + 'D'
    elif((n % 16) == 14):
        temp = temp + 'E'
    elif((n % 16) == 15):
        temp = temp + 'F'
    return temp
