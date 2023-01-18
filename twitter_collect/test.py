
"""
Ce module contient des fonction de tests des fonctions
permettant la récueration de tweets
"""
import pandas as pd
from twitter_collect import connection_setup
#from twitter_collect import fetch_tweets
from twitter_collect import utils


def test_connexion():
    """
    Test la fonction twitter_setup
    """

    assert connection_setup.twitter_setup() is not None


def test_query():
    """
    Test la fonction make_query
    """

    assert utils.make_query(
        "test", subject=True) == 'test lang:en -filter:retweets'
    assert utils.make_query(
        "NASA", user=True) == 'from:NASA lang:en -filter:retweets'
    assert utils.make_query(
        "WorldCup", hasthag=True) == '#WorldCup lang:en -filter:retweets'


def test_tweet_scapper():
    """
    Test la fonction tweet_scraper
    """

    api = connection_setup.twitter_setup()
    tweet_limit = 5
    tweets = utils.tweet_scraper(
        api, query="f", tweet_limit=tweet_limit)

    assert isinstance(tweets, pd.DataFrame)

    assert tweets.shape[0] == tweet_limit
