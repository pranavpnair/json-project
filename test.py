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
#import pdf2txt
import fileinput
from modules import *

w=raw_input()
if w[-1]=='f':
	subprocess.call('python pdf2txt.py '+w+' > file.txt', shell=True)
	#pdf2txt.main({w})
elif w[-1]=='c':
	subprocess.call('lowriter --convert-to pdf '+w, shell=True)
	subprocess.call('python pdf2txt.py '+w[:-3]+'pdf > file.txt', shell=True)
	#pdf2txt.main({w[:-3]+'pdf'})
else:
	subprocess.call('cp '+w+' file.txt', shell=True)

def main():
    pass

if __name__ == '__main__':
    main()
    
    
    
blacklistlines = [1]
    
fInput=open("file.txt","r")
fOutput=open("out.json","w")
fOutput.write('{\n')

#Name extraction

line=fInput.readline()
fOutput.write('"Basic Details": {\n')
fOutput.write('\t"Name": "' + line[:-1] + '",\n')


#Email Extraction
emailline=1
emaillist=[]

line=fInput.readline()
while line:
    emailline+=1
    email = extract_email(line)
        emaillist.append(email)
        blacklistlines.append(emailline)
    line=fInput.readline()

if len(emaillist)>1:
    fOutput.write('\t"Email ID": ["' + '", "'.join(emaillist) + '"],\n')
else:
    fOutput.write('\t"Email ID": "' + '", "'.join(emaillist) + '",\n')
fInput.close()



#Phone number extraction

fInput=open("file.txt","r")

phonelist=[]
phoneline=0
line=fInput.readline()

while line:
    phoneline+=1 
    if phoneline in blacklistlines:
        line=fInput.readline()
        continue
    extract_phone(line)
    line=fInput.readline()


#Details

if len(phonelist)>1:
        fOutput.write('\t"Phone Number": ["' + '", "'.join(phonelist) + '"]\n}')
else:
        fOutput.write('\t"Phone Number": "' + '", "'.join(phonelist) + '"}\n}')    
fInput.close()    
        
fInput=open("file.txt","r")

line=fInput.readline()

line=fInput.readline()
linenumber = 1
o=0

while len(line)>1:
    linenumber += 1
    fOutput.write('{\n"More_Details:"{\n')
    if linenumber in blacklistlines:
        line=fInput.readline()
   
    else :
        if (line.find(':') is -1):
            o=o+1
            fOutput.write('\t"Detail'+str(o)+'":"'+ line[0:-1] + '",\n' )
        else:
            tmp = line.find(':')
            fOutput.write('\t"' + line[0:tmp] + '": "' + line[tmp+1:-1] + '",\n' )
        line=fInput.readline()
    fOutput.write('}\n}')    

linenumber += 1

while 1:
    line=fInput.readline()
    linenumber += 1
    
    if linenumber in blacklistlines:
        continue
    
    k=0
    while len(line)==1 and k<1000:#k is for checking infinite loop
        line=fInput.readline()
        linenumber += 1
        k=k+1

    if linenumber in blacklistlines:
        continue    

    if k==1000:
        break
    if not line:
        break
    j=0
    k=0
    while (line[k]==' 'or line[k]=='\t'):
        if j==1000:
            print 'blank resume'
            fOutput.write('\t{"Blank":"Blank"}\n]}')
            break
        if k==len(line):
            j=j+1
            k=-1
            line=fInput.readline()
            linenumber += 1
        k=k+1 
    if j==1000:
        break
    k=0
    fOutput.write('{\n')
    fOutput.write('\t"'+line[0:-1]+'":[\n')
    line=fInput.readline()
    linenumber += 1
    
    if linenumber in blacklistlines:
        continue

    k=0
    while len(line)==1 and k<1000:#k is for checking infinite loop
        line=fInput.readline()
        linenumber += 1
    
        if linenumber in blacklistlines:
            continue

        k=k+1

    if linenumber in blacklistlines:
        continue    

    if k==1000:
        print 'blank resume'
        fOutput.write('\t{"Blank":"Blank"}\n]}')
        break
    k=0
    j=0
    if not line:
        break
    p=ord(line[0])
    while not((p>=65 and p<=90)or(p>=97 and p<=122)or(p>=48 and p<=57)):#check infinite loop of k
        if k==len(line):
            j=j+1
            line=fInput.readline()
            if linenumber in blacklistlines:
                continue    
            k=-1
            linenumber += 1
        if j>1000:
            print 'blank resume'
            fOutput.write('\t{"Blank":"Blank"}\n]}')
            break
        if line[k]=='\n':
            j=j+1
            line=fInput.readline()
            linenumber += 1
            
            if linenumber in blacklistlines:
                continue    

            k=-1
        k=k+1
        p=ord(line[k])
    if j>1000:
        break
    if linenumber in blacklistlines:
        continue    
    
    fOutput.write('\t{"Detail1":"'+line[k:-1])
    line=fInput.readline()
    linenumber += 1

    if linenumber in blacklistlines:
        continue

    k=0
    o=1
    while 1:
        if ((line[k]==' 'or line[k]=='\t')and k<1000 and k<len(line)):
            k=k+1
        p=ord(line[k])           
        if p>=97 and p<=122:
            fOutput.write(' '+line[k:-1])
            line=fInput.readline()
            linenumber += 1
        
            if linenumber in blacklistlines:
                continue

            k=0
            continue
        k=0
        while k<len(line) and k<1000:
            p=ord(line[k])              
            if (p>=65 and p<=90)or(p>=97 and p<=122)or(p>=48 and p<=57):
                break
            else:
                k=k+1
        if k==1000 or k==len(line):
            fOutput.write('"}\n]}\n')
            break
        else:
            #o=o+1
            #fOutput.write('"},\n\t{"Detail'+str(o)+'":"'+line[k:-1])
            if (line[k:-1].find(':') is -1):
                o=o+1
                fOutput.write('"},\n\t{"Detail'+str(o)+'":"'+ line[k:-1])
            else:
                tmp = line[k:-1].find(':')
                fOutput.write('"},\n\t{"' + line[k:tmp] + '": "' + line[tmp+1:-1])
            line=fInput.readline()
            linenumber += 1
        
            if linenumber in blacklistlines:
                continue

            k=0  
                
fInput.close()
fOutput.close()
