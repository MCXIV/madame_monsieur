#!/usr/bin/python
# -*- coding: latin-1 -*-

# --------------------------------------------------
# Madame MOnsieur webhook bot for Discord
# Quentin Dufournet, 2022
# --------------------------------------------------

# Built-in


# 3rd party
import pytest
import madame_monsieur as script


def load_tokens():
    """
    It opens the file 'tokens' and reads the lines, then splits the lines by the '=' character and
    returns the second item in the list.
    :return: the discordWebhook, jokeApi, and newsApi variables.
    """
    
    with open('tokens', 'r') as f:
        f = f.readlines()
        discordWebhook = f[0].split('=')[1].strip('\n')
        jokeApi = f[1].split('=')[1].strip('\n')
        newsApi = f[2].split('=')[1].strip('\n')
    return discordWebhook, jokeApi, newsApi if '' not in [discordWebhook, jokeApi, newsApi] else None

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
    assert script.send_info(load_tokens()[0], 'TEST INFO', 'https://www.google.fr', 'https://www.google.fr/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png') == 204