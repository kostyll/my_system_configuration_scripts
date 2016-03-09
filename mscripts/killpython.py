#!/usr/bin/env python

import os
import subprocess

my_pid = os.getpid()

seek_expr = os.sys.argv[1]

processes_info = subprocess.check_output(['ps', 'aux']).split('\n')[1:]
processes_info = map(lambda x: x[9:].strip(), processes_info)

for process in processes_info:
    if seek_expr in process:
        process_pid = int(process.split(' ')[0])
        if process_pid == my_pid: continue
        os.kill(process_pid, 9)


