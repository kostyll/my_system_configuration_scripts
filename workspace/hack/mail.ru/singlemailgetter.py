import poplib
import getpass
import argparse
from collections import namedtuple

Mail = namedtuple("Mail", "Date Subject From To Received ContentType ContentTransferEncoding MessageID SpamDetected Content Additions")

def get_messages(account,params):
    print ("Beginning...")
    result = []
    AllMessages = []
    if params.PORT:
        mServer = poplib.POP3(params.SERVER,port=params.PORT)
    else:
        mServer = poplib.POP3(params.SERVER)
    # mServer.set_debuglevel(2)
    mServer.user(account[0])
    mServer.pass_(account[1])
    messages = mServer.list()[1]
    print ("List is ready")
    messages_count = len(messages)
    for index, mList in enumerate(range(messages_count)):
        print ('item[%s]'% index)
        message = {
                'Date':None,
                'Subject':None,
                'From':None,
                'To':None,
                'Received':None,
                'ContentType':None,
                'ContentTransferEncoding':None,
                'MessageID':None,
                'SpamDetected':None,
                'Content':list(),
                'Additions':None
            }        
        begin_message = False            
        for msg in mServer.retr(mList+1)[1]:
            # print msg,len(msg)

            if begin_message:
                message['Content'].append(msg)

            if msg.startswith('Subject:'):
                message['Subject'] = msg.partition('Subject:')[2]
                # print "Subject found"
            if msg.startswith('From:'):
                message['From'] = msg.partition('From:')[2]
                # print "From found"
            if msg.startswith('To:'):
                message['To'] = msg.partition('To:')[2]                
                # print "To found"
            if msg.startswith('Date:'):
                message['Date'] = msg.partition('Date:')[2]
                # print "Date found"
            if msg.startswith('Content-Type:'):
                message['ContentType'] = msg.partition('Content-Type:')[2]
                # print "Content-Type found"
            if msg.startswith('Content-Transfer-Encoding:'):
                message['ContentTransferEncoding'] = msg.partition('Content-Transfer-Encoding:')[2]
                # print "Content-Transfer-Encoding found"
            if msg.startswith('Received:'):
                message['Received'] = msg.partition('Received:')[2]
                # print "Received found"
            if msg.startswith('X-Spam:'):
                message['SpamDetected'] = msg.partition('X-Spam:')[2]
                # print "X-Spam found"
            if msg.startswith('Message-Id:'):
                message['MessageID'] = msg.partition('Message-Id:')[2]
                # print "Message-Id found"
            if not begin_message and len(msg) == 0:
                begin_message = True
                # print "Message content starts"

        print ("message:",message)
        AllMessages.append(message)
    mServer.quit()
    print "Done."
    return AllMessages


def main():
    parser = argparse.ArgumentParser(description="""
            Some description
            """)
    parser.add_argument('--server', action='store', dest='SERVER', help='server address')
    parser.add_argument('--port', action='store',dest='PORT', help='server port')
    parser.add_argument('-u', action='store',dest='USER', help='user name')
    parser.add_argument('-p', action='store',dest='PASSWORD', help='user password')
    args = parser.parse_args()
    if args.USER and args.PASSWORD:
        messages = get_messages((args.USER,args.PASSWORD),args)
        for message in messages:
            print ("MESSAGE:\n%s" % message)

if __name__ == '__main__':
    main()
