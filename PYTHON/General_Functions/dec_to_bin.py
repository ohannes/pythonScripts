def dec_to_bin(x):
    a = []
    bin_num = ''
    n = 0
    while(x > 0):
        a.insert(n, x%2)
        x = x / 2
        n = n + 1
    for i in range(n):
        bin_num = bin_num + str(a[-i-1])
    return bin_num

