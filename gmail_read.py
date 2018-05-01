from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import sqlite3

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
global GMAIL
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
user_id =  'me'
label_id_one = 'INBOX'
label_id_two = 'UNREAD'
conn=sqlite3.connect('mg_db.db')
unread_msgs = GMAIL.users().messages().list(userId='me',labelIds=[label_id_one,label_id_two]).execute()
c=conn.cursor()
mssg_list = unread_msgs['messages']

print ("Loading...")

final_list = [ ]

xmail=[]
for mssg in mssg_list:
	temp_dict = { }
	m_id = mssg['id']
	temp_dict['m_id']=m_id
	message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute() # fetching the message using API
	payld = message['payload']
	headr = payld['headers']

	for one in headr:
		if one['name'] == 'Subject':
			msg_subject = one['value']
			temp_dict['Subject'] = msg_subject
		else:
			pass

	for two in headr:
		if two['name'] == 'Date':
			msg_date = two['value']
			date_parse = (parser.parse(msg_date))
			m_date = (date_parse.date())
			temp_dict['Date'] = str(m_date)
		else:
			pass

	for three in headr:
		if three['name'] == 'From':
			msg_from = three['value']
			temp_dict['Sender'] = msg_from
		else:
			pass

	temp_dict['Snippet'] = message['snippet']

	final_list.append(temp_dict)
#	print final_list
for mail in final_list:
      try:
		  h=re.search(r'([a-zA-Z0-9]+)@.+[^>]',mail['Sender']).group()
		  d=mail['Date']
		 # print mail['Snippet']
		  c.execute("INSERT INTO Email VALUES (?,?,?,?,?)",[str(h,),str(mail['m_id']),str(d),str(mail['Subject']),str(mail['Snippet'])] )
		 # print h
		  conn.commit()
      except Exception as e:
        print e.message

conn.close();
