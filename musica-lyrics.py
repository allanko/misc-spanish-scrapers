# -*- coding: utf-8 -*-

# scrape song lyrics for five artists from musica.com
# mana: http://www.musica.com/letras.asp?letras=9300
# ricky martin: http://www.musica.com/letras.asp?letras=251
# celia cruz: http://www.musica.com/letras.asp?letras=3682
# paulina rubio: http://www.musica.com/letras.asp?letras=502
# shakira: http://www.musica.com/letras.asp?letras=340

import requests, time
from bs4 import BeautifulSoup
import cache

BS_PARSER = "html.parser" 
RUN = True # switch this to true to run script
ROOT_URL = u'http://www.musica.com/'

ARTIST_URLS = {'mana' : u'http://www.musica.com/letras.asp?letras=9300',
               'ricky-martin' : u'http://www.musica.com/letras.asp?letras=251',
               'celia-cruz' : u'http://www.musica.com/letras.asp?letras=3682',
               'paulina-rubio' : u'http://www.musica.com/letras.asp?letras=502',
               'shakira' : u'http://www.musica.com/letras.asp?letras=340'}

def fetch_webpage_text(url, use_cache=True):
    if use_cache and cache.contains(url):
        return cache.get(url)
    # if cache miss, download it and sleep one second to prevent too-frequent calls
    content = requests.get(url).text
    cache.put(url,content)
    time.sleep(1)
    return content
    
def get_all_song_links(artist):
    # return a list of links to all listed songs by that artist
    # links to song lyrics take the form u'letras.asp?letra=####' - disregard all other links
    sand = BeautifulSoup(fetch_webpage_text(ARTIST_URLS[artist]), BS_PARSER)
    links = [a.get('href') for a in sand.find_all('a')]
    links = [l for l in links if l.startswith(u'letras.asp?letra=')]
    links = list(set(links)) # remove repeats
    return links
    
def get_lyrics(page):
    # return lyrics from a given link item as outputted by get_all_song_links()
    # every lyrics page has exactly 83 <table> tags
    # the lyrics are in table 50, plus some extra text that we can clip out

    sand = BeautifulSoup(fetch_webpage_text(ROOT_URL + page), BS_PARSER)
    lyrics = sand.find_all('table')[50].get_text()
    title = lyrics[lyrics.find('RankingCompartir Letra') + 22 : lyrics.find('Enviar letra')]
    lyrics = lyrics[lyrics.find(u'.push({});') + 10 : lyrics.rfind(u'(adsbygoogle')]
        
    return [title.strip(), lyrics.strip()]
    
if __name__ == "__main__" and RUN:
    
    for artist in ['mana', 'ricky-martin', 'celia-cruz', 'paulina-rubio', 'shakira']:
        print 'working on: ', artist
        songs = get_all_song_links(artist)
        print 'songs found: ', len(songs)
        
        alllyrics = []
        
        for s in songs:
            alllyrics += get_lyrics(s)
        
        # output
        outfile = 'lyrics-' + artist + '.txt'
        towrite = '\n\n'.join(alllyrics)
        
        with open(outfile, 'w') as f:
            f.write(towrite.encode('utf-8'))
        
        

        
    