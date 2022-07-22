#!/usr/bin/python
# -*- coding: latin-1 -*-

# --------------------------------------------------
# Madame MOnsieur webhook bot for Discord
# Quentin Dufournet, 2022
# --------------------------------------------------

# Built-in


# 3rd party
import madame_monsieur as script

# --------------------------------------------------

def test_send_meteo():
    """ Scenario:
    * Send a request to the Discord webhook URL with the meteo image as an embed
    * Check the response's status code
    """
    mM = script.MadameMonsieur()
    assert mM.send_meteo('Lyon') == 204
    
def test_send_joke():
    """ Scenario:
    * Get a random joke from the API
    * Send it to the Discord webhook
    * Check the response's status code
    """
    mM = script.MadameMonsieur()
    assert mM.send_joke('dark') == 204
    
def test_send_fact():
    """ Scenario:
    * Get a random fact from the API
    * Send it to the Discord webhook
    * Check the response's status code
    """
    mM = script.MadameMonsieur()
    assert mM.send_fact() == 204

def test_send_news():
    """ Scenario:
    * Get the latest news from the API
    * Send it to the Discord webhook
    * Check the response's status code
    """
    mM = script.MadameMonsieur()
    assert mM.send_news() == [204, 204, 204, 204, 204, 204]
    
def test_send_info():
    """ Scenario:
    * Send a request to the Discord webhook URL with the info as an embed
    * Check the response's status code
    """
    mM = script.MadameMonsieur()
    assert mM.send_info('TEST INFO', 'https://github.com/MCXIV/madame_monsieur', 'https://avatars.githubusercontent.com/u/43221669?v=4') == 204

def test_send_trending_stocks():
    """ Scenario:
    * Get the trending stocks from Yahoo Finance
    * Parse the raw html source code to a Discord embed message
    * Send the results
    * Check the response's status code
    """
    mM = script.MadameMonsieur()
    assert mM.send_trending_stocks() == 204