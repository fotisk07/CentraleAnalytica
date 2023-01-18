
"""
    Met en forme un dataframe a partir d'un json contenant des tweets
"""

import tweepy
import pandas as pd
import numpy as np


def tweet_scraper(api, query, tweet_mode="extended", count=100, tweet_limit=1000):
    '''
    Returns a dataframe object with tweets corresponding to a certain query

    '''

    data = {
        "user_id": [],
        "screen_name": [],
        "name": [],
        "verified": [],
        "id": [],
        "created_at": [],
        "full_text": [],
        "retweet_count": [],
        "favorite_count": [],
        "hashtags": [],
        "user_mentions": [],
        "in_reply_to_user_id": [],
        "in_reply_to_screen_name": [],
        "is_quote_status": [],
        "is_retweet": [],
        "retweet_og_id": [],  # the ID of the original retweeted tweet
        "retweet_og_author_id": [],  # the original author ID of a retweeted tweet
        # the original author screen name of a retweeted tweet
        "retweet_og_author_screen_name": [],
        "retweet_og_author_name": [],  # the original author's name of a retweeted tweet
        "retweet_og_date": [],  # the date of the original tweet
        "retweet_og_full_text": [],  # OG full text of the retweet
        "retweet_og_retweet_count": [],  # OG retweet count
        "retweet_og_favorite_count": []  # OG favorite count
    }

    # Search the tweets as we've already done, but this time, plug in the paremeter values
    # from the function arguments:

    for tweet in tweepy.Cursor(api.search_tweets, q=query,
                               tweet_mode=tweet_mode, count=count).items(tweet_limit):

        # User ID:
        data["user_id"].append(tweet.user.id)
        # Screen name:
        data["screen_name"].append(tweet.user.screen_name)
        # Name:
        data["name"].append(tweet.user.name)
        # verified status:
        data["verified"].append(tweet.user.verified)

        # Tweet ID:
        data["id"].append(tweet.id)
        # Date:
        data["created_at"].append(tweet.created_at)
        # Full text of tweet:
        data["full_text"].append(tweet.full_text)
        # Get retweet count:
        data["retweet_count"].append(tweet.retweet_count)
        # Get favorite count:
        data["favorite_count"].append(tweet.favorite_count)

        hashtags = []
        # Try to get hashtags; if there is an error, then there are no hashtags
        # and we can pass:
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
        except Exception:
            pass

        # Now append the hashtag list to our dataset! If there are no
        # hashtags, just set it equal to NaN:
        if len(hashtags) == 0:
            data["hashtags"].append(np.nan)
        else:
            data["hashtags"].append(hashtags)

        # We do the same thing for user mentions:
        mentions = []
        try:
            for mention in tweet.entities["user_mentions"]:
                mentions.append(mention["screen_name"])
        except Exception:
            pass

        if len(mentions) == 0:
            data["user_mentions"].append(np.nan)
        else:
            data["user_mentions"].append(mentions)

        # In reply to user id:
        data["in_reply_to_user_id"].append(tweet.in_reply_to_user_id)
        # In reply to user screen name:
        data["in_reply_to_screen_name"].append(tweet.in_reply_to_screen_name)
        # Check if quote status:
        data["is_quote_status"].append(tweet.is_quote_status)

        # We need to check if a tweet is a retweet ourselves. We can do this by checking
        # if the retweeted_status key is present in the JSON:
        if "retweeted_status" in tweet._json.keys():
            # Then it is a retweet:
            data["is_retweet"].append(True)
            # Get OG tweet id:
            data["retweet_og_id"].append(str(tweet.retweeted_status.id))
            # Get OG author ID:
            data["retweet_og_author_id"].append(
                str(tweet.retweeted_status.user.id))
            # Get OG author screen name:
            data["retweet_og_author_screen_name"].append(
                tweet.retweeted_status.user.screen_name)
            # Get OG author name:
            data["retweet_og_author_name"].append(
                tweet.retweeted_status.user.name)
            # Get date of OG tweet:
            data["retweet_og_date"].append(tweet.retweeted_status.created_at)
            # Get OG full text:
            data["retweet_og_full_text"].append(
                tweet.retweeted_status.full_text)
            # Get OG retweet count:
            data["retweet_og_retweet_count"].append(
                tweet.retweeted_status.retweet_count)
            # Get OG favorite count:
            data["retweet_og_favorite_count"].append(
                tweet.retweeted_status.favorite_count)
        else:
            # Set is_retweet to false and all other values to np.nan:
            data["is_retweet"].append(False)
            data["retweet_og_id"].append(np.nan)
            data["retweet_og_author_id"].append(np.nan)
            data["retweet_og_author_screen_name"].append(np.nan)
            data["retweet_og_author_name"].append(np.nan)
            data["retweet_og_date"].append(np.nan)
            data["retweet_og_full_text"].append(np.nan)
            data["retweet_og_retweet_count"].append(np.nan)
            data["retweet_og_favorite_count"].append(np.nan)

    dataframe = pd.DataFrame(data)

    return dataframe


def make_query(key, user=False, subject=False, hasthag=False):
    """Make Querry

    Args:
        key (_type_): _description_
        user (bool, optional): _description_. Defaults to False.
        subject (bool, optional): _description_. Defaults to False.
        hasthag (bool, optional): _description_. Defaults to False.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    if user:
        query = "from:" + key + " lang:en -filter:retweets"

    elif hasthag:
        query = "#" + key + " lang:en -filter:retweets"

    elif subject:
        query = key + " lang:en -filter:retweets"
    else:
        raise Exception("No category specified")

    return query
