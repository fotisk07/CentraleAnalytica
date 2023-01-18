
"""
    Récupère des tweets et crée un fichier json avec
"""
import pandas as pd
from twitter_collect import utils
from twitter_collect import connection_setup



def create_data(key, subject=False, user=False, hashtag=False, tweet_limit=100):
    """_summary_

    Args:
        key (_type_): _description_
        subject (bool, optional): _description_. Defaults to False.
        user (bool, optional): _description_. Defaults to False.
        hashtag (bool, optional): _description_. Defaults to False.
        tweet_limit (int, optional): _description_. Defaults to 100.
    """

    api = connection_setup.twitter_setup()

    query = utils.make_query(key, subject=subject, user=user, hasthag=hashtag)

    data = utils.tweet_scraper(api, query=query, tweet_limit=tweet_limit)

    data.to_json("twitter_data.json")


def get_data(path):
    """_summary_

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """

    dataframe = pd.read_json(path, dtype="str")

    return dataframe
