# -*- coding: cp1254 -*-
import xlrd
import os

fonkArr = ["Fonksiyon Tablo 0",
           "Fonksiyon Tablo 1",
           "Fonksiyon Tablo 2",
           "Fonksiyon Tablo 4",
           "Fonksiyon Tablo 5",
           "Fonksiyon Tablo 6",
           "Fonksiyon Tablo 8",
           "Fonksiyon Tablo 10",
           "Fonksiyon Tablo 11",
           "Fonksiyon Tablo 0+MFT",
           "Fonksiyon Tablo 1+MFT",
           "Fonksiyon Tablo 2+MFT",
           "Fonksiyon Tablo 4+MFT",
           "Fonksiyon Tablo 5+MFT",
           "Fonksiyon Tablo 6+MFT",
           "Fonksiyon Tablo 8+MFT",
           "Fonksiyon Tablo 10+MFT",
           "Fonksiyon Tablo 11+MFT",
           "Fonksiyon Tablo 0+REJ",
           "Fonksiyon Tablo 1+REJ",
           "Fonksiyon Tablo 2+REJ",
           "Fonksiyon Tablo 4+REJ",
           "Fonksiyon Tablo 6+REJ",
           "Fonksiyon Tablo 7+REJ",
           "Fonksiyon Tablo 8+REJ",
           "Fonksiyon Tablo 10+REJ",
           "Fonksiyon Tablo 11+REJ",
           "Fonksiyon Tablo 0+MFT+REJ.",
           "Fonksiyon Tablo 1+MFT+REJ.",
           "Fonksiyon Tablo 2+MFT+REJ.",
           "Fonksiyon Tablo 4+MFT+REJ.",
           "Fonksiyon Tablo 5+MFT+REJ.",
           "Fonksiyon Tablo 6+MFT+REJ.",
           "Fonksiyon Tablo 8+MFT+REJ.",
           "Fonksiyon Tablo 10+MFT+REJ.",
           "Fonksiyon Tablo 11+MFT+REJ."
           ]

optionArray = [
                "------------------------------------------- Ön Yıkama -------------------------------------------------", "16",
                "--------------------------------------------------- Ana Yıkama -------------------------------------------------------", "18",
                "---------MFT---------", "4",
                "--------------Soğuk Durulama----------------", "7",
                "---------MFT---------", "4",
                "------------ Sıcak Durulama1 ----------------------", "8",
                "--------------------------- Sıcak Durulama2 -------------------------------", "12",
                "---------MFT---------", "4",
                "---------DSB---------", "4",
                "---------------REJENERASYON------------------------------", "9",
                "------------KURUTMA----------------------------------------------------", "12"
              ]

def findFonk(head):
    fonk = ""
    i = 0
    #print "while loop 0"
    while i < len(head):
        if head[i] == "(":
            i += 1
            break
        i += 1
    #print "while loop 0"
    #print "while loop 1"
    while i < len(head):
        if head[i] !=  ")":
            fonk += head[i]
        i += 1
    #print "while loop 1"
    return fonk

fileName = "F5-F7_EU_60cm_BLDC_V_PAT_GR_V03_MT_convert"
exceptPage = [
                "Auto2-W2L1074",
                "Auto7L-W2L1058"
             ]
header2length = 100
headerlength = 65
datalength = 8
programCount = 98

