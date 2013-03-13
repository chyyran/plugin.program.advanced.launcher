# -*- coding: UTF-8 -*-

import re
import os
import urllib,urllib2
import simplejson

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

# Return Comics search list
def _get_games_list(search):
    comicvine_key = "a1aaa516eaf233abf29c8aefaa46dc39cc0f0873"
    results = []
    display = []
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
                comic["id"] = str(issue_id[-1].encode('utf-8','ignore'))
                f = urllib.urlopen('http://api.comicvine.com/issue/'+comic["id"]+'/?api_key='+comicvine_key+'&format=xml&field_list=publish_year,description,volume,name,issue_number')
                page = f.read().replace('\r\n', '').replace('\n', '')
                volume_name = ''.join(re.findall('</id><name><!\[CDATA\[(.*?)\]\]></name></volume>', page))
                issue_number = ''.join(re.findall('<issue_number>(.*?)</issue_number>', page))
                issue_name = ''.join(re.findall('</issue_number><name><!\[CDATA\[(.*?)\]\]></name><publish_year>', page))
                release = ''.join(re.findall('<publish_year>(.*?)</publish_year>', page))
                comic["title"] = str(volume_name)
                if ( issue_number != "" ):
                    comic["title"] += ' #'+'{0:.3g}'.format(float(issue_number))
                if ( issue_name != "" ):
                    comic["title"] += ': '+issue_name
                if ( release != "" ):
                    comic["title"] += ' ('+release+')'
                comic["gamesys"] = 'Comic'
                results.append(comic)
                display.append(comic["title"].encode('utf-8','ignore'))
        return results,display
    except:
        return results,display
        
# Return 1st Comic search
def _get_first_game(search,gamesys):
    comicvine_key = "a1aaa516eaf233abf29c8aefaa46dc39cc0f0873"
    results = []
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
                comic["id"] = str(issue_id[-1].encode('utf-8','ignore'))
                f = urllib.urlopen('http://api.comicvine.com/issue/'+comic["id"]+'/?api_key='+comicvine_key+'&format=xml&field_list=publish_year,description,volume,name,issue_number')
                page = f.read().replace('\r\n', '').replace('\n', '')
                volume_name = ''.join(re.findall('</id><name><!\[CDATA\[(.*?)\]\]></name></volume>', page))
                issue_number = ''.join(re.findall('<issue_number>(.*?)</issue_number>', page))
                issue_name = ''.join(re.findall('</issue_number><name><!\[CDATA\[(.*?)\]\]></name><publish_year>', page))
                release = ''.join(re.findall('<publish_year>(.*?)</publish_year>', page))
                comic["title"] = str(volume_name)
                if ( issue_number != "" ):
                    comic["title"] += ' #'+'{0:.3g}'.format(float(issue_number))
                if ( issue_name != "" ):
                    comic["title"] += ': '+issue_name
                if ( release != "" ):
                    comic["title"] += ' ('+release+')'
                comic["gamesys"] = 'Comic'
                results.append(comic)
        return results
    except:
        return results
        
# Return Comic data
def _get_game_data(game_id):
    comicvine_key = "a1aaa516eaf233abf29c8aefaa46dc39cc0f0873"
    gamedata = {}
    gamedata["genre"] = ""
    gamedata["release"] = ""
    gamedata["studio"] = ""
    gamedata["plot"] = ""
    try:
        f = urllib.urlopen('http://api.comicvine.com/issue/'+game_id+'/?api_key='+comicvine_key+'&format=xml&field_list=publish_year,description,volume,name,issue_number')
        page = f.read().replace('\r\n', '').replace('\n', '')
        release_date = ''.join(re.findall('<publish_year>(.*?)</publish_year>', page))
        gamedata["release"] = release_date.encode('utf-8','ignore')
        plot = ''.join(re.findall('<description><!\[CDATA\[(.*?)\]\]></description>', page))
        title = re.findall('<name><!\[CDATA\[(.*?)\]\]></name>', page)
        p = re.compile(r'<.*?>')
        gamedata["plot"] = unescape(p.sub('', title[0].encode('utf-8','ignore')+" : "+plot.encode('utf-8','ignore')))
        volume = ''.join(re.findall('<api_detail_url><!\[CDATA\[(.*?)\]\]></api_detail_url>', page))
        if volume:
            f = urllib.urlopen(volume+'?api_key='+comicvine_key+'&format=xml&field_list=publisher')
            page = f.read().replace('\r\n', '').replace('\n', '')
            studio = ''.join(re.findall('<name><!\[CDATA\[(.*?)\]\]></name>', page))
            gamedata["studio"] = studio.encode('utf-8','ignore')
        return gamedata
    except:
        return gamedata
        
def unescape(s):
    s = s.replace('<br />',' ')
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    s = s.replace("&#039;","'")
    s = s.replace('<br />',' ')
    s = s.replace('&quot;','"')
    s = s.replace('&nbsp;',' ')
    s = s.replace('&#x26;','&')
    s = s.replace('&#x27;',"'")
    s = s.replace('&#xB0;',"°")
    return s
