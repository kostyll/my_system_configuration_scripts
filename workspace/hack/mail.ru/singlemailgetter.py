import poplib
import email
import getpass
import argparse
from collections import namedtuple
from email.header import decode_header
import quopri
from StringIO import StringIO
import os
import re
from base64 import b64decode

email_dir = './accounts/'
Mail = namedtuple("Mail", "Date Subject From To Received ContentType ContentTransferEncoding MessageID SpamDetected Content Additions")

def get_messages(account,params):
    print ("Beginning...")
    result = []
    AllMessages = []
    mask = {'windows-1251':'cp1251','koi8-r':'koi8-r','iso-8859-5':'iso-8859-5',None:'utf-8','utf-8':'utf-8'}
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
    output = email_dir+account[0]+'/'
    try:
        os.makedirs(output)
    except:
        pass
    for index, mList in enumerate(range(messages_count)):
        print ('item[%s]'% index)
    
        begin_message = False
        message_data = mServer.retr(mList+1)[1]
        message_data = '\n'.join(message_data)        
        femail = open(output+str(index)+'.msg','wb')
        femail.write(message_data)
        femail.close
        msg = email.message_from_string(message_data)
        # print msg
        for post_index, post in enumerate(msg.walk()):
            # print "post",post
            print "post[%s] [%s]" % (post_index, post.get_param("name")) 
            if post.has_key('Subject'):
                value, charset = decode_header(post['Subject'])[0]
                try:
                    value = value.decode(mask[charset]).encode('utf-8')
                except KeyError:
                    print '[WARNING] add new mask -> {unk}'.format(unk = charset)
                message = {
                    'Date':post['Date'],
                    'Subject':post['Subject'],
                    'From':post['From'],
                    'To':post['To'],
                    'Received':post['Received'],
                    'ContentType':post['Content-Type'],
                    'ContentTransferEncoding':post['Content-Transfer-Encoding'],
                    'MessageID':post['Message-Id'],
                    'SpamDetected':post['X-Spam'],
                    'RawContent':None,
                    'Content':None,
                    'Additions':None,
                }    

                if message['Subject'].pos(r'=?') and message['Subject'].pos('?='):
                    try:
                        search = re.compile(r'=\?([\w\s-]+)\?B\?{0,1}([^?]+)')
                        matches = search.findall(message['Subject'])
                        matches = map (lambda x: (x[0],b64decode(x[1])), matches)
                        subject = ""
                        for match in matches:
                            subject += match[1].decode(match[0].lower())
                        message['Subject'] = subject
                    except:
                        pass

                body = post.get_payload()
                message['RawContent'] = body
                try:
                    if not post.is_multipart():
                        message['Content'] = body.decode(mask[charset]).encode('utf-8') if isinstance(body,str) else ''.join(body).decode(mask[charset]).encode('utf-8')
                        # print value , body.decode(mask[charset]).encode('utf-8') if isinstance(body,str) else ''.join(body).decode(mask[charset]).encode('utf-8')
                    else:
                        message['Content'] = []
                        for part in body:
                            message['Content'].append(part.get_payload())
                except BaseException as error:
                    print '[ERROR] {err}'.format(err=error)
                    message['Content'] = body
                if message['ContentTransferEncoding'] == "quoted-printable":
                    message['Content'] = quopri.decodestring(body)
                    message['Subject'] = quopri.decodestring(message['Subject'])
                    # print ("subject : %s" message['Subject'])
                # print "message",message
                print ("subject : %s" % message['Subject'])
                print ("Decoded message"), 
                print (message['Content'] if isinstance(message['Content'],str) else message['Content'][0][:100])

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
