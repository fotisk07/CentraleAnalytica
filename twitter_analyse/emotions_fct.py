
"""
    Ce programme permet d'analyser un dataframe de tweet (sentiments)
    et de renvoyer des dataframes prêt à la visualisation
"""
import math
import pandas as pd
from nrclex import NRCLex
from textblob import TextBlob


def emo_analysis(dataframe):
    """Analyse les sentiments présents dans les tweets fournis

    Args:
        dataframe (dataframe): dataframe avec les tweets

    Returns:
        list(dataframe,dataframe): listes de deux dataframes.
        Le premier contient le traitement des emotions
        et le second le traitement global
    """

    # on ne garde que les textes
    data_text = dataframe['full_text']

    # on crée une chaine de caractère contenant tous les textes concaténés
    stack = data_text.str.cat(others=None, sep=None,
                              na_rep=None, join='left')

    # on calcule les occurences des mots par émotion
    scores_dict = NRCLex(stack).raw_emotion_scores

    # si aucun mot n'a été trouvés pour une catégorie, on crée la case et on la met à zéro
    for word in ['fear', 'anger', 'joy', 'sadness', 'disgust', 'surprise', 'negative', 'positive']:
        if word not in scores_dict:
            scores_dict[word] = 0

    # PARTIE 1 : EMOTIONS
    # pour calculer la fréquence on a besoin d'un compteur des 6 émotions
    emo_tot = scores_dict['fear'] + scores_dict['anger'] + scores_dict['joy'] + \
        scores_dict['sadness'] + scores_dict['disgust'] + \
        scores_dict['surprise']

    if emo_tot == 0:
        dataframe1 = pd.DataFrame({
            'Emotion': ['fear', 'anger', 'joy', 'sadness', 'disgust', 'surprise'],
            'Frequency': [0,
                          0,
                          0,
                          0,
                          0,
                          0]
        })

    else:
        # on crée le dataframe des émotions
        dataframe1 = pd.DataFrame({
            'Emotion': ['fear', 'anger', 'joy', 'sadness', 'disgust', 'surprise'],
            'Frequency': [scores_dict['fear']/emo_tot,
                          scores_dict['anger']/emo_tot,
                          scores_dict['joy']/emo_tot,
                          scores_dict['sadness']/emo_tot,
                          scores_dict['disgust']/emo_tot,
                          scores_dict['surprise']/emo_tot]
        })

    # PARTIE 2 : OTHER DATA
    global_tot = scores_dict['positive'] + scores_dict['negative']
    stack_tb = TextBlob(stack)

    fav = dataframe['favorite_count']
    fav = fav.astype(float)
    fav_freq = fav.mean()/30600
    print(fav_freq)
    alpha = 10**8

    # pour la fame, on fait une comparaison aux 10 teets récents
    # les plus likés d'Elon Musk : 30 600 likes
    # on a donc un résultat entre 0 et 1
    # on veut zoomer proche de zéro, et tasser proche de 1, en gardant des résultats entre 0 et 1
    # on utilise la fonction f(x)=log(1+alpha*x)/log(1+alpha)

    if global_tot == 0:
        dataframe2 = pd.DataFrame({
            'Global': ['Positivity', 'Subjectivity', 'Fame'],
            'Frequency': [0,
                          stack_tb.sentiment.subjectivity,
                          math.log(1+alpha*fav_freq)/math.log(1+alpha)]

        })

    else:
        dataframe2 = pd.DataFrame({
            'Global': ['Positivity', 'Subjectivity', 'Fame'],
            'Frequency': [scores_dict['positive']/global_tot,
                          stack_tb.sentiment.subjectivity,
                          math.log(1+alpha*fav_freq)/math.log(1+alpha)]

        })

    return ([dataframe1, dataframe2])
