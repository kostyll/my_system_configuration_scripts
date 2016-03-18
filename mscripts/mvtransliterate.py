#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    import transliterate
except:
    print "install transliterate library: pip install transliterate"
    sys.exit(0)

try:
    import fnmatch
except:
    print "install fnmatch library: pip install fnmatch"
    sys.exit(0)

try:
    dir_for_transliterating = sys.argv[1]
except:
    dir_for_transliterating = '.'

try:
    mask_for_transliterating = sys.argv[2]
except:
    mask_for_transliterating = '*'

files_to_transliterate = []
for file in os.listdir(dir_for_transliterating):
    if fnmatch.fnmatch(file, mask_for_transliterating):
        files_to_transliterate.append(file)

for file in files_to_transliterate:
    #import ipdb; ipdb.set_trace()
    print "Renaming file %s" % file
    try:
        newfile = transliterate.translit(file.decode('utf-8'), reversed=True)
        newfile = newfile.replace('\'', '_')
        newfile = newfile.replace(u'і', 'i')
        newfile = newfile.replace(u'ї', 'i')
        newfile = newfile.replace(u'є', 'e')
    except:
        print "Error while renaming file %s" % file
        continue
    os.rename(file, newfile)