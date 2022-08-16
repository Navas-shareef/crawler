import argparse
import logging

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


def get_artist():
    logger.debug("Crawling starting")
    res=requests.get("https://www.songlyrics.com/")
    soup=BeautifulSoup(res.content)
    content=soup.find('table',{"class":"tracklist"})
    
  
    artist_names=content.findAll('span')

    artist_albums=content.findAll('td',{"class":"td-item td-last"})

   
  
   
    for name,album in zip(artist_names,artist_albums):
        print(f"{name.get_text()}:{album.find('a').get_text()}")



    


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
    logger.debug("Here's a debug message")
    logger.info("Here's an info message!")
    logger.warning("Here's an warning message!")
    logger.critical("Here's an critical message!")
    get_artist()


if __name__ == "__main__":
    main()
