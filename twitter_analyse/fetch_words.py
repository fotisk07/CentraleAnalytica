
"""
A partir d'un dataframe, on fait une selection des 12
mots les plus fréquents pour ensuite créer la mosaïque d'images.

"""

from collections import Counter
from textblob import TextBlob


def frequent_words(dataframe, num):
    """recherche les n mots les plus fréquents dans
    un dataframe de tweets

    Args:
        dataframe (datafram): contient les tweets
        num (integer): nombre de mots recherchés

    Returns:
        list(strings): liste des mots n mots les plus fréquents
    """
    text = ""

    for tweet in dataframe["full_text"]:

        text += " " + tweet

    text = text.lower()

    # On enlève au texte les chaines de carctères inutiles qui reviennent souvent

    remove = ["https://t.co/", "&amp", "@",
              "▫️", "•", "'", " ’ ", "\"", " i ", " t ", " s "]
    for mot in remove:
        text = text.replace(mot, ' ')

    text = TextBlob(text)

    nouns_in_text = [w for (w, pos) in text.tags if (
        pos[0] == 'N' or pos[0] == 'NN' or pos[0] == 'NNP' or pos[0] == 'NNS' or pos[0] == 'NNPS')]

    # on enlève les mots de moins de 3 caractères
    i = 0
    while i < len(nouns_in_text):
        if len(nouns_in_text[i]) < 3:
            nouns_in_text.pop(i)
        i = i+1

    # On crée une liste avec des couples de la forme ("mot", nombre d'occurrences).
    counter = Counter(nouns_in_text)
    # on supprime le mot 's' qui apparait tout le temps
    del counter['s']
    # On prend dans la liste Counter les n mots les plus fréquents.
    most_frequent = counter.most_common(num)

    # Finalement, on fait une liste uniquement avec les mots.
    most_frequent_words = [couple[0] for couple in most_frequent]

    return most_frequent_words
