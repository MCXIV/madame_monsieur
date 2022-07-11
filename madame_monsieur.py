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

# 3rd party
import requests
from deep_translator import GoogleTranslator

# DEBUG
DEBUG = 0

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
            with open('tokens', 'r') as f:
                f = f.readlines()
                self.DISCORD_WEBHOOK_URL = f[0].split('=')[1].strip('\n')
                self.BLAGUE_API_KEY = f[1].split('=')[1].strip('\n')
                self.NEWS_API_KEY = f[2].split('=')[1].strip('\n')
                return None
        except Exception as e:
            logging.error(f'Could not load tokens: {e}')
        # If tokens file failed, try to load tokens from environment variables (for Github Actions)
        try:
            self.BLAGUE_API_KEY = os.environ['BLAGUE_API_KEY']
            self.DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
            self.NEWS_API_KEY = os.environ['NEWS_API_KEY']
        except Exception as e:
            logging.error(f'Could not load tokens: {e}')
            sys.exit(1)
    
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

        return requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('utf-8'), headers=headers).status_code

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
            
        return requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('utf-8'), headers=headers).status_code

    def send_fact(self, language='fr'):
        """
        It gets a random fact from a website, translates it to the language specified, and sends it to the
        webhook URL

        :param language: The language you want the fact to be translated to
        :return: The response's status code from the POST request.
        """
        
        fact = requests.get('https://fungenerators.com/random/facts/').text
        fact = GoogleTranslator(source='english', target=language).translate(fact.split('<h2 class="wow fadeInUp animated"  data-wow-delay=".6s">')[1].split('<span class="text-muted">')[0])
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
            
        return requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('utf-8'), headers=headers).status_code

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
            'description': 'Les 5 derniÃ¨res actualitÃ©s tech. du moment.',
            'url': 'https://rapidapi.com/ubillarnet/api/google-news1/details',
        }
        data = {
            'content': '',
            'embeds': [embed]
        }
        headers = {
            'Content-Type': 'application/json'
        }
        responseCode = [requests.post(self.DISCORD_WEBHOOK_URL, data=json.dumps(data).encode('utf-8'), headers=headers).status_code]

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
        
        
if __name__ == '__main__':
    mM = MadameMonsieur()

    # Flags for the different types of messages
    flag_meteo = 1
    flag_joke = 1
    flag_fact = 1
    flag_news = 1

    while 1:
        # If the time is 8:00, send the meteo
        if time.localtime().tm_hour == 8 and time.localtime().tm_min == 0 and flag_meteo == 1 or DEBUG:
            logging.info('Sent meteo - ' + str(mM.send_meteo('Lyon')))
            logging.info('Sent meteo - ' + str(mM.send_meteo('Oyonnax')))
            flag_meteo = time.time()
        # If the hour is even (from 9AM to 9PM), send the joke
        if time.localtime().tm_hour in [9, 11, 13, 15, 17, 19, 21] and time.localtime().tm_min == 0 and flag_joke == 1 or DEBUG:
            logging.info('Sent joke - ' + str(mM.send_joke('dark')))
            flag_joke = time.time()
        # If the hour is odd (from 10AM to 10PM), send a fact
        if time.localtime().tm_hour in [10, 12, 14, 16, 18, 20, 22] and time.localtime().tm_min == 0 and flag_fact == 1 or DEBUG:
            logging.info('Sent fact - ' +  str(mM.send_fact()))
            flag_fact = time.time()
        # If the hour is 8AM, or 1PM, or 6PM, send the news
        if time.localtime().tm_hour in [8, 13, 18] and time.localtime().tm_min == 0 and flag_news == 1 or DEBUG:    
            logging.info('Sent news - ' + str(mM.send_news()))
            flag_news = time.time()

        if time.time() - flag_meteo >= 86400 and flag_meteo != 1:
            flag_meteo = 1
        if time.time() - flag_joke >= 7200 and flag_joke != 1:
            flag_joke = 1
        if time.time() - flag_fact >= 7200 and flag_fact != 1:
            flag_fact = 1
        if time.time() - flag_news >= 18000 and flag_news != 1:
            flag_news = 1

        time.sleep(10 if DEBUG else 1)
