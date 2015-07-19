#           ***environment variables***
#       test_env        ::      sip***st.cpp
#       target          ::      pr.bat

import threading
import os
import time
from time import localtime, strftime

all_test_arr = 'cut', 'dut', 'eut', 'iut', 'put', 'tut'

def reset(all_tests_arr):
    test_env = os.getenv('test_env')
    os.chdir(test_env)
    os.chdir('..')

    for i in range(len(all_tests_arr)):
        txtfile = 'MS_' + all_tests_arr[i].upper() + '.txt'
        ctrl_remove = os.access(txtfile, os.F_OK)
        if(ctrl_remove == True):
            os.remove(txtfile)
        txtfile = 'MS_' + all_tests_arr[i].upper() + '_BUILD.log'
        ctrl_remove = os.access(txtfile, os.F_OK)
        if(ctrl_remove == True):
            os.remove(txtfile)

ctrl_reset = raw_input('reset all the log files (Y/N): ')

if(ctrl_reset == 'y'):
    reset(all_test_arr)
elif(ctrl_reset == 'Y'):
    reset(all_test_arr)

h = 0
curr_test_arr = []
test_factor = '0'
print all_test_arr
while(len(test_factor) != 6):
    test_factor = raw_input('binary array (' + str(len(all_test_arr)) + ' digits): ')
for i in range(len(test_factor)):
    if(test_factor[i] == '1'):
        curr_test_arr.insert(h, all_test_arr[i])
        h = h + 1

print 'create PSL file...1'
print 'create AXE file...2'
print 'run...............4'
test_code = -1
while(test_code < 1 or test_code > 7):
    test_code = input("total: ")

