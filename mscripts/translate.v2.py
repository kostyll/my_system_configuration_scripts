#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""This script allow users to translate a string 
from one language to another with Google Translate API
You have to insert Your Translate API key
Get your API key from here: 
   https://code.google.com/apis/console/?api=translate
Replace 
    api_key = '**********' with your API key
"""

import sys
import urllib
import urllib2
import json

def translate(list_of_params):
    """Translate given text"""
        
    url = "https://www.googleapis.com/language/translate/v2?%s"    
    
    request = urllib2.Request(url % urllib.urlencode(list_of_params), 
       headers={ 'User-Agent': 'Mozilla/5.0', 'Accept-Charset': 'utf-8' })
    res = urllib2.urlopen(request).read()
    translated = json.loads(res)
    for translations in translated['data']['translations']:            
        print translations['translatedText']    

def main():
    """
    Usage:
        first arg - string to translate
        second arg - source lang
        third arg - target lang    
    Example:
        translate.py 'text to translate' en ru
        translate.py 'text to translate' ru en
        translate.py 'auto detect source language' ru
    """
    api_key = '**********'
    list_of_params = {'key' : api_key, }    
    
    if len(sys.argv) == 4:
        #both langs entered
        list_of_params.update({'q' : sys.argv[1],
                               'source' : sys.argv[2], 
                               'target' : sys.argv[3] })
        translate(list_of_params)

    elif len(sys.argv) == 3:
        #auto source language
        list_of_params.update({'q' : sys.argv[1],
                               'target' : sys.argv[2] })
        translate(list_of_params)        
    else:
        print main.__doc__
        
if __name__ == '__main__':
    main()
