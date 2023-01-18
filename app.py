
"""
Ce programme est le programme principal du projet,
il execute l'application dash et fait appel aux différents autres packages
"""

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from twitter_collect import fetch_tweets
from twitter_analyse import emotions_fct
from twitter_analyse import word_cloud
from twitter_analyse import fetch_words
from twitter_analyse import mosaic
#import pandas as pd
import dash_daq as daq

external_stylesheets = ['assets/style.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Structure de la page
app.layout = html.Div([

    # Header
    html.Div([
        html.Div([
            html.Img(className='app-header--logo', src=app.get_asset_url(
                'logo-blanc.svg')),
            html.H1("Centrale Analytica", style={'textAlign': 'center'}),
        ], className='box head1'),

        # Searchbox
        html.Div([dcc.RadioItems(id='research-type', options=[
            {'label': 'Subject', 'value': 'subject'},
            {'label': 'Hashtag', 'value': 'hashtag'},
            {'label': 'User', 'value': 'user'},
        ], inline=True, style={'margin': '10px'}, value='subject'),
            dcc.Input(id='input-text', type='text',
                      value='Type here', className='input'),
            html.Button(id='submit-button-text', n_clicks=0,
                        children='Submit', style={'backgroundColor': '#1A8CD8', 'margin': '10px'}),
            html.Div(id='wainting-text'),
            html.Div(id='ending-text'),
            dcc.Checklist(
                ['Feelings Proportions', 'Wordcloud', 'Mosaic', 'Gauge'],
                id='dropdown-to-show-or-hide-element',
                inline=True, value=[],
                className="checkbox"
        )], className='box head2'),


    ], className='app-header', style={'background-image': 'url(assets/banniere2.jpg)',
                                      'background-size': 'cover'}),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='barchart_feelings')],
                     className='box graph', id='barchart_box'),
            html.Div([dcc.Graph(id='wordcloud', className='image1')],
                     className='box graph', id='wordcloud_box')], className='top flex'),
        html.Div([
            html.Div([dcc.Graph(id='mosaic', className='image2')],
                     className='box graph', id='mosaic_box'),
            html.Div([daq.Gauge(
                id='my-gauge-1',
                label="Negative-Positive",
                color={"gradient": True, "ranges": {
                    "red": [0, 0.35], "yellow":[0.35, 0.7], "green":[0.7, 1]}},
                value=0.5,
                min=0,
                max=1,
                size=120
            ),
                daq.Gauge(
                id='my-gauge-2',
                label="Objective-Subjective",
                color={"gradient": True, "ranges": {
                    "blue": [0, 0.5], "red":[0.5, 1]}},
                value=0.5,
                min=0,
                max=1,
                size=120
            ),
                daq.Gauge(
                id='my-gauge-3',
                label="Unknown-Famous",
                color={"gradient": True, "ranges": {
                    "purple": [0, 0.5], "orange":[0.5, 1]}},
                value=0.5,
                min=0,
                max=1,
                size=120
            )], className='box graph', id='gauge_box')], className='bottom flex')
    ])
], className='page')


# Appelé lors de l'appui du boutton, affiche la phrase d'attente
@ app.callback(Output('wainting-text', 'children'),
               Input('submit-button-text', 'n_clicks'),
               State('input-text', 'value'))
def start_analyse(n_clicks, request):
    """Affiche la phrase d'attente lorsque l'analyse est lancée

    Args:
        n_clicks (integer): nombre de fois que le bouton a été appuyé
        input (string): texte entré par l'utilisateur

    Raises:
        PreventUpdate: si le bouton n'a pas été appué ie au chargement de la page

    Returns:
        strin: texte à afficher
    """
    if n_clicks == 0:
        raise PreventUpdate

    return f'''Your request about "{request}" is being treated'''


@ app.callback(Output('barchart_feelings', 'figure'),
               Output('wordcloud', 'figure'),
               Output('mosaic', 'figure'),
               Output('my-gauge-1', 'value'),
               Output('my-gauge-2', 'value'),
               Output('my-gauge-3', 'value'),
               Output('ending-text', 'children'),
               Input('submit-button-text', 'n_clicks'),
               Input('research-type', 'value'),
               State('input-text', 'value'))
def analyse(n_clicks, rtype, request):
    """Analyse les tweets et crée plusieurs représentations

    Args:
        n_clicks (integer): nombre de fois que le bouton a été appuyé
        type (string): type de la recherche (subject/hashtag/user)
        request (string): texte entré par l'utilisateur

    Raises:
        PreventUpdate: si le bouton n'a pas été appué ie au chargement de la page

    Returns:
        figure: barchart associé au sentiment détéctés par l'analyse
    """

    if n_clicks == 0:
        raise PreventUpdate

    # Récuperation des données
    sub, hashtag, use = False, False, False
    if rtype == 'subject':
        sub = True
    elif rtype == 'hashtag':
        hashtag = True
    else:
        use = True
    fetch_tweets.create_data(request, subject=sub,
                             user=use, hashtag=hashtag, tweet_limit=100)
    dataframe = fetch_tweets.get_data("twitter_data.json")

    # analyse des données
    datas = emotions_fct.emo_analysis(dataframe)
    # création du wordcloud

    feeling = str(datas[0]["Emotion"].iloc[datas[0]["Frequency"].idxmax()])
    print(feeling)
    wordcloud = word_cloud.generate_wordcloud(dataframe, feeling=feeling, contour_width=1,
                                              coutor_color='blue', background_color='black')
    fig2 = px.imshow(wordcloud)
    fig2.update_layout(template=None, paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
    fig2.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig2.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    # création de la mosaïque
    mots = fetch_words.frequent_words(dataframe, 12)
    mosaic_image = mosaic.fetch_image(mots, request)
    fig3 = px.imshow(mosaic_image)
    fig3.update_layout(template=None, paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
    fig3.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig3.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    # Création du barchart
    fig = px.bar(datas[0], x='Emotion', y='Frequency', text_auto=True,
                 title="Feelings proportions")
    fig.update_traces(textfont_size=14, textangle=0,
                      textposition="inside", cliponaxis=False)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      font_color='white',
                      title_font_color='white')

    freqp, freqs, freqf = datas[1]['Frequency'][0], datas[1]['Frequency'][1], datas[1]['Frequency'][2]
    return fig, fig2, fig3, freqp, freqs, freqf, f'''Your request about "{request}" has been treated'''


@ app.callback(
    Output(component_id='barchart_box', component_property='style'),
    Output(component_id='wordcloud_box', component_property='style'),
    Output(component_id='mosaic_box', component_property='style'),
    Output(component_id='gauge_box', component_property='style'),
    [Input(component_id='dropdown-to-show-or-hide-element', component_property='value')])
def show_hide_element(visibility_state):
    """Change l'état de certains div pour qu'ils soient visibles ou non

    Args:
        visibility_state (list): liste des id dont le state doit être
        changé pour block, les autres doivent être changés pour none

    Returns:
        dict: type de display des quatres fenêtres
    """
    if 'Feelings Proportions' in visibility_state:
        barc = {'display': 'block'}
    else:
        barc = {'display': 'none'}

    if 'Wordcloud' in visibility_state:
        wor = {'display': 'block'}
    else:
        wor = {'display': 'none'}

    if 'Mosaic' in visibility_state:
        mos = {'display': 'block'}
    else:
        mos = {'display': 'none'}

    if 'Gauge' in visibility_state:
        gau = {'display': 'block'}
    else:
        gau = {'display': 'none'}

    return barc, wor, mos, gau


if __name__ == '__main__':
    app.run_server(debug=True)
