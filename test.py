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
	subprocess.call('python pdf2txt.py '+fileName+' > file1.txt', shell = True)
elif fileName[-1]=='c':
	subprocess.call('lowriter --convert-to pdf '+fileName, shell = True)
	subprocess.call('python pdf2txt.py '+fileName[:-3]+'pdf > file1.txt', shell = True)

else:
	subprocess.call('cp '+fileName+' file1.txt', shell = True)

def match(sentence, array , numberofwords):
    i=0
    left=-1
    right=-1
    ident=0
    while i<len(sentence):
        if ((ord(sentence[i])>64 and ord(sentence[i])<91) or (ord(sentence[i])>96 and ord(sentence[i])<123)) and ident==0:
            ident=1
            left=i
        if ord(sentence[i])==58:
            right=i
        i=i+1
    j=0
    while j<numberofwords:
        if sentence[left:right].lower()==array[j]:
            return [left,right]
        j=j+1
    return [-1,-1]

def check_for_empty_spaces(line):
    if not line:
        return -2
    index=0
    while (line[index] == ' ' or line[index] is '\t'):
        if index==len(line):
            return -3
        index=index+1
    return index

def empty_lines_and_spaces(finput,mylist):
    index=mylist[0]
    line=mylist[1]
    linenumber=mylist[2]
    numberOfBlankLines=mylist[3]
    mylist=[-1,line,linenumber,numberOfBlankLines]
    while 1:
        if not line or numberOfBlankLines>1000:
            return mylist
        else:
            while index!=len(line):
                p=ord(line[index])
                if ((p>64 and p<91) or (p>96 and p<123) or (p>47 and p<58)):
                    mylist[0]=index
                    return mylist
                index += 1
        line = fInput.readline()
        linenumber += 1
        numberOfBlankLines += 1
        index=0
        mylist=[-1,line,linenumber,numberOfBlankLines]

def main():
    pass

if __name__ == '__main__':
    main()
    
    
subprocess.call('python clean_spaces.py file1.txt file.txt', shell = True)
blacklistlines = [1]
    
fInput = open("file.txt","r")
fOutput = open("out.json","w")
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

array=['education', 'courses completed', 'projects undertaken', 'achievements', 'computer Skills', 'activities','personal details', 'personal strengths', 'personal profile', 'precis',   


'academic details', 'important course work', 'lab', 'labs', 'academia', 'academic qualifications', 'academic credentials',


'work experience', 'professional experience', 'experience', 'chronology', 'recent achievements', 'notable achievements', 'notable attainments', 'projects undertaken', 'project undertaken', 'projects executed',


'skills', 'highlights of qualifications', 'technical skill set',  'computer skill', 'computer literacy', 'technical skills', 'technical certifiaction',

'others', 'objective declaration', 'other', 'details summary', 'professional summary', 'some hobbies', 'few hobbies', 'extracurricular activities']
numberofwords=6
l=0
index=0
numberOfBlankLines=0
mylist=[index,line,linenumber,numberOfBlankLines]
     
