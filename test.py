#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Hemu
#
# Created:     12/04/2014
# Copyright:   (c) Hemu 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import string
import subprocess
from subprocess import call
w=raw_input()
if w[-1]=='f':
	subprocess.call('python pdf2txt.py '+w+' > file.txt', shell=True)
elif w[-1]=='c':
	subprocess.call('lowriter --convert-to pdf '+w, shell=True)
	subprocess.call('python pdf2txt.py '+w[:-3]+'pdf > file.txt', shell=True)
else:
	subprocess.call('cp '+w+' file.txt', shell=True)
import fileinput

def main():
    pass

if __name__ == '__main__':
    main()
fp=open("file.txt","r")
fp2=open("out.json","w")
fp2.write('{\n')
b=1
line=fp.readline()
fp2.write('"' + line[0:-1] + '": {\n' )

line=fp.readline()
fp2.write('\t"Name": "' + line[0:-1] + '",\n' )

line=fp.readline()
fp2.write('\t"Phone": "' + line[0:-1] + '",\n' )

line=fp.readline()
fp2.write('\t"Email ID": "' + line[0:-1] + '",\n' )

fp2.write('},\n')
while 1:
    line=fp.readline()
    if not line:
        break
    if len(line)==1:
        a=1
    elif not(line[0]>='1' and line[0]<='9'):
        if b==0:
            fp2.write('},\n"')
        b=0
        fp2.write(line[0:-1] + '": {\n')
    else:
        i=0
        while line[i]!='.':
            i=i+1
        fp2.write('\t"' + line[i+2:-1] + '",\n')

fp2.write('},\n}')
fp.close()
fp2.close()
