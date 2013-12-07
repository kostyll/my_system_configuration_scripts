from sys import argv
import smtplib

USAGE ="""script.py single server port username_full password
script.py list filename{login:pass}"""

def check(handler,user, password):
    try:
        log = handler.login(user,password)
        return True
    except:
        return False
    

if len(argv) == 1:
    print USAGE
else:
    action = argv[1]
    SERVER = argv[2]
    PORT = argv[3]
    handler = smtplib.SMTP()
    currsor = handler.connect(SERVER,int(PORT))
 
    if action == 'single':
    	USER = argv[4]
    	PASSWORD = argv[5]
        print (check(handler,USER,PASSWORD))
    else:
        logfile = open('logfile.txt','wt')
        FILENAME = argv[4]
        f = open (FILENAME,'rt')
        res = False
        for index, line in enumerate(f.readlines()):
            handler = smtplib.SMTP()
            try:
                currsor = handler.connect(SERVER,int(PORT))
                #print ("Line = %s" % line)
                try:
                    USER, PASSWORD = line.split(':')
                    USER = USER.strip()
                    PASSWORD = PASSWORD.strip()
                except:
                    break
                res = check(handler,USER,PASSWORD)
                print ("[%s] checking email '%s' & password '%s' : %s" % (index,USER,PASSWORD,True if res==True else False))
            except:
                continue
            if res == True:
                logfile.write("%s:%s"%(USER,PASSWORD))
        logfile.close()

