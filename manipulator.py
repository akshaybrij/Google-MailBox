import os
import sys
import sqlite3
from datetime import timedelta, datetime
from tkinter import *
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from dateutil import parser
from oauth2client import file, client, tools
import base64
import re
import time
import dateutil.parser as parser

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id =  'me'

lis=[]
om=[]
ne=[]
dta=[]
xz=[]
q=[]
class Manipulator:
    def __init__(self):
        conn=sqlite3.connect("mg_db.db")
        c=conn.cursor()
        c.execute("""Select * from Email""")
        lis.append(c.fetchall())
        conn.commit()
        conn.close()

    def contains(self,strs,index):
        for k in lis[0]:
            if strs in k[index]:
              try:
                om.append(k[1])
              except Exception as e:
                e.message
            else:
                pass
        return om

    def notequals(self,strs,index):
        for k in lis[0]:
            if strs not in k[index]:
              try:
                  ne.append(k[1])
              except Exception as e:
                  e.message
            else:
                None
        return ne

    def equals(self,strs,index):
        for k in lis[index]:
            if k[0] == strs:
                q.append(k[1])
        return q

    def date_equals(self,day):
        now = datetime.now()
        td = timedelta(int(day))
        req = now + td
        for s in lis[0]:
            x=datetime(int(s[2][0:4]),int(s[2][5:7]),int(s[2][8:]))
            if x.date() == req.date():
               dta.append(s[1])
        return dta

    def date_lessrthan(self,day):
        now = datetime.now()
        td = timedelta(int(day))
        req = now + td
        for s in lis[0]:
            x=datetime(int(s[2][0:4]),int(s[2][5:7]),int(s[2][8:]))
            if x.date() < req.date():
               dta.append(s[1])
        return dta


#mn=Manipulator()
#mn.contains("twitter.com")
#mn.date_recieved(-3)
#q=mn.notequals("twitter")
#mn.equals("info@twitter.com")