def gogogo(test_name, ctrl):

    if(ctrl == 1 or ctrl == 3 or ctrl == 5 or ctrl == 7):
        test_env = os.getenv('test_env')
        os.chdir(test_env)
        ara_metin = 'IsVoIPParametersNull'
        blg_brk = 'sip' + test_name + 'st'
        myfile = 'sip' + test_name + 'st.cpp'
        belge = open(myfile, 'r')
        full_metin = belge.read()
        UCHAR_arr = []
        line_arr = []
        test_arr = []
        full_test_name = ''

        belge.seek(0)
        lines = belge.readlines()

        z = 0
        for z in range(len(lines)):
            if(full_test_name == ''):
                if(len(lines[z]) > 3):
                    if(lines[z][0] + lines[z][1] + lines[z][2] == 'SIP'):
                        for y in range(len(lines[z])):
                            if(lines[z][y] != ':'):
                                full_test_name = full_test_name + lines[z][y]
                            else:
                                break


        n = 0
        for i in range(len(lines)):
            lines[i] = lines[i][:-1]
            if(len(lines[i])>5):
                if(lines[i][0] + lines[i][1] + lines[i][2] + lines[i][3] + lines[i][4] == 'UCHAR'):
                    if(lines[i-1] != '/*'):
                        UCHAR_arr.insert(n, i+1)
                        n = n + 1

        k = 0
        j = 0
        count = 0
        for i in range(len(full_metin)*2):
            belge.seek(i)
            oku = belge.read(len(ara_metin))
            if(oku == ara_metin):
                belge.seek(0)
                line_no = 0
                while(j <= i):
                    belge.readline()
                    line_no = line_no + 1
                    j = belge.tell()
                count = count + 1
                print 'at line', line_no
                line_arr.insert(k, line_no)
                k = k + 1

        x = 0
        m = 0
        while(1):
            if(UCHAR_arr[x]<line_arr[0]):
                x = x + 1
            else:
                x = x - 1
                for i in range(len(UCHAR_arr) - x):
                    test_arr.insert(m, UCHAR_arr[x])
                    m = m + 1
                    x = x + 1
                break

        x = len(line_arr) - len(test_arr)
        if(x>0):
            line_arr = line_arr[:-x]
            count = len(line_arr)

        if(count == 0):
            print ara_metin, 'was not found'
        else:
            print count, 'results were found'
        print 'search completed!'

        os.chdir('../src_cpp')

        fhw = open("fhw.cpp", 'r')
        metin_ara = 'FHW::Entry'
        fhw_full_metin = fhw.read()
        j = 0
        for i in range(len(fhw_full_metin)*2):
            fhw.seek(i)
            fhw_oku = fhw.read(len(metin_ara))
            if(fhw_oku == metin_ara):
                fhw.seek(0)
                fhw_line_no = 0
                while(j <= i):
                    fhw.readline()
                    fhw_line_no = fhw_line_no + 1
                    j = fhw.tell()
                break
        
        os.chdir('..')
        
        logfile = 'MS_' + test_name.upper() + '.txt'

        brk_pnt = open('MS.PSL', 'w')

        brk_pnt.write('DEBUGemucommand("Control Dynamic 1 1 1");\n\n')
        brk_pnt.write('DEBUGload("MS.AXE");\n\n')
        brk_pnt.write('PSLlogfile("' + logfile + '");\n')
        brk_pnt.write('PSLlogging(1);\n\n')
        brk_pnt.write('printf("___' + full_test_name + '___");\n')
        brk_pnt.write('DEBUGbreakclear();\n')
        brk_pnt.write('bp1 = DEBUGbreakset("#cmonitor#154");\n')
        brk_pnt.write('bp2 = DEBUGbreakset("#ipp#EX0_IVPN");\n')
        brk_pnt.write('bp3 = DEBUGbreakset("#voip#J3_VIC");\n')
        brk_pnt.write('//DEBUGbreakset("#voip#J1_CFND");\n')
        brk_pnt.write('//DEBUGbreakset("#voip#J1_CTND");\n')
        brk_pnt.write('//DEBUGbreakset("#cm#J1_Purge");\n\n\n')
        brk_pnt.write('emu.bphandle = 0;\n\n')
        brk_pnt.write('PORT_CNT = 128;\n')
        brk_pnt.write('DIALOG_CNT = 48;\n')
        brk_pnt.write('REFERENCE_CNT = 16;\n')
        brk_pnt.write('TRKCNT = 20;\n')
        brk_pnt.write('IPTRK_CNT = 36;\n')
        brk_pnt.write('MFRCNT = 6;\n')
        brk_pnt.write('CHANCNT = 12;\n')
        brk_pnt.write('MAX_RUNTO_CNT = ' + str(count) + ';\n\n')
            
        brk_pnt.write('line_no_arr =\n{\n')
        for i in range(count):
            brk_pnt.write('\t"' + blg_brk + '#' + str(line_arr[i]))
            if(i != count - 1):
                brk_pnt.write('",\n')
            else:
                brk_pnt.write('"\n')
        brk_pnt.write('}\n\n')
        
        brk_pnt.write('test_name_arr = \n{\n')
        for i in range(count):
            brk_pnt.write('\t"' + str(lines[test_arr[i] - 1]))
            if(i != count - 1):
                brk_pnt.write('",\n')
            else:
                brk_pnt.write('"\n')
        brk_pnt.write('}\n\n')
        
        brk_pnt.write('int DEBUGcontrol(test_name)\n')
        brk_pnt.write('{\n')
            
        brk_pnt.write('if(!DEBUGisrunning(emu))\n')
        brk_pnt.write('{\n')
            
        brk_pnt.write('\tif(bp1 == emu.bphandle)\n')
        brk_pnt.write('\t{\n')
            
        brk_pnt.write('\t\tprintf("FAILURE_1 at %s", test_name);\n')
        brk_pnt.write('\t\tprintf("----------------------------");\n')
        brk_pnt.write('\t\tprintf("----------------------------");\n')
        brk_pnt.write('\t\tseverity_str = "";\n')
        brk_pnt.write('\t\tfile_str = "";\n')
        brk_pnt.write('\t\tmsg_str = "";\n')
        
        brk_pnt.write('\t\ti = 0;\n')
        brk_pnt.write('\t\tdo\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str,"severity[%d]", i);\n')
        brk_pnt.write('\t\t\tseverity_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tseverity_str[i] = severity_i;\n')
        brk_pnt.write('\t\t\ti++;\n')
        brk_pnt.write('\t\t}\n')
        brk_pnt.write('\t\twhile(severity_i != 0)\n')
        
        brk_pnt.write('\t\ti = 0;\n')
        brk_pnt.write('\t\tdo\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str,"file[%d]", i);\n')
        brk_pnt.write('\t\t\tfile_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tfile_str[i] = file_i;\n')
        brk_pnt.write('\t\t\ti++;\n')
        brk_pnt.write('\t\t}\n')
        brk_pnt.write('\t\twhile(file_i != 0)\n')
        
        brk_pnt.write('\t\terr_line = TARGETreadword("line");\n')
        
        brk_pnt.write('\t\ti = 0;\n')
        brk_pnt.write('\t\tdo\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str,"msg[%d]", i);\n')
        brk_pnt.write('\t\t\tmsg_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tmsg_str[i] = msg_i;\n')
        brk_pnt.write('\t\t\ti++;\n')
        brk_pnt.write('\t\t}\n')
        brk_pnt.write('\t\twhile(msg_i != 0)\n\n')
        brk_pnt.write('\t\tprintf("%s failed at %s:%d(%s)", msg_str, file_str, err_line, severity_str);\n')
        brk_pnt.write('\t\tprintf("----------------------------");\n')
        brk_pnt.write('\t\tprintf("----------------------------");\n')
        brk_pnt.write('\t\treturn 0;\n')
        brk_pnt.write('\t}\n')
            
        brk_pnt.write('\tif(bp2 == emu.bphandle)\n')
        brk_pnt.write('\t{\n')
        brk_pnt.write('\t\tprintf("FAILURE_2 at %s", test_name);\n')
        brk_pnt.write('\t\tprintf("----------------------------");\n')
        brk_pnt.write('\t\tprintf("----------------------------");\n')
        
        brk_pnt.write('\t\tfor(i=0; i < PORT_CNT; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "STTAB[%d]", i);\n')
        brk_pnt.write('\t\t\tSTTAB_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("STTAB[%d] = %#2X", i, STTAB_i);\n')
        brk_pnt.write('\t\t}\n')
        
        brk_pnt.write('\t\tfor(i=0; i < PORT_CNT; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "PTIMER[%d]", i);\n')
        brk_pnt.write('\t\t\tPTIMER_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("PTIMER[%d] = %#2X", i, PTIMER_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < PORT_CNT; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "P2TIMER[%d]", i);\n')
        brk_pnt.write('\t\t\tP2TIMER_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("P2TIMER[%d] = %#2X", i, P2TIMER_i);\n')
        brk_pnt.write('\t\t}\n')
        
        brk_pnt.write('\t\tfor(i=0; i < CHANCNT; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "XMITTAB[%d]", i);\n')
        brk_pnt.write('\t\t\tXMITTAB_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("XMITTAB[%d] = %#2X", i, XMITTAB_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < CHANCNT; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "XMIT2TAB[%d]", i);\n')
        brk_pnt.write('\t\t\tXMIT2TAB_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("XMIT2TAB[%d] = %#2X", i, XMIT2TAB_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < PORT_CNT; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "XMITTAB2[%d]", i);\n')
        brk_pnt.write('\t\t\tXMITTAB2_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("XMITTAB2[%d] = %#2X", i, XMITTAB2_i);\n')
        brk_pnt.write('\t\t}\n')
        
        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipDialogIndexMap[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipDialogIndexMap_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipDialogIndexMap[%d] = %#2X", i, voipDialogIndexMap_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipSIPSIPDialogPair[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipSIPSIPDialogPair_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipSIPSIPDialogPair[%d] = %#2X", i, voipSIPSIPDialogPair_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipTransDialogPair[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipTransDialogPair_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipTransDialogPair[%d] = %#2X", i, voipTransDialogPair_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipRTPType[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipRTPType_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipRTPType[%d] = %#2X", i, voipRTPType_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipReferredByName[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipReferredByName_i = TARGETreadword(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipReferredByName[%d] = %#4X", i, voipReferredByName_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipRefName[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipRefName_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipRefName[%d] = %#2X", i, voipRefName_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipPreReqStat[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipPreReqStat_i = TARGETreadword(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipPreReqStat[%d] = %#4X", i, voipPreReqStat_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipDialogTimer[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipDialogTimer_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipDialogTimer[%d] = %#2X", i, voipDialogTimer_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipHFTAB[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipHFTAB_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipHFTAB[%d] = %#2X", i, voipHFTAB_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT); i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipRingTab[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipRingTab_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipRingTab[%d] = %#2X", i, voipRingTab_i);\n')
        brk_pnt.write('\t\t}\n')
        
        brk_pnt.write('\t\tfor(i=0; i < PORT_CNT; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipDialogTab[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipDialogTab_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipDialogTab[%d] = %#2X", i, voipDialogTab_i);\n')
        brk_pnt.write('\t\t}\n')
        
        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT) * 3; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipSt[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipSt_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipSt[%d] = %#2X", i, voipSt_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT) * 3; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipFlag[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipFlag_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipFlag[%d] = %#2X", i, voipFlag_i);\n')
        brk_pnt.write('\t\t}\n')

        brk_pnt.write('\t\tfor(i=0; i < (DIALOG_CNT + REFERENCE_CNT) * 3; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "voipSttab[%d]", i);\n')
        brk_pnt.write('\t\t\tvoipSttab_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("voipSttab[%d] = %#2X", i, voipSttab_i);\n')
        brk_pnt.write('\t\t}\n')
        
        brk_pnt.write('\t\tfor(i=0; i < PORT_CNT; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "interEventTimer[%d]", i);\n')
        brk_pnt.write('\t\t\tinterEventTimer_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("interEventTimer[%d] = %#2X", i, interEventTimer_i);\n')
        brk_pnt.write('\t\t}\n')
        
        brk_pnt.write('\t\tfor(i=0; i < (TRKCNT + IPTRK_CNT) * 16; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "TRNUM[%d]", i);\n')
        brk_pnt.write('\t\t\tTRNUM_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("TRNUM[%d] = %#2X", i, TRNUM_i);\n')
        brk_pnt.write('\t\t}\n')
        
        brk_pnt.write('\t\tfor(i=0; i < MFRCNT * 2; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "MFCHIP[%d]", i);\n')
        brk_pnt.write('\t\t\tMFCHIP_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("MFCHIP[%d] = %#2X", i, MFCHIP_i);\n')
        brk_pnt.write('\t\t}\n')
        
        brk_pnt.write('\t\tfor(i=0; i < PORT_CNT; i++)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tvar_str = "";\n')
        brk_pnt.write('\t\t\tsprintf(var_str, "T3BYTE[%d]", i);\n')
        brk_pnt.write('\t\t\tT3BYTE_i = TARGETreadbyte(var_str);\n')
        brk_pnt.write('\t\t\tprintf("T3BYTE[%d] = %#2X", i, T3BYTE_i);\n')
        brk_pnt.write('\t\t}\n')
                                
        brk_pnt.write('\t\tprintf("----------------------------");\n')
        brk_pnt.write('\t\tprintf("----------------------------");\n')
        brk_pnt.write('\t\treturn 0;\n')
        brk_pnt.write('\t}\n')
        
        brk_pnt.write('\tif(bp3 == emu.bphandle)\n')
        brk_pnt.write('\t{\n')
        brk_pnt.write('\t\tprintf("FAILURE_3 at %s", test_name);\n')
        brk_pnt.write('\t\tprintf("voipSt[BX] = %d", TARGETreadbyte("voipSt[BX]"));\n')
        brk_pnt.write('\t\treturn 0;\n')
        brk_pnt.write('\t}\n')
        brk_pnt.write('\telse\n')
        brk_pnt.write('\t{\n')
        brk_pnt.write('\t\tprintf("success at %s", test_name);\n')
        brk_pnt.write('\t\tsuccess_count++;\n')
        brk_pnt.write('\t\ttime_end[runto_count] = PSLticks();\n')
        brk_pnt.write('\t\tx = (time_end[runto_count]*10)/182;\n')
        brk_pnt.write('\t\ty = (time_end[runto_count - 1]*10)/182;\n')
        brk_pnt.write('\t\tif(runto_count != 0)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tprintf("test[%d of %d] duration: %ld secs", success_count, MAX_RUNTO_CNT, x - y);\n')
        brk_pnt.write('\t\t}\n')
        brk_pnt.write('\t\treturn 1;\n')
        brk_pnt.write('\t}\n')
        brk_pnt.write('}\n')
        brk_pnt.write('}\n\n')
        
        brk_pnt.write('int runto(line_no)\n')
        brk_pnt.write('{\n')
        brk_pnt.write('\tDEBUGrunto(line_no);\n')
        brk_pnt.write('}\n\n')
        
        brk_pnt.write('runto_count = 0;\n')
        brk_pnt.write('success_count = -1;\n\n')
            
        brk_pnt.write('DEBUGrunto("fhw#44");\n')
        brk_pnt.write('TARGETwriteword("cmd", 0xa000);\n\n')

        brk_pnt.write('if(DEBUGcontrol("fhw"))\n')
        brk_pnt.write('{\n')
        brk_pnt.write('\tdo\n')
        brk_pnt.write('\t{\n')
        brk_pnt.write('\t\ttime_end[runto_count] = PSLticks();\n')
        brk_pnt.write('\t\tif(runto_count >= MAX_RUNTO_CNT)\n')
        brk_pnt.write('\t\t{\n')
        brk_pnt.write('\t\t\tbreak;\n')
        brk_pnt.write('\t\t}\n')
        brk_pnt.write('\t\trunto(line_no_arr[runto_count]);\n')
        brk_pnt.write('\t}\n')
        brk_pnt.write('while(DEBUGcontrol(test_name_arr[runto_count++]) == 1)\n')
        brk_pnt.write('}\n\n')
        brk_pnt.write('printf("%d of %d tests completed", success_count, MAX_RUNTO_CNT);\n\n')

        brk_pnt.write('printf("END OF THE TEST");\n\n')
        brk_pnt.write('PSLlogging(0);\n')

        brk_pnt.close()
        belge.close()
        fhw.close()

    if(ctrl == 2 or ctrl == 3 or ctrl == 6 or ctrl == 7):
        derle_test = test_name.upper()
        derle = 'do48 r -B -DUTEST -D' + derle_test + ' > ' + 'MS_' + derle_test + '_BUILD.log' 
        test_env = os.getenv('test_env')
        os.chdir(test_env)
        os.chdir('..')
        os.system(derle)

    if(ctrl == 4 or ctrl == 5 or ctrl == 6 or ctrl == 7):
        test_env = os.getenv('test_env')
        os.chdir(test_env)
        os.chdir('..')
        target = os.getenv('target')
        target = target + ' ms'
        os.system(target)

for test_name in curr_test_arr:
    
    class Client1Thread(threading.Thread):
            
        def __init__(self):
                    
            threading.Thread.__init__(self)
                    
        def run(self):
                    
            gogogo(test_name, test_code)
                    
    threadOne = Client1Thread()
    threadOne.start()
    start_time = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    time.sleep(10)

    if(test_code > 3):
        test_env = os.getenv('test_env')
        os.chdir(test_env)
        os.chdir('..')
        ctrl_brk = 1
        fail_brk = 'END OF THE TEST'
        log_file = 'MS_' + test_name.upper() + '.txt'
        ret = os.access(log_file,os.F_OK);
        while(False == ret):
            ret = os.access(log_file,os.F_OK);
            time.sleep(1)
        logfile = open(log_file, 'r')

        while(ctrl_brk != 0):
            logfile.seek(0)
            time.sleep(0.1)
            for j in range(len(logfile.read())*2):
                logfile.seek(j)
                oku = logfile.read(len(fail_brk))
                if(oku == fail_brk):
                    ctrl_brk = 0
                    end_time = strftime("%a, %d %b %Y %H:%M:%S", localtime())
                    ms_log = open(log_file, 'a')
                    ms_log.write('\n\nstarted   at ' + start_time + '\nfinished  at ' + end_time)
                    ms_log.close()
                    os.system(r"taskkill /F /IM ntvdm.exe")

        logfile.close()
