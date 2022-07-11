#!/usr/bin/python
# -*- coding: latin-1 -*-

# --------------------------------------------------
# Madame MOnsieur webhook bot for Discord
# Quentin Dufournet, 2022
# --------------------------------------------------

# Built-in
import os

# 3rd party
import pytest
import madame_monsieur as script


def load_tokens():
    """
    It opens the file 'tokens' and reads the lines, then splits the lines by the '=' character and
    returns the second item in the list.
    :return: the discordWebhook, jokeApi, and newsApi variables.
    """
    
    try:
        with open('tokens', 'r') as f:
            f = f.readlines()
            DISCORD_WEBHOOK_URL = f[0].split('=')[1].strip('\n')
            BLAGUE_API_KEY = f[1].split('=')[1].strip('\n')
            NEWS_API_KEY = f[2].split('=')[1].strip('\n')
    except Exception as e:
        BLAGUE_API_KEY = os.environ['BLAGUE_API_KEY']
        DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
        NEWS_API_KEY = os.environ['NEWS_API_KEY']
    
    return DISCORD_WEBHOOK_URL, BLAGUE_API_KEY, NEWS_API_KEY if '' not in [DISCORD_WEBHOOK_URL, BLAGUE_API_KEY, NEWS_API_KEY] else None

def test_send_meteo():
    """ Scenario:
    * Send a request to the Discord webhook URL with the meteo image as an embed
    * Check the response's status code
    """
    
    assert script.send_meteo(load_tokens()[0], 'Lyon') == 204
    
def test_send_joke():
    """ Scenario:
    * Get a random joke from the API
    * Send it to the Discord webhook
    * Check the response's status code
    """
    
    assert script.send_joke(load_tokens()[0], load_tokens()[1], 'dark') == 204
    
def test_send_fact():
    """ Scenario:
    * Get a random fact from the API
    * Send it to the Discord webhook
    * Check the response's status code
    """
    assert script.send_fact(load_tokens()[0]) == 204

def test_send_news():
    """ Scenario:
    * Get the latest news from the API
    * Send it to the Discord webhook
    * Check the response's status code
    """
    assert script.send_news(load_tokens()[0], load_tokens()[2]) == [204, 204, 204, 204, 204, 204]
    
def test_send_info():
    """ Scenario:
    * Send a request to the Discord webhook URL with the info as an embed
    * Check the response's status code
    """
    assert script.send_info(load_tokens()[0], 'TEST INFO', 'https://www.github.com', 'https://github.githubassets.com/app-icon-192.png') == 204
