from __future__ import unicode_literals
import os
import re
import logging
from unicodedata import normalize

import requests
import youtube_dl
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

logging.basicConfig(
  filename="sample.log",
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO)

def normalize_specail_char(txt):
  return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def search_youtube(text):
  url = 'https://www.youtube.com'
  r = requests.get(url + '/results', params={'search_query': text})
  soup = BeautifulSoup(r.content, 'html.parser')
  for tag in soup.find_all('a', {'rel': 'spf-prefetch'}):
    title, video_url = tag.text, url + tag['href']
    if 'googleads' not in video_url:
      return normalize_specail_char(title), video_url

def download(title, video_url):
  ydl_opts = {
    'outtmpl' : '{}.%(ext)s'.format(title),
    'format' : 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
  return {
    'audio' : open(title + '.mp3', 'rb'),
    'title': title,
  }

def start(bot, update):
  update.message.reply_text("YouTube Music Dowloader")
  
def music(bot, update):
  title, video_url = search_youtube(update.message.text)
  update.message.reply_text("Start download" + title)
  music_dict = download(title, video_url)
  update.message.reply_text("Convert to m3 " + title)
  update.message.reply_audio(**music_dict, timeout=9999)
  os.remove(title + '.mp3')
  


# 6243249299:AAFV6GUCe7hxhEg05ufoThKSq43Xrm4vyjE


def main():
    updater = Updater(token="6243249299:AAFV6GUCe7hxhEg05ufoThKSq43Xrm4vyjE", use_context=True)  # Замените "YOUR_BOT_TOKEN" на ваш токен
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, music))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
