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
import fileinput

def main():
    pass

if __name__ == '__main__':
    main()
    
    
    
blacklistlines = [1]
    
fp=open("file.txt","r")
fp2=open("out.json","w")
fp2.write('{\n')
name=fp.readline()
fp2.write('"Basic Details": {\n')
fp2.write('\t"Name": "' + name[:-1] + '",\n')

emailline=1
emaillist=[]

while 1:
    line=fp.readline()
    emailline+=1
    if not line:
        break
    i=0
    while i!=len(line):
        if line[i]=='@':
            break
        i=i+1
    if i!=len(line):
        left=i
        while line[left]!=' ':
            left=left-1
            if left==0:
                break
        right=i
        while line[right]!=' ':
            right=right+1
            if right==len(line):
                break
         
        if len(line) >= right-1 and (line[right-1].isalpha() or line[right-1].isdigit()):
            right +=1
        
        email=line[left:right-1]
        emaillist.append(email)
        #fp2.write('\t{"Email ID": "' + email + '"},\n')
        blacklistlines.append(emailline)

if len(emaillist)>1:
    fp2.write('\t"Email ID": ["' + '", "'.join(emaillist) + '"],\n')
else:
    fp2.write('\t"Email ID": "' + '", "'.join(emaillist) + '",\n')
fp.close()

fp=open("file.txt","r")

phonelist=[]
phoneline=0


while 1:
    line=fp.readline()
    phoneline+=1 
    if not line:
        break
    if phoneline not in blacklistlines:

        i=0
        while i!=len(line):
            if line[i].isdigit()==1:
                j=1
                test=1
                while j!=10:
                    if line[i+j].isdigit()!=1:
                        test=0
                        break
                    j=j+1
                if test==1:
                    phone=line[i:len(line)]
                    #fp2.write('\t{"Phone Number": "' + phone[:-1] + '"},\n]')
                    phonelist.append((phone[:-1]))
                    blacklistlines.append(phoneline)
                    break
            i=i+1

if len(phonelist)>1:
        fp2.write('\t"Phone Number": ["' + '", "'.join(phonelist) + '"]\n}')
else:
        fp2.write('\t"Phone Number": "' + '", "'.join(phonelist) + '"\n}')    
fp.close()    
        
fp=open("file.txt","r")

line=fp.readline()

line=fp.readline()
linenumber = 1
o=0
while len(line)>1:
    linenumber += 1
   
    if linenumber in blacklistlines:
        line=fp.readline()
   
    else :
        if (line.find(':') is -1):
            o=o+1
            fp2.write(',\n\t"Detail'+str(o)+'":"'+ line[0:-1] + '"' )
        else:
            tmp = line.find(':')
            fp2.write(',\n\t"' + line[0:tmp] + '": "' + line[tmp+1:-1] + '"' )
        line=fp.readline()
    
fp2.write('\n}\n')
linenumber += 1

while 1:
    line=fp.readline()
    linenumber += 1
    
    if linenumber in blacklistlines:
        continue
    
    k=0
    while len(line)==1 and k<10:#k is for checking infinite loop
        line=fp.readline()
        linenumber += 1
        k=k+1

    if linenumber in blacklistlines:
        continue    

    if k==10:
        break
    if not line:
        break
    
    fp2.write('{\n')
    fp2.write('\t"'+line[0:-1]+'":[\n')
    line=fp.readline()
    linenumber += 1
    
    if linenumber in blacklistlines:
        continue

    k=0
    while len(line)==1 and k<5:#k is for checking infinite loop
        line=fp.readline()
        linenumber += 1
    
        if linenumber in blacklistlines:
            continue

        k=k+1

    if linenumber in blacklistlines:
        continue    

    if k==5:
        print 'blank resume'
        fp2.write('\t{"Blank":"Blank"}\n]}')
        break
    k=0
    j=0
    p=ord(line[0])
    while not((p>=65 and p<=90)or(p>=97 and p<=122)or(p>=48 and p<=57)):#check infinite loop of k
        if j>5:
            print 'blank resume'
            fp2.write('\t{"Blank":"Blank"}\n]}')
            break
        if line[k]=='\n':
            j=j+1
            line=fp.readline()
            linenumber += 1
            
            if linenumber in blacklistlines:
                continue    

            k=-1
        k=k+1
        p=ord(line[k])

    if linenumber in blacklistlines:
        continue    
    
    if j>5:
        break
    fp2.write('\t{"Detail1":"'+line[k:-1])
    line=fp.readline()
    linenumber += 1

    if linenumber in blacklistlines:
        continue

    k=0
    o=1
    while 1:
        if ((line[k]==' 'or line[k]=='\t')and k<5 and k<len(line)):
            k=k+1
        p=ord(line[k])           
        if p>=97 and p<=122:
            fp2.write(' '+line[k:-1])
            line=fp.readline()
            linenumber += 1
        
            if linenumber in blacklistlines:
                continue

            k=0
            continue
        k=0
        while k<len(line) and k<10:
            p=ord(line[k])              
            if (p>=65 and p<=90)or(p>=97 and p<=122)or(p>=48 and p<=57):
                break
            else:
                k=k+1
        if k==10 or k==len(line):
            fp2.write('"}\n]}\n')
            break
        else:
            #o=o+1
            #fp2.write('"},\n\t{"Detail'+str(o)+'":"'+line[k:-1])
            if (line[k:-1].find(':') is -1):
                o=o+1
                fp2.write('"},\n\t{"Detail'+str(o)+'":"'+ line[k:-1])
            else:
                tmp = line[k:-1].find(':')
                fp2.write('"},\n\t{"' + line[k:tmp] + '": "' + line[tmp+1:-1])
            line=fp.readline()
            linenumber += 1
        
            if linenumber in blacklistlines:
                continue

            k=0  
                
fp.close()
fp2.close()
