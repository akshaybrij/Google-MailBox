from tkinter import *
import manipulator
import gmail_read
import tkinter as tk
import ruler
import json
from datetime import timedelta, datetime
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id =  'me'
root=Tk()
root.title("MailBox")
mn=manipulator.Manipulator()
rl=ruler.Ruler()

def callback(param,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11):
    pr1=[]
    pr2=[]
    pr3=[]
    pr4=[]
    pr5=[]
    pr6=[]
    if param == "contains":
        pr1=mn.contains(param5,0)
        #print pr1

    if param == "not equal":
        pr1=mn.notequals(param5,0)
        #print pr1

    if param == "equal":
        pr1=mn.equals(param5,0)
        print pr1

    if param2 == "Subject":
        pr2=mn.contains(param6,3)
    #    print pr2

    if param2 == "Message":
        pr2=mn.contains(param6,4)
    #    print pr2

    if param4 == "equal to":
        param7=int(param7)*-1
    #    pr3=mn.date_equals(param7)

    if param4 == "less than":
        param7=int(param7)*-1
    #   print param7
        pr3=mn.date_lessrthan(param7)
        #print pr3

    if param1 == "All":
        pr4= set(pr1+pr2)
        pr5= set(pr3)
        pr6=list(set(pr4).intersection(pr5))
#        print pr6

    if param1 == "Any":
        pr6=list(set(pr1+pr2+pr3))
#        print pr6

    if param8 == "Move as Read":
        xl=rl.MakeAsRead()
        for msggs in pr6:
            rl.ModifyMessage(GMAIL,user_id,msggs,xl)

    if param8 == "Move as Unread":
        xl=rl.AddMsgLabels()
        for msggs in pr6:
            rl.ModifyMessage(GMAIL,user_id,msggs,xl)

    cvl=rl.AddManuallyLabels(param9.upper())
    for msggs in pr6:
        rl.MessageMode(GMAIL,user_id,msggs,cvl)

    cxx=rl.MakeLabel(param10.upper())
    rl.CreateLabel(GMAIL,user_id,cxx)


    param7=int(param7)*-1
    print "Param=",param
    print "Param1=",param1
    print "Param2=",param2
    print "Param3=",param3
    print "Param4=",param4
    print "Param5=",param5
    print "Param6=",param6
    print "Param7=",param7
    print "Param8=",param8
    print "Param9=",param9
    print "Param11=",param11

    param12={
    param1:{
    "from":{
     param : param5
    },
    param2:{
    param3 : param6,
    },
    "daterecieved":{
    param4 : param7,
    },
    param8:{
    "value" : param9
    }
    }
    }
    jsonData = json.dumps(param12)
    with open('{}.json'.format(param11),'w') as fly:
        fly.write(jsonData)

def client_ex():
    exit()

label_1 = Label(root, text="Description:")
entry_1 = Entry(root)
entry_2 = Entry(root)
entry_3 = Entry(root)
entry_4 = Entry(root)
entry_5 = Entry(root)
button_1 = Button(text="From")
button_2 = Button(text="Date Recieved")

root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

label_2=Label(root, text="If")
label_3=Label(root, text="condition are true")
label_4 = Label(root, text="days old")
label_5= Label(root, text="Perform the following actions:")
label_5.grid(row=7,columnspan=2)
label_6= Label(root, text="to mailbox:")
label_7= Label(root, text="Add Custom Label:")
label_1.grid(row=0, sticky=(N,W,E,S))
button_4 = Button(text="Submit",command=lambda: callback(tkvar.get(),tkVar2.get(),tkVar3.get(),tkVar4.get(),tkVar5.get(),entry_2.get(),entry_3.get(),entry_4.get(),tkVar6.get(),tkVar7.get(),entry_5.get(),entry_1.get()))
button_4.grid(row=11,column=2)
button_5 = Button(text="Cancel",command=lambda: client_ex())
button_5.grid(row=11,column=3)
entry_1.grid(row=0, column=1,)
entry_3.grid(row=3,column=2)
entry_4.grid(row=4,column=2)
entry_5.grid(row=10,column=1)
label_2.grid(row=1,column=0)
label_3.grid(row=1,column=2,sticky=(W))
label_4.grid(row=4,column=3,sticky=(W))
label_6.grid(row=8,column=1)
label_7.grid(row=10)
tkvar = StringVar(root)
tkVar2= StringVar(root)
tkVar3= StringVar(root)
tkVar4= StringVar(root)
tkVar5= StringVar(root)
tkVar6= StringVar(root)
tkVar7= StringVar(root)

choices = { 'contains','equal','not equal'}
tkvar.set('contains')

cal = {'Inbox', 'Important', 'Spam', 'Trash'}
tkVar7.set('Inbox')

ckl = { 'Move as Read','Move as Unread'}
tkVar6.set('Move as Read')

choice= {'All', 'Any'}
tkVar2.set('Any')

ch= {'Subject', 'Message'}
tkVar3.set('Subject')

choice2 = { 'contains','equal','not equal'}
tkVar4.set('contains')

choice3 = { 'less than','equal to'}
tkVar5.set('less than')

pMenu= OptionMenu(root,tkVar2, *choice)
popupMenu = OptionMenu(root, tkvar, *choices)

ckMenu= OptionMenu(root,tkVar6, *ckl)
ckMenu.grid(row=8)

calMenu= OptionMenu(root,tkVar7, *cal)
calMenu.grid(row=8,column=2)

popupMenu.grid(row=2,column=1 ,sticky=(N,W,E,S))
pMenu.grid(row=1, column=1 ,sticky=(W))

pkMenu= OptionMenu(root, tkVar3, *ch)
pkMenu.grid(row=3)

pMenu= OptionMenu(root, tkVar4, *choice2)
pMenu.grid(row=3,column=1)

Menu= OptionMenu(root, tkVar5, *choice3)
Menu.grid(row=4,column=1)

button_1.grid(row=2)
button_2.grid(row=4)
entry_2.grid(row=2,column=2)

root.mainloop()
