def extract_email(line):
    i=0
    while i!=len(line) and line[i] is not '@':
        i+=1
    
    if i!=len(line):
        left=i
        while line[left]!=' ' and left is not 0:
            left-=1
        right=i
        while right is not len(line) and line[right]!=' ':
            right+=1
        
        if len(line) >= right-1 and (line[right-1].isalpha() or line[right-1].isdigit()):
            right +=1
        
        return line[left:right-1].strip()
    
    else: return None
    
    
def extract_phone(line):
    i=0
    while i!=len(line):
        if line[i].isdigit():
            j=1
            test=1
            while j!=10:
                if line[i+j].isdigit()!=1:
                    test=0
                    break
                j=j+1
            if test is 1:
                phone=line[i:len(line)]
                #fOutput.write('\t{"Phone Number": "' + phone[:-1] + '"},\n]')
                return phone[:-1].strip()
        i=i+1
    
    return None