wb = xlrd.open_workbook(fileName + '.xls')
sheets = wb.sheets()
counter = 0
pageCounter = 0
space = " "
for sheet in sheets:
    print sheet.name
    ##print len(sheets)
    ##print len(fonkArr)
    ftw = open(sheet.name+".txt", "w")
    numCol = sheet.ncols
    for colNum in range(numCol):
        if sheet.cell_value(5, colNum) == "Kalan Zaman":
            cells1 = sheet.col_values(colNum, start_rowx=6, end_rowx=104)
            cells2 = sheet.col_values(colNum+1, start_rowx=6, end_rowx=104)
            cells3 = sheet.col_values(colNum+2, start_rowx=6, end_rowx=104)
            if sheet.name in exceptPage:
                cells4 = sheet.col_values(4, start_rowx=6, end_rowx=104)
                cells5 = sheet.col_values(5, start_rowx=6, end_rowx=104)
            else:
                cells4 = sheet.col_values(colNum+3, start_rowx=6, end_rowx=104)
                cells5 = sheet.col_values(colNum+4, start_rowx=6, end_rowx=104)
            _E = []
            _F = []
            _G = []
            _H = []
            _I = []
            for cell in cells1:
                if type(cell) is str:
                    _E.append(cell.encode('ascii', 'ignore'))
                else:
                    _E.append(str(cell))
            for cell in cells2:
                if type(cell) is str:
                    _F.append(cell.encode('ascii', 'ignore'))
                else:
                    _F.append(str(cell))
            for cell in cells3:
                if type(cell) is str:
                    _G.append(cell.encode('ascii', 'ignore'))
                else:
                    _G.append(str(cell))
            for cell in cells4:
                if type(cell) is str:
                    _H.append(cell.encode('ascii', 'ignore'))
                else:
                    _H.append(str(cell))
            for cell in cells5:
                if type(cell) is str:
                    _I.append(cell.encode('ascii', 'ignore'))
                else:
                    _I.append(str(cell))
            E = []
            F = []
            G = []
            H = []
            I = []
            for cell in _E:
                if cell == "-":
                    data = "0"
                elif "." in cell:
                    data = ""
                    if cell[-1] != "0":
                        for char in cell:
                            if char != ".":
                                data += char
                    else:
                        for char in cell:
                            if char != ".":
                                data += char
                            else:
                                break
                else:
                    data = cell
                E.append(data)
            for cell in _F:
                if cell == "-":
                    data = "0"
                elif "." in cell:
                    data = ""
                    if cell[-1] != "0":
                        for char in cell:
                            if char != ".":
                                data += char
                    else:
                        for char in cell:
                            if char != ".":
                                data += char
                            else:
                                break
                else:
                    data = cell
                F.append(data)
            for cell in _G:
                if cell == "litre":
                    data = "lt"
                elif cell == "dak":
                    data = "dk"
                else:
                    data = cell
                G.append(data)
            for cell in _H:
                if cell == "-":
                    data = "_idle"
                elif cell == "ALT":
                    data = "_dwnn"
                elif cell == "UST":
                    data = "_uppp"
                elif cell == "60sn UST-60sn ALT":
                    data = "_upDw1"
                elif cell == "60sn UST-90sn ALT":
                    data = "_upDw2"
                elif cell == "90sn UST-60sn ALT":
                    data = "_upDw3"
                elif cell == "SUREKLI ENERJILI":
                    data = "_runn"
                H.append(data)
            for cell in _I:
                if cell == "-":
                    data = "_00"
                elif cell == "2200":
                    data = "_22"
                elif cell == "2400":
                    data = "_24"
                elif cell == "2600":
                    data = "_26"
                elif cell == "2800":
                    data = "_28"
                elif cell == "3000":
                    data = "_30"
                elif cell == "3200":
                    data = "_32"
                elif cell == "3400":
                    data = "_34"
                I.append(data)
                
            header = ""
            _header = sheet.cell_value(4, colNum)
            for char in _header:
                if char != "\n":
                    header += char
            header2 = findFonk(header)
            #print "while loop 2"
            #print len(header), headerlength
            while len(header) != headerlength:
                header = " " + header
            #print "while loop 2"

            line = ""
            line += "{"
            for i in range(len(E)):
                data = E[i]
                #print "while loop 3"
                while len(data) != datalength:
                    data = " " + data
                #print "while loop 3"
                line += data + ", "
            line = line[:-2]
            line += "},"
            line += "\n"
            ftw.write(header + " " + line)

            htw = None
            if header2 in fonkArr:
                htw = open(header2+".txt", "a")
                spacedHeader = "/*" + sheet.name + " -> " + header + space + "*/"
                #print "while loop 4"
                while len(spacedHeader) != header2length:
                    spacedHeader = " " + spacedHeader
                #print "while loop 4"
                line2 = spacedHeader + line
                htw.write(line2)
                xtw = open(header2+"-kalan zaman.c", "a")
                xtw.write(line2)
                xtw.close()

            line = ""
            line += "{"
            for i in range(len(F)):
                if G[i] == "C":
                    if F[i] == "0":
                        data = "_0" + F[i] + G[i]
                    else:
                        data = "_" + F[i] + G[i]
                elif G[i] == "lt":
                    if "." in _F[i] and _F[i][-1] == "0":
                        data = F[i] + "0 " + G[i]
                    else:
                        data = F[i] + " " + G[i]
                else:
                    data = F[i] + " " + G[i]
                #print "while loop 5"
                while len(data) != datalength:
                    data = " " + data
                #print "while loop 5"
                line += data  + ", "
            line = line[:-2]
            line += "},"
            line += "\n"
            ftw.write(header + " " + line)
            
            if header2 in fonkArr:
                spacedHeader = "/*" + sheet.name + " -> " + header + space + "*/"
                #print "while loop 6"
                while len(spacedHeader) != header2length:
                    spacedHeader = " " + spacedHeader
                #print "while loop 6"
                line2 = spacedHeader + line
                htw.write(line2)
                xtw = open(header2+"-parametre.c", "a")
                xtw.write(line2)
                xtw.close()

            line = ""
            line += "{"
            for i in range(len(I)):
                data  = I[i]
                #print "while loop 7"
                while len(data) != datalength:
                    data = " " + data
                #print "while loop 7"
                line += data + ", "
            line = line[:-2]
            line += "},"
            line += "\n"
            ftw.write(header + " " + line)

            if header2 in fonkArr:
                spacedHeader = "/*" + sheet.name + " -> " + header + space + "*/"
                #print "while loop 8"
                while len(spacedHeader) != header2length:
                    spacedHeader = " " + spacedHeader
                #print "while loop 8"
                line2 = spacedHeader + line
                htw.write(line2)
                htw.write("\n")
                #htw.close()
                xtw = open(header2+"-motor.c", "a")
                xtw.write(line2)
                #xtw.close()

            line = ""
            line += "{"
            for i in range(len(H)):
                data  = H[i]
                #print "while loop 7-2"
                while len(data) != datalength:
                    data = " " + data
                #print "while loop 7-2"
                line += data + ", "
            line = line[:-2]
            line += "},"
            line += "\n"
            ftw.write(header + " " + line)

            if header2 in fonkArr:
                spacedHeader = "/*" + sheet.name + " -> " + header + space + "*/"
                #print "while loop 8"
                while len(spacedHeader) != header2length:
                    spacedHeader = " " + spacedHeader
                #print "while loop 8"
                line2 = spacedHeader + line
                htw.write(line2)
                htw.write("\n")
                htw.close()
                xtw = open(header2+"-motor.c", "a")
                xtw.write(line2)
                xtw.close()

            ftw.write("\n")
            ##print counter, sheet.name, "->", header2
            counter += 1
    ##print pageCounter, sheet.name
    pageCounter += 1
    ftw.close()

