from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from dateutil import parser
from oauth2client import file, client, tools
import base64
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
user_id =  'me'
vx=[]

class Ruler:
    def __init__(self):
        pass
    def CreateLabel(self,service, user_id, label_object):
      try:
        label = service.users().labels().create(userId=user_id,
                                                body=label_object).execute()
    #   print label['id']
        return label
      except errors.HttpError, error:
        print 'error occurred: %s' % error


    def MakeLabel(self,label_name, mlv='show', llv='labelShow'):
      label = {'messageListVisibility': mlv,
               'name': label_name,
               'labelListVisibility': llv}
      return label

    def ModifyMessage(self,service, user_id, msg_id, msg_labels):
      try:
        message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                    body=msg_labels).execute()

        label_ids = message['labelIds']

        return message
      except errors.HttpError, error:
        print 'Error occurred: %s' % error

    def MessageMode(self,service, user_id, msg_id, msg_labels):
      try:
        message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                    body=msg_labels).execute()

        label_ids = message['labelIds']

        print 'Message ID: %s - With Label IDs %s' % (msg_id, label_ids)
        return message
      except errors.HttpError, error:
        print 'Error occurred: %s' % error

    def AddMsgLabels(self):
      return {'removeLabelIds': [], 'addLabelIds': ['UNREAD', 'INBOX']}
      vx=['UNREAD']

    def MakeAsRead(self):
      return {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}

    def AddManuallyLabels(self,label_id):
      #print label_id
      return {'removeLabelIds': [], 'addLabelIds': [label_id,vx]}
