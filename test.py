# Author:  Ajay,Hemant,Naga Varun,Pratik,Pranav    
# Name:	RESUME PARSER
# Purpose: INTERNSHIP
# Created:  24/06/2014

import string
import subprocess
import fileinput
from subprocess import call
from modules import *

fileName = raw_input()

if (fileName[-1] == 'f'):
	subprocess.call('python pdf2txt.py '+fileName+' > file.txt', shell = True)
elif fileName[-1]=='c':
	subprocess.call('lowriter --convert-to pdf '+fileName, shell = True)
	subprocess.call('python pdf2txt.py '+fileName[:-3]+'pdf > file.txt', shell = True)

else:
	subprocess.call('cp '+fileName+' file.txt', shell = True)

def main():
    pass

if __name__ == '__main__':
    main()
    
    
    
blacklistlines = [1]
    
fInput = open("file.txt","r")
fOutput = open("out.json","fileName")
fOutput.write('{\n')

#Name extraction

line = fInput.readline()
fOutput.write('"Basic Details": {\n')
fOutput.write('\t"Name": "' + line[:-1] + '",\n')


#Email Extraction

emailline = 1
emaillist = []

line = fInput.readline()

while line:
    emailline = emailline + 1
    email = extract_email(line)
    if email is not None:
    	emaillist.append(email) 
    	blacklistlines.append(emailline)
    line=fInput.readline()

if len(emaillist)>1:
    fOutput.write('\t"Email ID": ["' + '", "'.join(emaillist) + '"],\n')
else:
    fOutput.write('\t"Email ID": "' + '", "'.join(emaillist) + '",\n')
fInput.close()



#Phone Number Extraction

fInput = open("file.txt","r")

phonelist = []
phoneline = 0
line = fInput.readline()

while line:
    phoneline = phoneline + 1 
    if phoneline in blacklistlines:
        line = fInput.readline()
        continue
    phone = extract_phone(line)
    if phone is not None:
    	phonelist.append(phone)
    	blacklistlines.append(phoneline)
    line=fInput.readline()


#Basic Details Extraction

if len(phonelist)>1:
        fOutput.write('\t"Phone Number": ["' + '", "'.join(phonelist) + '"]\n}')
else:
        fOutput.write('\t"Phone Number": "' + '", "'.join(phonelist) + '"\n}')    

fInput.close()    
        
fInput = open("file.txt","r")

line = fInput.readline()

line = fInput.readline()
linenumber = 2

detailNumber = 1

#More Details Extraction

fOutput.write('\n"More Details:"{\n')

while (len(line)>1):
    if linenumber in blacklistlines:
        line = fInput.readline()
   
    else :
        if (line.find(':') is -1):
        	fOutput.write('\t"Detail'+str(detailNumber)+'":"'+ line[0:-1] + '",\n' )
        	detailNumber = detailNumber + 1
        else:
            indexOfColon = line.find(':')
            fOutput.write('\t"' + line[0:indexOfColon] + '": "' + line[indexOfColon + 1:-1] + '",\n' )
        line = fInput.readline()
        
    linenumber = linenumber + 1

fOutput.write('}\n')    



while 1:
    line = fInput.readline()
    linenumber = linenumber + 1
    
    if linenumber in blacklistlines:
        continue
    
    numberOfBlankLines = 0
    
    while (len(line)==1 and numberOfBlankLines<1000): #numberOfBlankLines is for checking infinite loop
        line = fInput.readline()
        linenumber = linenumber + 1
        numberOfBlankLines = numberOfBlankLines + 1

    if (linenumber in blacklistlines):
        continue    

    if (numberOfBlankLines is 1000):
        break
        
    if not line:
        break
    
    numberOfBlankLines = 0
    index = 0
    
    while (line[index] == ' ' or line[index] is '\t'):
        if numberOfBlankLines is 1000:
            fOutput.write('\t{"Blank":"Blank"}\n]}')
            break
        
        if index==len(line):
            numberOfBlankLines = numberOfBlankLines + 1
            index = -1
            line=fInput.readline()
            linenumber = linenumber + 1
        index = index + 1 
    
    if numberOfBlankLines is 1000:
        break
    
    numberOfBlankLines = 0
    
    fOutput.write('{\n')
    fOutput.write('\t"' + line[0:-1] + '":[\n')
    
    line = fInput.readline()
    linenumber = linenumber + 1
    
    if linenumber in blacklistlines:
        continue

    numberOfBlankLines = 0
    
    while (len(line) == 1 and numberOfBlankLines < 1000):  #numberOfBlankLines is for checking infinite loop
        line=fInput.readline()
        linenumber = linenumber + 1
        numberOfBlankLines = numberOfBlankLines + 1

    if linenumber in blacklistlines:
        continue    

    if numberOfBlankLines == 1000:
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
    detailNumber=1
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
            #detailNumber=detailNumber+1
            #fOutput.write('"},\n\t{"Detail'+str(detailNumber)+'":"'+line[k:-1])
            if (line[k:-1].find(':') is -1):
                detailNumber=detailNumber+1
                fOutput.write('"},\n\t{"Detail'+str(detailNumber)+'":"'+ line[k:-1])
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
