def line_no(myfile, ttf):
    myrfile = open(myfile, 'r')
    full_text = myrfile.read()
    k = 0
    j = 0
    count = 0
    line_arr = []
    for i in range(len(full_text)*2):
        myrfile.seek(i)
        oku = myrfile.read(len(ttf))
        if(oku == ttf):
            myrfile.seek(0)
            line_no = 0
            while(j <= i):
                myrfile.readline()
                line_no = line_no + 1
                j = myrfile.tell()
            count = count + 1
            line_arr.insert(k, line_no)
            k = k + 1
    print count, 'results were found\n'
    myrfile.close()
    return line_arr

ctrl = '0'

while(ctrl != '9'):
    x = raw_input('file to be searched: ')  #file to be searched
    y = raw_input('text to be found: ')     #the text to be found


    print line_no(x, y)
    print '\npress any key to continue...\n'
    ctrl = raw_input('press 9 to exit...\n')
