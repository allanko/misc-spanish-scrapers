# -*- coding: utf-8 -*-

# scrape all spanish-language speeches by fidel castro
# from http://www.cuba.cu/gobierno/discursos/

import requests, time
from bs4 import BeautifulSoup
import cache

BS_PARSER = "html.parser" 
RUN = True # switch this to true to run script
ROOT_URL = u'http://www.cuba.cu/gobierno/discursos/'

def fetch_webpage_text(url, use_cache=True):
    if use_cache and cache.contains(url):
        return cache.get(url)
    # if cache miss, download it and sleep one second to prevent too-frequent calls
    content = requests.get(url).text
    cache.put(url,content)
    time.sleep(1)
    return content
    
if __name__ == "__main__" and RUN:
    
    homepage = BeautifulSoup(fetch_webpage_text(ROOT_URL), BS_PARSER)
    keep = [a for a in homepage.find_all('a') if u'pa\xf1o' in a.get_text()] 
    # there are typos: checking for a.get_text() == Espa\xf1ol is unreliable. this catches 1151 links. think that's right.
    
    links = [a.get('href') for a in keep]
    
    # most links look something like u'2007/esp/f270807e.html' -- but some don't:
    # eg u'../discursos/2008/esp/f220208e.html' or u'http://www.cuba.cu/gobierno/reflexiones/2007/esp/f190707e.html' are both in links
    # make all links the same format:
    for i, l in enumerate(links):
        if l.startswith('2') or l.startswith('1'):
            links[i] = ROOT_URL + l
        elif l.startswith('..'):
            links[i] = ROOT_URL[:-10] + l[3:]
        elif l.startswith('http'):
            pass
        else:
            raise ValueError("unexpected URL found:  " + l)
            
    # some pages have <body> tags and some don't
    # but i think every page puts all the text in <p> tags
    # so let's grab those...
            
    towrite = ''
            
    for l in links:
        sand = BeautifulSoup(fetch_webpage_text(l), BS_PARSER)
        textlist = [p.get_text() for p in sand.find_all('p')]
        towrite += '\n'.join(textlist) + '\n\n'
    
    # output to file
    with open('castro-speech-text.txt', 'w') as f:
        f.write(towrite.encode('utf-8'))