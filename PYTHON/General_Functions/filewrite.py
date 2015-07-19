import os

test_env = os.getenv('test_env')
os.chdir(test_env)
os.chdir('..')

myrfile = open("MS.PSL", 'r')
mywfile = open("MS_PSLw.py", 'w')


rlines = myrfile.readlines()
writeopen = 'PSLfile.write("'
writeclose = '")\n'

for i in range(len(rlines)):
    temp = writeopen
    for j in range(len(rlines[i])):
        if(rlines[i][j] != '\n'):
            temp = temp + rlines[i][j]
    temp = temp + writeclose
    mywfile.write(temp)

myrfile.close()
mywfile.close()
