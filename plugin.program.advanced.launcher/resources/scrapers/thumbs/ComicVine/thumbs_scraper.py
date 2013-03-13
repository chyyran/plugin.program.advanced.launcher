# -*- coding: UTF-8 -*-

import os
import re
import urllib,urllib2
import simplejson
from xbmcaddon import Addon

# Get url with Mozilla User-Agent
def get_url(url):
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13','Referer': 'http://python.org'}
    request = urllib2.Request(url, headers=req_headers)
    opener = urllib2.build_opener()
    response = opener.open(request)
    contents = response.read().replace('\r\n', '').replace('\n', '')
    return contents

# Remove HTML tags
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


# Get Comics pages
def _get_game_page_url(system,search):
    comicvine_key = "a1aaa516eaf233abf29c8aefaa46dc39cc0f0873"
    comics_results = []
    search = urllib.quote(search.lower())
    try:
        url = get_url('http://www.google.com/cse?cx=017553361912933201960%3Ag3cbzpf3qis&q="'+search+'"&as_occt=title&nojs=1&num=100')
        issues = re.findall('<a class="l" href="(.*?)" (.*?)>(.*?)</a>', url)
        for i in issues:
            comic = {}
            comic_id = i[0].split('/')
            issue_id = comic_id[-2].rsplit('-',1)
            page_type = issue_id[0]
            if ( issue_id[-1].isdigit()) and ( issue_id[0] == "37" ):
                comic["url"] = i[0]
                comics_results.append(comic)
        return comics_results
    except:
        return comics_results
        
# Thumbnails list scrapper
def _get_thumbnails_list(system,search,region,imgsize):
    covers = []
    game_id_url = _get_game_page_url(system,search)
    try:
        for comic in game_id_url:
            cover_number = 1
            game_page = urllib.urlopen(str(comic["url"].encode('utf-8','ignore')))
            if game_page:
                for line in game_page.readlines():
                    if '[/img][/url]' in line:
                        result = ''.join(re.findall('\[img\](.*?)\[/img\]', line))
                        covers.append((result,result.replace('_large','_thumb'),"Cover "+str(cover_number)))
                        cover_number = cover_number + 1
        return covers
    except:
        return covers

# Get Thumbnail scrapper
def _get_thumbnail(image_url):
    return image_url
