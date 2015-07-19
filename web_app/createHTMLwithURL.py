import sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

file_name = getStrArg(1, 1)
lines = getFileLines(file_name)

httpStr = "http"

openHTML = '<html><head><script>function init(){window.location.href = "'
closeHTML = '"}</script></head><body onload="init();"></body></html>'

cnt = 1
for line in lines:
	if len(line) < len(httpStr):
		continue
	if line[0:len(httpStr)] != httpStr:
		continue
	url = line[:-1]
	ftw = open(str(cnt) + ".html", write_mode)
	ftw.write(openHTML)
	ftw.write(url)
	ftw.write(closeHTML)
	ftw.close()
	cnt += 1

