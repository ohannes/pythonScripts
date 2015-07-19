import os, sys

PERCENTAGE_STEP = 1

file_name = ""
char_per_line = 0

if len(sys.argv) < 3:
    sys.exit("Usage Error: python to_hex <file_name:string> <char_per_line:int>")
else:
    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        sys.exit("File Not Exists Error: No such file:: " + file_name)
    try:
        char_per_line = int(sys.argv[2], 10)
    except:
        sys.exit("Invalid Argument Error: invalid char per line: " + sys.argv[2])

file_stat = os.stat(file_name)
file_size = file_stat.st_size
size_per_step = file_size / (100 / PERCENTAGE_STEP)
print "file size:", file_size
ftr = open(file_name)
ftw = open(file_name + ".hex", "w")
byte_cnt = 0
step_cnt = 0
step_str = ""

def cleanMessage(message):
    for char in message:
        sys.stdout.write("\b")
    sys.stdout.flush()

def writeMessage(message):
    sys.stdout.write(message)
    sys.stdout.flush()

while True:
    byte = ftr.read(1)
    if len(byte) < 1:
        cleanMessage(step_str)
        step_str = "100% completed"
        writeMessage(step_str)
        break
    ftw.write(str(hex(ord(byte)))[2:])
    if byte_cnt == step_cnt * size_per_step and step_cnt < 100:
        cleanMessage(step_str)
        step_str = str(step_cnt) + "% completed"
        writeMessage(step_str)
        step_cnt += 1
    byte_cnt += 1
    if byte_cnt % char_per_line:
        ftw.write(" ")
    else:
        ftw.write("\n")

ftw.close()
ftr.close()
