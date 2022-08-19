import argparse
import logging
import os

import requests
from bs4 import BeautifulSoup

logger = None

def parse_args():
    parser = argparse.ArgumentParser(description = "Web crawler")
    parser.add_argument("-d", "--debug", help = "Enable debug logging", action="store_true")
    return parser.parse_args()

def configure_logging(level=logging.INFO):
    global logger
    logger = logging.getLogger("crawler")
    logger.setLevel(level)
    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(level)
    formatter = logging.Formatter("[%(levelname)s] : %(filename)s(%(lineno)d) : %(message)s")
    screen_handler.setFormatter(formatter)
    logger.addHandler(screen_handler)


def get_artists(artists):
    resp = requests.get(artists)
    soup = BeautifulSoup(resp.content, "lxml")
    track_list = soup.find("table", attrs = {"class" : "tracklist"})
    track_link = track_list.find_all('td',{"class":"td-item td-last"})
    artists={}
    for link in range(0,5):
            artists[track_link[link].find('a').text]=track_link[link].find('a')['href']
    return artists

def get_artists_songs(singer_name,artists_songs):
    resp = requests.get(artists_songs)
    soup = BeautifulSoup(resp.content, "lxml")
    song_lists = soup.find("table", attrs = {"class" : "tracklist"})
    songs_list = song_lists.find_all('a')
    albums={}
    for song in range(0,5):
        albums[songs_list[song].text]=songs_list[song]['href']
        # logger.info(songs_list[song].text)        
    return albums

def get_atrists_song_lyrics(song_lyrics):
    resp = requests.get(song_lyrics)
    soup = BeautifulSoup(resp.content, "lxml")
    lyrics = soup.find('p', attrs = {"id" : "songLyricsDiv"})
    # lyrics=lyrics.find_all('br')
    lines=[]
    # print(lyrics.text)
   
    # for line in range(0,5):
    #     lines.append(lyrics[line].text)
    #     print(line.text)


    


    # for lyric_link in artist_albums:
    #     lyrics_links.append(lyric_link.find('a')['href'])
    #     res=requests.get(lyric_link.find('a')['href'])   
    #     soup=BeautifulSoup(res.content)
    #     content=soup.find('div',{"class":"lyrics-inner-col-wrap"})

    #     print(content.find('p',{"class":"songLyricsV14 iComment-text"}).get_text()[:10])
    

    
    
       
    logger.debug("Completed crawling")

def main():
    args = parse_args()
    if args.debug:
        configure_logging(logging.DEBUG)
    else:
        configure_logging(logging.INFO)
   
    artists=get_artists('https://www.songlyrics.com/top-artists-lyrics.html')
    # print(artists)
    

    data={}
    for singer,songlink in artists.items():
        artist_dir=os.path.join('/home/navas/Desktop/jul-2022-crawler',singer)
        os.makedirs(artist_dir,exist_ok=True)
        data[singer]=get_artists_songs(singer,artists[singer])

    
    # print(data)
    
    print(data.values())

    for singer,songs in data.items():  
        for song,link in data[singer].items():
            file=open(f'/home/navas/Desktop/jul-2022-crawler/{singer}/{song}.txt','w')  
            get_atrists_song_lyrics(link)
    
   

if __name__ == "__main__":
    main()
