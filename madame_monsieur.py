#!/usr/bin/python
# -*- coding: latin-1 -*-

# --------------------------------------------------
# Madame MOnsieur webhook bot for Discord
# Quentin Dufournet, 2022
# --------------------------------------------------

# Built-in
import json
import time
import logging
import sys
import os
import configparser

# 3rd party
import requests
from deep_translator import GoogleTranslator

# DEBUG
DEBUG = 0
DEVELOP = 1

# --------------------------------------------------

class MadameMonsieur:
    def __init__(self):
        """
        It reads the tokens from the file and stores them in variables.
        """
        
        # Set logger
        logging.basicConfig(filename='madame_monsieur.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.info('Starting Madame Monsieur')
        # Try to load tokens
        try:
            self.load_configuration()
            with open('tokens', 'r') as f:
                f = f.readlines()
                self.DISCORD_WEBHOOK_URL = f[0].split('=')[1].strip('\n') if not DEVELOP else f[1].split('=')[1].strip('\n')
                self.BLAGUE_API_KEY = f[2].split('=')[1].strip('\n')
                self.NEWS_API_KEY = f[3].split('=')[1].strip('\n')
                return None
        except Exception as e:
            logging.error(f'Could not load tokens: {e}')
        # If tokens file failed, try to load tokens from environment variables (for Github Actions)
        try:
            self.BLAGUE_API_KEY = os.environ['BLAGUE_API_KEY']
            self.DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL'] if not DEVELOP else os.environ['DISCORD_WEBHOOK_URL_DEV']
            self.NEWS_API_KEY = os.environ['NEWS_API_KEY']
            self.NEWS_API_KEY = os.environ['NEWS_API_KEY']
        except Exception as e:
            logging.error(f'Could not load tokens: {e}')
            sys.exit(1)
             
    def load_configuration(self):
        self.config = configparser.ConfigParser()
        self.config.read('./config.conf')
        
    def send_meteo(self, ville):
        """
        It sends a request to the Discord webhook URL with the meteo image as an embed
        
        :param ville: The city you want to get the weather for
        :return: The response's status code from the POST request.
        """
        
        embed = {
            'title': 'Bonjour, c\'est la météo', 
            'url': f'https://wttr.in/{ville}.png?qp1m', 
            'image': {
                'url': f'https://wttr.in/{ville}.png?qp1m&lang=fr'
                }
            }
        
        data = {
            'content': '',
            'embeds': [embed]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        return requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('latin-1'), headers=headers).status_code

    def send_joke(self, type):
        """
        It sends a joke to a Discord webhook
        
        :param type: The type of joke you want to send
        :return: The response's status code from the POST request.
        """
        
        blague = requests.get(f'https://www.blagues-api.fr/api/type/{type}/random', headers={'Authorization': f'Bearer {self.BLAGUE_API_KEY}'}).json()

        embed = {
            'title': 'Bonjour, c\'est la blague',
            'description': blague['joke'] + ' ' + blague['answer'],
        }
        
        data = {
            'content': '',
            'embeds': [embed]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
            
        return requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('latin-1'), headers=headers).status_code

    def send_fact(self, language='fr'):
        """
        It gets a random fact from a website, translates it to the language specified, and sends it to the
        webhook URL

        :param language: The language you want the fact to be translated to
        :return: The response's status code from the POST request.
        """
        
        try:
            fact = requests.get('https://fungenerators.com/random/facts/').text
            fact = GoogleTranslator(source='english', target=language).translate(fact.split('<h2 class="wow fadeInUp animated"  data-wow-delay=".6s">')[1].split('<span class="text-muted">')[0])
        except Exception as e:
            logging.error(f'Could not get fact: {e}')
            return -1
        
        embed = {
            'title': 'Bonjour, c\'est le fact',
            'description': fact,
        }
        
        data = {
            'content': '',
            'embeds': [embed]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
            
        return requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('latin-1'), headers=headers).status_code

    def send_news(self):
        """
        It sends news to a Discord channel using a webhook

        :param newsApi: The API key for the news API
        :return: A list of response code.
        """
        
        url = "https://google-news1.p.rapidapi.com/topic-headlines"

        querystring = {"topic":"TECHNOLOGY","country":"FR","lang":"fr","limit":"5"}

        headers = {
            "X-RapidAPI-Key": self.NEWS_API_KEY,
            "X-RapidAPI-Host": "google-news1.p.rapidapi.com"
        }

        news = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)

        timeOfDay = 'du DEBUG'
        if time.localtime().tm_hour == 8:
            timeOfDay = 'du matin!'
        elif time.localtime().tm_hour == 13:
            timeOfDay = 'de l\'aprÃ¨s-midi!'
        elif time.localtime().tm_hour == 18:
            timeOfDay = 'du soir!'    

        embed = {
            'title': 'Bonjour, c\'est les actus ' + timeOfDay,
            'description': 'Les 5 dernières actualités tech. du moment.',
            'url': 'https://rapidapi.com/ubillarnet/api/google-news1/details',
        }
        data = {
            'content': '',
            'embeds': [embed]
        }
        headers = {
            'Content-Type': 'application/json'
        }
        responseCode = [requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('latin-1'), headers=headers).status_code]

        for i in news['articles']:
            embed = {
                'title': i['title'],
                'url': i['link'],
            }
            data = {
                'content': '',
                'embeds': [embed]
            }
            headers = {
                'Content-Type': 'application/json'
            }
            responseCode.append(requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('utf-8'), headers=headers).status_code)

        return responseCode
        
    def send_info(self, info, infoUrl, imageUrl):
        """
        It sends a message to a Discord webhook
        
        :param info: The text that will be displayed in the embed
        :param infoUrl: The URL of the info
        :param imageUrl: The URL of the image you want to send
        :return: The status code of the request.
        """
        
        embed = {
            'title': 'Bonjour, c\'est une info',
            'description': info,
            'url': infoUrl,
            'image' : {'url' : imageUrl},
        }
        
        data = {
            'content': '',
            'embeds': [embed]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
            
        return requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('utf-8'), headers=headers).status_code
        
    def send_trending_tickers(self):
        """
        It gets the trending tickers from Yahoo Finance, formats them into a Discord embed, and sends
        them to a Discord webhook
        :return: The status code of the request.
        """
        
        try:
            response = requests.get('https://finance.yahoo.com/trending-tickers').text.split('\n')
            titles = response[44].split('title="')

            for i in range(len(titles)):
                if 'next"><svg class="' in titles[i]:
                    break

            trendingTitles = []
            for i in range(i+2, len(titles)):
                if titles[i].split('"')[0] != '':
                    titleName = titles[i].split('"')[0]
                    titleValue = titles[i].split('value="')[1].split('"')[0]
                    titleChange = str(round(float(titles[i].split('value="')[4].split('"')[0]), 2))
                    titleChange = f'+{titleChange}' if '-' not in titleChange else titleChange
                    trendingTitles.append([titleName, titleValue, titleChange])
            trendingTitles = sorted(trendingTitles, key=lambda x: float(x[2]), reverse=True)
            
            embed = {
                'title': 'Bonjour, c\'est les trending tickers du moment',
                'description': ''.join(f'{trendingTitle[0]} : US$ {trendingTitle[1]} ({trendingTitle[2]}%)\n' for trendingTitle in trendingTitles),
                'url': 'https://finance.yahoo.com/trending-tickers',
            }
            
            data = {
                'content': '',
                'embeds': [embed]
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
                
            return requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('utf-8'), headers=headers).status_code
        except Exception as e:
            logging.error(f'Error while getting trending tickers: {str(e)}')
            

        
