import poplib
import getpass
import argparse

def get_messages(account,params):
    result = []
    if params.PORT:
        mServer = poplib.POP3(params.SERVER,port=params.PORT)
    else:
        mServer = poplib.POP3(params.SERVER)
    mServer.user(account[0])
    mServer.pass_(account[1])
    messages = mServer.list()[1]
    messages_count = len(messages)
    for mList in range(messages_count):
        for msg in mServer.retr(mList+1)[1]:
            if msg.startswith('Received:'):
                result.append(msg)
    mServer.quit()
    return result


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