#print "I am about to finish"
os.system("md c")
os.system("md fonk")
os.system("md other")
os.system("move *.c c")
os.system("move fonk*.txt fonk")
os.system("move *.txt other")

open_str = ""
open_str += "\n\n\t{\n"
data = "//,"
#print "while loop 9"
while len(data) != header2length:
    data = data + " "
#print "while loop 9"
open_str += data + space
i = 0
#print "while loop 10"
while i < len(optionArray):
    data = optionArray[i]
    stateNum = int(optionArray[i+1])
    #print "while loop 11"
    while len(data) != stateNum * datalength + 1:
        data = "-" + data
    #print "while loop 11"
    data = "<" + data + ">"
    open_str += data + ", "
    i += 2
#print "while loop 10"
open_str = open_str[:-2] + "\n"
data = "//stepNo"
#print "while loop 12"
while len(data) != header2length:
    data = data + " "
#print "while loop 12"
open_str += data + space
for i in range(programCount):
    data = str(i)
    if len(data) == 1:
        data = "0" + data
    data = "s" + data
    #print "while loop 13"
    while len(data) != datalength:
        data = " " + data
    #print "while loop 13"
    open_str += data + ", "
open_str = open_str[:-2] + "\n"

close_str = ""
close_str += "\t},\n"

addr = str(os.getcwd()) + "\\c"
for fileName in os.listdir(addr):
    ftw = None
    ftr = open(addr + "\\" + fileName, "r")
    flines = ftr.readlines()
    ftr.close()
    if len(fileName.split("+")) == 1:
        ftw = open("Fonksiyon_"+fileName.split("-")[1], "a")
    elif len(fileName.split("+")) == 2:
        ftw = open("Fonksiyon+" + fileName.split("+")[1][:3] + "_"+fileName.split("-")[1], "a")
    elif len(fileName.split("+")) == 3:
        ftw = open("Fonksiyon+MFT+REJ._"+fileName.split("-")[1], "a")
    ftw.write(open_str)
    for line in flines:
        ftw.write(line)
    ftw.write(close_str)
    ftw.close()

os.system("md EA")
os.system("move *.c EA")
os.system("move c EA")
os.system("move fonk EA")
os.system("move other EA")

print "DONE"
