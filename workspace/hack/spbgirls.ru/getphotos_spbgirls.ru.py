#! -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os
from urllib import urlopen
from grab import Grab

URL = 'http://spbgirls.ru'
BYTES_COUNT = 0

def get_girls():
    g = Grab()
    g.go(URL)
    girls_list = g.xpath_list('//a[@class="zag1s"]')
    girls_list = map(lambda x: {'name':x.text,'page':x.get('href'),'photos':[]}, girls_list)
    return girls_list

def strip_girl_url(url):
    return url.partition('/individ/')[2].rpartition('.html')[0]

def get_girl_photos(girl):
    g = Grab()
    g.go(URL+girl['page'])
    girl_url = strip_girl_url(girl['page'])
    content_body = g.tree.get_element_by_id('contnt').body
    photos = []
    photo_pages = []
    for link in content_body.iterlinks():
        if link[1] == 'src' and link[2].find('site_original_') > 0 :
            photos.append (link[2])
        if link[1] == 'href' and girl_url in link[2]:
            photo_pages.append(link[2])
    for page in photo_pages :
        g.go(page)
        for link in g.tree.get_element_by_id('contnt').body.iterlinks():
            if link[1] == 'src' and link[2].find('site_original_') > 0:
                photos.append(link[2])
    return photos

def save_girl(girl,out = './'):
    try:
        girl_dir = strip_girl_url(girl['page'])
        os.mkdir(girl_dir)
    except:
        pass
    for index, photo in enumerate(girl['photos']):
        image = urlopen(URL+photo)
        if image.code != 200:
            continue
        info = image.info()
        if info.maintype != 'image':
            continue
        file_name = photo.rpartition('/')[2]
        fdir = open(girl_dir+'/'+file_name,'wb')
        f = open(file_name,'wb')
        data = image.read()
        global BYTES_COUNT
        BYTES_COUNT += len(data)
        fdir.write(data)
        f.write(data)
        fdir.close()
        f.close()


girls = get_girls()
print ('girls count = %s'%len(girls))
for index, girl in enumerate(girls):
    print ("[%s] girl %s at %s" % (index, girl['name'],URL+girl['page']))

for index, girl in enumerate(girls):
    print ('index = %s bytes loaded = %s' % (index,BYTES_COUNT))
    photos = get_girl_photos(girl)
    girls[index]['photos'] = photos
    for photo in photos:
        print (photo)
    save_girl(girl)

# save_girls(girls)

# print (get_girls())
