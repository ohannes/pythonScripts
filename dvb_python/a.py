import os

input_file = "out.txt"

if not os.path.exists(input_file):
	sys.exit("input file does not exists " + input_file)

ftr = open(input_file)

last_line = ""
last_pts = 0
cnt = 0

while True:
	cnt += 1
	line = ftr.readline()
	if line == "":
		break
	if line == last_line:
		continue
	if line[-1] == "\n":
		line = line[:-1]
	if not "Current PTS: " in line:
		continue
	split = line.split(": ")
	pts_str = split[1]
	try:
		pts = int(pts_str, 10)
	except:
		print "unable to convert to integer", line, "at line", cnt
		continue
	if last_pts != 0 and last_pts != pts:
		if pts - last_pts != 3600:
			print "unexpected pts", pts, "at line", cnt
			print "expected", last_pts+3600, "read", pts
	last_line = line
	last_pts = pts

ftr.close()