mylist=empty_lines_and_spaces(fInput,mylist)
index=mylist[0]
line=mylist[1]
linenumber=mylist[2]
numberOfBlackLines=mylist[3]
llist=match(line,array,numberofwords);
while 1:
    if index==-1:
        break
    if llist[0]!=-1:
        break 
    if l==0:
        fOutput.write(',\n"More Details":{\n')
        l=l+1
    if (line.find(':') is -1):
        if l==1:
            fOutput.write('\t"Detail'+str(detailNumber)+'":"'+line[index:-1])
            l=l+1
        else:
            fOutput.write(',\n\t"Detail'+str(detailNumber)+'":"'+line[index:-1])
        detailNumber = detailNumber + 1
    else:
        indexOfColon = line.find(':')
        if l==1:
            fOutput.write('\t"' + line[index:indexOfColon] + '": "' + line[indexOfColon + 1:-1])
        else:
            fOutput.write(',\n\t"' + line[index:indexOfColon] + '": "' + line[indexOfColon + 1:-1])
    line=fInput.readline()
    linenumber += 1
    llist=match(line,array,numberofwords)
    index=check_for_empty_spaces(line)
    while llist[0]==-1 and index>=0:
        p=ord(line[index])
        index=-1
        if p>=97 and p<=122:
            fOutput.write(' '+line[index:-1])
            line=fInput.readline()
            linenumber += 1
            llist=match(line,array,numberofwords)
            index=check_for_empty_spaces(line) 
    fOutput.write('"')
    while 1:
        if llist[0]!=-1:
            break
        index=0
        numberOfBlankLines=0
        mylist=[index,line,linenumber,numberOfBlankLines]
        mylist=empty_lines_and_spaces(fInput,mylist)
        index=mylist[0]
        line=mylist[1]
        linenumber=mylist[2]
        numberOfBlackLines=mylist[3]
        llist=match(line,array,numberofwords)
        if linenumber in blacklistlines:
            line=fInput.readline()
            linenumber += 1
            llist=match(line,array,numberofwords)
        else:
            break 
    if llist[0]!=-1:
        break
    if index==-1:
        break
if l==2:
    fOutput.write('\n}')    



while 1:
    if index==-1:
        break
    fOutput.write(',\n"' + line[llist[0]:llist[1]] + '":{\n')
    
    detail_no=1
    if llist[1]!=-1:
        fOutput.write('\t"Detail'+str(detail_no)+'":"'+line[llist[1]:-1])
        detail_no=detail_no+1
        line=fInput.readline()
        linenumber += 1
        llist=match(line,array,numberofwords)
        index=check_for_empty_spaces(line)
        while llist[0]==-1 and index>=0:
            p=ord(line[index])
            index=-1
            if p>=97 and p<=122:
                fOutput.write(' '+line[index:-1])
                line=fInput.readline()
                linenumber += 1
                llist=match(line,array,numberofwords)
                index=check_for_empty_spaces(line)        
        fOutput.write('"')
        
    index=0
    line = fInput.readline()
    linenumber = linenumber + 1
    numberOfBlankLines = 0 
    
    while linenumber in blacklistlines:
        line = fInput.readline()
        linenumber = linenumber + 1

    mylist=[index,line,linenumber,numberOfBlankLines]
    
    #empty_lines_and_spaces discards any empty lines and empty spaces 
    mylist=empty_lines_and_spaces(fInput,mylist)
    index=mylist[0]
    line=mylist[1]
    linenumber=mylist[2]
    numberOfBlackLines=mylist[3]
    
    if index==-1:
        fOutput.write('\n}')
        break
    if detail_no==1:
        fOutput.write('\t"Detail'+str(detail_no)+'":"'+line[index:-1])
    else:
        fOutput.write(',\n\t"Detail'+str(detail_no)+'":"'+line[index:-1])
    while 1:
        line=fInput.readline()
        linenumber += 1
        llist=match(line,array,numberofwords)
        index=check_for_empty_spaces(line)
        while llist[0]==-1 and index>=0:
            p=ord(line[index])
            index=-1
            if p>=97 and p<=122:
                fOutput.write(' '+line[index:-1])
                line=fInput.readline()
                linenumber += 1
                llist=match(line,array,numberofwords)
                index=check_for_empty_spaces(line) 
        fOutput.write('"')
        if llist[0]!=-1:
            break
        mylist=[0,line,linenumber,0]
    
    #empty_lines_and_spaces discards any empty lines and empty spaces 
        mylist=empty_lines_and_spaces(fInput,mylist)
        index=mylist[0]
        line=mylist[1]
        linenumber=mylist[2]
        numberOfBlackLines=mylist[3]
        if index==-1:
            break
        llist=match(line,array,numberofwords)
        if llist[0]!=-1:
            fOutput.write('\n}')
            break
        detail_no=detail_no+1
        fOutput.write(',\n\t"Detail'+str(detail_no)+'":"'+line[index:-1])
    if index==-1:
        fOutput.write('\n}')
        break
fOutput.write('\n}')
fInput.close()
fOutput.close()