if __name__ == '__main__':
    mM = MadameMonsieur()
    meteoConfig, jokeConfig, newsConfig, factConfig, tickersConfig = 0, 0, 0, 0, 0
    
    try:
        if int(mM.config['MAIN']['meteo']):
            meteoConfig = [mM.config['TIME PERIOD']['meteo_tp'].split(','), mM.config['FREQUENCY']['meteo_frequency'], mM.config['LANGUAGE']['meteo_language']]
        if int(mM.config['MAIN']['joke']):
            jokeConfig = [mM.config['TIME PERIOD']['joke_tp'].split(','), mM.config['FREQUENCY']['joke_frequency'], mM.config['LANGUAGE']['joke_language']]
        if int(mM.config['MAIN']['fact']):
            factConfig = [mM.config['TIME PERIOD']['fact_tp'].split(','), mM.config['FREQUENCY']['fact_frequency'], mM.config['LANGUAGE']['fact_language']]     
        if int(mM.config['MAIN']['news']):
            newsConfig = [mM.config['TIME PERIOD']['news_tp'].split(','), mM.config['FREQUENCY']['news_frequency'], mM.config['LANGUAGE']['news_language']]
        if int(mM.config['MAIN']['tickers']):
            tickersConfig = [mM.config['TIME PERIOD']['tickers_tp'].split(','), mM.config['FREQUENCY']['tickers_frequency'], None]
            
        if meteoConfig:
            meteoConfig.append([i for i in range(int(meteoConfig[0][0]), int(meteoConfig[0][1])+1, int(meteoConfig[1]))])
            meteoConfig.append(1)
                    
        if jokeConfig:
            jokeConfig.append([i for i in range(int(jokeConfig[0][0]), int(jokeConfig[0][1])+1, int(jokeConfig[1]))])
            jokeConfig.append(1)
            
        if factConfig:
            factConfig.append([i for i in range(int(factConfig[0][0]), int(factConfig[0][1])+1, int(factConfig[1]))])
            factConfig.append(1)
        
        if newsConfig:
            newsConfig.append([i for i in range(int(newsConfig[0][0]), int(newsConfig[0][1])+1, int(newsConfig[1]))])
            newsConfig.append(1)
            
        if tickersConfig:
            tickersConfig.append([i for i in range(int(tickersConfig[0][0]), int(tickersConfig[0][1])+1, int(tickersConfig[1]))])
            tickersConfig.append(1)
    except Exception as e:
        logging.error(f'Error while parsing config: {str(e)}')
        
    while 1:
        try:
            if meteoConfig:
                if time.localtime().tm_hour in meteoConfig[3] and time.localtime().tm_min == 0 and meteoConfig[4] == 1 or DEBUG:
                    logging.info('Sent meteo - ' + str(mM.send_meteo('Lyon')))
                    meteoConfig[4] = time.time()
                if time.time() - meteoConfig[4] > 60 and meteoConfig[4] != 1:
                    meteoConfig[4] = 1
                    
            if jokeConfig:
                if time.localtime().tm_hour in jokeConfig[3] and time.localtime().tm_min == 0 and jokeConfig[4] == 1 or DEBUG:
                    logging.info('Sent joke - ' + str(mM.send_joke('dark')))
                    jokeConfig[4] = time.time()
                if time.time() - jokeConfig[4] > 60 and jokeConfig[4] != 1:
                    jokeConfig[4] = 1
                    
            if factConfig:
                if time.localtime().tm_hour in factConfig[3] and time.localtime().tm_min == 0 and factConfig[4] == 1 or DEBUG:
                    logging.info('Sent fact - ' + str(mM.send_fact('fr')))
                    factConfig[4] = time.time()
                if time.time() - factConfig[4] > 60 and factConfig[4] != 1:
                    factConfig[4] = 1
                    
            if newsConfig:
                if time.localtime().tm_hour in newsConfig[3] and time.localtime().tm_min == 0 and newsConfig[4] == 1 or DEBUG:
                    logging.info('Sent news - ' + str(mM.send_news()))
                    newsConfig[4] = time.time()
                if time.time() - newsConfig[4] > 60 and newsConfig[4] != 1:
                    newsConfig[4] = 1
            
            if tickersConfig:
                if time.localtime().tm_hour in tickersConfig[3] and time.localtime().tm_min == 0 and tickersConfig[4] == 1 or DEBUG:
                    logging.info('Sent trending tickers - ' + str(mM.send_trending_tickers()))
                    tickersConfig[4] = time.time()
                if time.time() - tickersConfig[4] > 60 and tickersConfig[4] != 1:
                    tickersConfig[4] = 1

        except Exception as e:
            logging.error(f'Error while sending message: {str(e)}')
        
        time.sleep(10 if DEBUG else 1)
                    
# TODO:
# - update tests for configuration file
# - add some sort of docs lol
# - add different language support
# - add different meteo location support
