#!/usr/bin/python
# smush.py - Use your SmushBox
import argparse, re, json, sys, urllib2
__author__ = 'RobPickering.com and INoUrScrts'

# Process SmushBox JSON Response
def processJSON( result ):
    print ("Result: %s" % result)
    return

# Process Errors
def handleError( e ):
    print ("Error: %s" % e)
    return

# Connect to SmushBox
def smushBox(url):
    try:
        result = json.load(urllib2.urlopen(url))
        if result['success']:
            return result
        else:
            print result['errors']
    except urllib2.URLError, e:
        handleError(e)
    sys.exit()

def queryIncoming(connectDict):
    url = 'http://'+connectDict['hostName']+'/messagelist/list/incoming/al?&username='+connectDict['username']+'&password='+connectDict['password']
    result = smushBox(url)
    print "----------Incoming Messages----------"
    print "====================================="
    print "#\tPhone Number\tDate\t\t\tRead\tMessage"
    for message in result['message']:
        print message['phone_id'].encode('utf-8'),"\t",message['number'].encode('utf-8'),"\t",message['format_time'].encode('utf-8'),"\t",message['read'],"\t",message['message'].encode('utf-8')
    return

def queryOutgoing(connectDict):
    url = 'http://'+connectDict['hostName']+'/messagelist/list/outgoing/all?username='+connectDict['username']+'&password='+connectDict['password']
    result = smushBox(url)
    print "----------Outgoing Messages----------"
    print "====================================="
    print "#\tMessage ID\tPhone Number\tDate\t\t\tMessage"
    for message in result['message']:
        print message['phone_id'].encode('utf-8'),"\t",message['message_id'].encode('utf-8'),"\t\t",message['number'].encode('utf-8'),"\t",message['format_sent'].encode('utf-8'),"\t",message['message'].encode('utf-8')
    return

def queryContacts(connectDict):
    url = 'http://'+connectDict['hostName']+'/phonebook/list?username='+connectDict['username']+'&password='+connectDict['password']
    result = smushBox(url)
    print "----------Contacts----------"
    print "============================"
    print "#\tPhone Number\tDisabled\tGroup"
    for contact in result['message']:
        print contact['phone_id'].encode('utf-8'),"\t",contact['number'].encode('utf-8'),"\t",contact['disabled'].encode('utf-8'),"\t\t",contact['group_member']
    return

def queryGroups(connectDict):
    url = 'http://'+connectDict['hostName']+'/group/list?groupname=&username='+connectDict['username']+'&password='+connectDict['password']
    result = smushBox(url)
    print "----------Groups----------"
    print "=========================="
    print "#\tGroup Name"
    for group in result['message']:
        print group['group_id'].encode('utf-8'),"\t",group['name'].encode('utf-8')
    return

def sendText(connectDict, textDict):
   # Replace spaces in the Text Message with Plus signs
    message = re.sub('[ ]', '+', textDict['message'])
   # Text Message is limited to 160 characters (at this time)
    message = (message[:157] + '...') if len(message) > 160 else message
    url = 'http://'+connectDict['hostName']+'/messagelist/send?number='+textDict['number']+'&message='+message+'&username='+connectDict['username']+'&password='+connectDict['password']
    smushBox(url)
    print "Message sent"
    return

def deleteOutgoing(connectDict):
    url = 'http://'+connectDict['hostName']+'/messagelist/delete/outgoing/all?username='+connectDict['username']+'&password='+connectDict['password']
    smushBox(url)
    return

def deleteIncoming(connectDict):
    url = 'http://'+connectDict['hostName']+'/messagelist/delete/incoming/all?username='+connectDict['username']+'&password='+connectDict['password']
    smushBox(url)
    return

def main():

    parser = argparse.ArgumentParser(description='Use your SmushBox by RobPickering.com and INoUrScrts')

    text_group = parser.add_argument_group('Text Options')
    text_group.add_argument('-t','--text',help='Send SMS message',action='store_true')
    text_group.add_argument('-n','--number',help='Recipient mobile number',required=False)
    text_group.add_argument('-m','--message',help='Text to send, use quoted string',required=False)
    query_group = parser.add_argument_group('Query Options')
    query_group.add_argument('-i','--incoming',help='Query incoming messages and display',action='store_true')
    query_group.add_argument('-o','--outgoing',help='Query outgoing messages and display',action='store_true')
    query_group.add_argument('-c','--contacts',help='Query phonebook and display',action='store_true')
    query_group.add_argument('-g','--groups',help='Query groups and display',action='store_true')
    auth_group = parser.add_argument_group('Authentication Options')
    auth_group.add_argument('-u','--username',help='Username',required=False)
    auth_group.add_argument('-p','--password',help='Password',required=False)
    auth_group.add_argument('-s','--smushbox',help='HostName or IP',required=False)
    clear_group = parser.add_argument_group('Clear Options')
    clear_group.add_argument('-d','--deleteout',help='Delete All Outgoing',action='store_true',required=False)
    clear_group.add_argument('-e','--deletein',help='Delete All Incoming',action='store_true',required=False)

    args = parser.parse_args() # Grab arguments

    connectDict = {}     # Override defaults with options
    if args.username:
        username = args.username
    else:
        username = "smushbox"
    connectDict['username'] = username
    if args.password:
        password = args.password
    else:
        password = "smushbox"
    connectDict['password'] = password
    if args.smushbox:
        hostName = args.smushbox
    else:
        hostName = "smushbox.home"
    connectDict['hostName'] = hostName

    if args.text:  # If text and message lets send a message
        if args.message and args.number:
            textDict = {'message':args.message, 'number':args.number}
            sendText(connectDict,textDict)
        else:
            print "Missing a message and/or a number"
            sys.exit()
               
    if args.incoming:
        queryIncoming(connectDict)

    if args.outgoing:
        queryOutgoing(connectDict)
       
    if args.contacts:
        queryContacts(connectDict)

    if args.groups:
        queryGroups(connectDict)
       
    if args.deleteout:
        deleteOutgoing(connectDict)
        queryOutgoing(connectDict)

    if args.deletein:
        deleteIncoming(connectDict)
        queryIncoming(connectDict)

    return

if __name__ == '__main__':
    main()
