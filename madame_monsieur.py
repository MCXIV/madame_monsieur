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

# 3rd party
import requests
from deep_translator import GoogleTranslator

# DEBUG
DEBUG = 0

# --------------------------------------------------

def send_meteo(webhook_url, ville):
    """
    It sends a request to the Discord webhook URL with the meteo image as an embed
    
    :param webhook_url: The URL of the webhook you want to send the message to
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

    return requests.post(webhook_url, data=json.dumps(data).encode('utf-8'), headers=headers).status_code

def send_joke(webhook_url, jokeApi, type):
    """
    It sends a joke to a Discord webhook
    
    :param webhook_url: The webhook URL you copied from the Discord channel
    :param jokeApi: The API key for the joke API
    :param type: The type of joke you want to send
    :return: The response's status code from the POST request.
    """
    
    blague = requests.get(f'https://www.blagues-api.fr/api/type/{type}/random', headers={'Authorization': f'Bearer {jokeApi}'}).json()

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
        
    return requests.post(webhook_url, data=json.dumps(data).encode('utf-8'), headers=headers).status_code

def send_fact(webhook_url, language='fr'):
    """
    It gets a random fact from a website, translates it to the language specified, and sends it to the
    webhook URL
    
    :param webhook_url: The webhook URL you got from the Discord server
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
        
    return requests.post(webhook_url, data=json.dumps(data).encode('utf-8'), headers=headers).status_code

def send_news(webhook_url, newsApi):
    """
    It sends news to a Discord channel using a webhook
    
    :param webhook_url: The URL of the webhook you want to send the message to
    :param newsApi: The API key for the news API
    :return: A list of response code.
    """
    
    url = "https://google-news1.p.rapidapi.com/topic-headlines"

    querystring = {"topic":"TECHNOLOGY","country":"FR","lang":"fr","limit":"5"}

    headers = {
        "X-RapidAPI-Key": newsApi,
        "X-RapidAPI-Host": "google-news1.p.rapidapi.com"
    }

    news = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
    
    responseCode = []
    
    timeOfDay = 'du DEBUG'
    if time.localtime().tm_hour == 8:
        timeOfDay = 'du matin!'
    elif time.localtime().tm_hour == 13:
        timeOfDay = 'de l\'après-midi!'
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
    responseCode.append(requests.post(webhook_url, data=json.dumps(data).encode('utf-8'), headers=headers).status_code)
    
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
        responseCode.append(requests.post(webhook_url, data=json.dumps(data).encode('utf-8'), headers=headers).status_code)

    return responseCode
    
def send_info(webhook_url, info, infoUrl, imageUrl):
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
        
    return requests.post(webhook_url, data=json.dumps(data).encode('utf-8'), headers=headers).status_code
    
if __name__ == '__main__':
    logging.basicConfig(filename='madame_monsieur.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info('Starting Madame Monsieur')
    try:
        with open('tokens', 'r') as f:
            tokens = f.readlines()
            discordWebhook = tokens[0].split('=')[1].strip('\n')
            jokeApi = tokens[1].split('=')[1].strip('\n')
            newsApi = tokens[2].split('=')[1].strip('\n')
            logging.info('Tokens loaded')
    except Exception as e:
        logging.error('Error while reading tokens')
        sys.exit(e)

    flag_meteo = 1
    flag_joke = 1
    flag_fact = 1
    flag_news = 1

    while 1:
        if time.localtime().tm_hour == 8 and time.localtime().tm_min == 0 and flag_meteo == 1 or DEBUG:
            logging.info('Sent meteo - ' + str(send_meteo(discordWebhook, 'Lyon')))
            logging.info('Sent meteo - ' + str(send_meteo(discordWebhook, 'Oyonnax')))
            flag_meteo = time.time()
        if time.localtime().tm_hour in [9, 11, 13, 15, 17, 19, 21] and time.localtime().tm_min == 0 and flag_joke == 1 or DEBUG:
            logging.info('Sent joke - ' + str(send_joke(discordWebhook, jokeApi, 'dark')))
            flag_joke = time.time()
        if time.localtime().tm_hour in [10, 12, 14, 16, 18, 20, 22] and time.localtime().tm_min == 0 and flag_fact == 1 or DEBUG:
            logging.info('Sent fact - ' +  str(send_fact(discordWebhook, 'fr')))
            flag_fact = time.time()
        if time.localtime().tm_hour in [8, 13, 18] and time.localtime().tm_min == 0 and flag_news == 1 or DEBUG:    
            logging.info('Sent news - ' + str(send_news(discordWebhook, newsApi)))
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
