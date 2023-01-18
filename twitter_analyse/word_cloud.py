
"""
    Ce programme genère une image wordcloud
"""

from wordcloud import WordCloud
#from PIL import Image
import numpy as np
#import matplotlib.pyplot as plt


def generate_wordcloud(dataframe, feeling="happy", contour_width=0,
                       coutor_color='blue', background_color='black'):
    """Gènere un wordcloud

    Args:
        df (dataframe): contient les emotions associés aux tweets
        feeling (str, optional): Determine la forme de l'emoji. Defaults to "happy".
        contour_width (int, optional): Defaults to 0.
        coutor_color (str, optional):  Defaults to 'blue'.
        background_color (str, optional): Defaults to 'black'.

    Raises:
        Exception: Si le feeling n'est pas dans la base des feelings
    """

    possible_feelings = ["joy", "anger",
                         "sadness", "fear", "disgust", "surprise"]

    if feeling not in possible_feelings:
        raise Exception('This feeling does not exist')

    mask = np.load("twitter_analyse/masks/" + feeling + ".npy")

    text = dataframe["full_text"].str.cat(
        others=None, sep=None, na_rep=None, join='left')
    text = text.replace("https://t.co/", '')
    text = text.replace("&amp", '')

    wordcloud = WordCloud(max_words=1000, background_color=background_color, mask=mask,
                          contour_width=contour_width, contour_color=coutor_color,
                          width=1600, height=800)

    cloud = wordcloud.generate(text)

    return cloud
