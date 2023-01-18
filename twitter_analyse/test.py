
"""
    module de test de fonctions reliées à wordcloud
"""

import pandas as pd
#from twitter_analyse import emotions_fct
#from twitter_analyse import mosaic
from twitter_analyse import word_cloud
from twitter_analyse import fetch_words


def test_word_cloud():
    """
    Test la fonction generate_wordcloud
    """

    data = ["bonjour", "sup"]
    dataframe = pd.DataFrame(data, columns=['full_text'])
    assert word_cloud.generate_wordcloud(dataframe) is not None


def test_relevant_words():
    """
    Test la fonction frequent_words
    """

    data = ["bonjour", "sup"]
    dataframe = pd.DataFrame(data, columns=['full_text'])
    assert fetch_words.frequent_words(dataframe, 2) is not None
