import os
import pickle
import re
from colorama import Fore, Back, Style, init
from optparse import OptionParser
from itertools import groupby


#COLORAMA
'''
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
'''
#colorama init
init()

headline=Fore.GREEN
done_col=Fore.CYAN
done_user=Fore.GREEN
done_category=Fore.RED
pending_col=Fore.MAGENTA
pending_user=Fore.GREEN
pending_category=Fore.RED
reset_font=Fore.RESET

back=Back.BLUE
reset_back=Back.RESET

bright=Style.BRIGHT
reset_style=Style.RESET_ALL


parser = OptionParser()
PATH='D:/tutorial/python/training/source_code'
FILE='toDo_4.dmp'
os.chdir(PATH)
l=[]


#OPTIONS
parser.add_option("-a", "--add",
                  help="add to list",
                  action="store_const", const='a', dest="opt")
parser.add_option("-l", "--list",
                  help="prints out the toDo list",
                  action="store_const", const='l', dest="opt")
parser.add_option("-g", "--byCategory",
                  help="prints out the toDo list grouped by category",
                  action="store_const", const='g', dest="opt")
parser.add_option("-u", "--byUser",
                  help="prints out the toDo list grouped by User",
                  action="store_const", const='u', dest="opt")
parser.add_option("-t", "--toggle",
                  help="toggle the todo list",
                  action="store_const", const='t', dest="opt")
parser.add_option("-p", "--pending",
                  help="prints the pending toDo list",
                  action="store_const", const='p', dest="opt",
                  )
parser.add_option("-c", "--completed",
                  help="prints the completed toDo list",
                  action="store_const", const='c', dest="opt")
parser.add_option("-d", "--delete",
                  help="clean toDo list",
                  action="store_const", const='d', dest="opt")
parser.add_option("-z", "--test",
                  help="clean toDo list",
                  action="store_const", const='d', dest="opt")
                  #action="store", type='string', dest="val")

'''Add new entries to the list'''
def addToList(lis,text):
    task_category=re.search(r'\+([a-z,A-Z, ]{1,})',text)
    task_person=re.search(r'@([a-z,A-Z, ]{1,})',text)
    if task_person and task_category:
        lis.append([text,'Y',task_person.group(1),task_category.group(1)])
        
    elif task_person and not task_category:
        lis.append([text,'Y',task_person.group(1),''])
        
    elif not task_person and task_category:
        lis.append([text,'Y','',task_category.group(1)])
        
    else:
        lis.append([text,'Y','',''])
        
'''Read the list file'''
def read():
    lis=[]
    try:
        with open(FILE,"r") as f:
            lis=pickle.load(f)
            return lis
            
    except EnvironmentError:
        with open(FILE,"w") as f:
            return lis
    except EOFError:
        return []



'''Print the list'''
def printL(lis,option='b'):
    print headline, bright, 'LIST OF ToDo :',reset_font
    #print lis
    for num,note in enumerate(lis,start=1):
        if option=='b':
            if note[1]=='N':
                print done_col, bright, num,' : ', note[0], \
                      done_user, note[2], done_category, note[3], reset_font
            else:
                print pending_col, bright, num,' : ',note[0],\
                      pending_user, note[2], pending_category, note[3], reset_font
                
        elif option=='c':
            if note[1]=='N':
                print done_col, bright, num,' : ', note[0],\
                      done_user, note[2], done_category, note[3], reset_font
                
        elif option=='p':   
            if note[1]=='Y':
                print pending_col, bright, num,' : ',note[0],\
                      pending_user, note[2], pending_category, note[3], reset_font

'''print by group by category[3] / User[2] (default ->category[3])'''
def printByCategoryOrUser(lis,groupon=3):
    print headline, bright, 'LIST OF ToDo',reset_font,
    if groupon == 3:
        print headline, bright, 'GROUPED BY CATEGORY ',reset_font
    elif groupon == 2:
        print headline, bright, 'GROUPED BY USER ',reset_font
    for category, l_byCategory in groupby(lis, key=lambda x: x[groupon]):
        print headline, bright, category
        
        for num,single_items in enumerate(l_byCategory, start=1):
            
            if single_items[1]=='N':
                print done_col, bright, num,' : ', single_items[0], \
                      done_user, single_items[2], done_category, single_items[3], reset_font
            else:
                print pending_col, bright, num,' : ', single_items[0], \
                      pending_user, single_items[2], pending_category, single_items[3], reset_font

'''Write into the list'''
def write(lis):
    with open(FILE,"w") as f:
        pickle.dump(lis,f)

'''Toggle the status of a single entry'''
def toggle(lis,pos):
    if lis[pos][1]=='Y':
        lis[pos][1]='N'
    else:
        lis[pos][1]='Y'


(options, args) = parser.parse_args()

l=read()    
opt=options.opt

if opt=='a':
    for text in args:        
        addToList(l,text)
    write(l)

elif opt=='l':
    printL(l,'b')

elif opt=='g':
    printByCategoryOrUser(l,3)

elif opt=='u':
    printByCategoryOrUser(l,2)
    
elif opt=='t':
    write(l)
    for text in args:
        toggle(l,int(text)-1)   
    write(l)
    printL(l,'b')
    
elif opt=='c':
    printL(l,'c')
    
elif opt=='p':
    printL(l,'p')

elif opt=='d':
    l=[]
    write(l)
