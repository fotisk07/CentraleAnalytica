# <div align="center">  <img src="/Pictures_README/logo.svg" alt="isolated" width="100"/> </div> <div align="center"> CentraleAnalytica </div>

## Description

<div align="left">The purpose of our tool is to analyze emotions from a large number of tweets, in two steps:</div>
<br>

<div align="left">Step1 : The user writes a query in the search bar, which can be a username, hashtag or subject. Our tool then fetches tweets related to the query.</div>
<div align="left">Step2 : Our program analyzes the fetched tweets and submits 4 results/charts :</div>
<br>

-	The first one is a WordCloud made of the words appearing the most frequently in the tweets fetched : the bigger the word is in the WordCloud the more it appeared in the results. The cloud will have the form of an emoji which should represent the main emotion emanating from the tweets.
-	The second one is a column chart representing the percentage of each emotion emanating from the tweets fetched. The higher bar should thus correspond to the emoji of the WorldCloud.
-	 The third one is made of four cursors giving further intel about the tweets : are they more positive or negative ? subjective or objective ? neutrous or famous ? unanimous or polarized ?
-	The fourth and last result displayed by the tool is a mosaic with no particular form made up of pictures which should represent the words frequently used within the tweets fetched.


## Installation

The Code is written in Python 3.9.12 . If you don't have Python installed you can find it [here](https://www.python.org/downloads/). If you are using a lower version of Python you can upgrade using the pip package, ensuring you have the latest version of pip.


You have to install several dependencies to get the project up and running. To do so just type
```
pip install -r requirements.txt
```
This will install all necessery packages

### Requirements

In order to use our tool, you have to have access to a Twitter Developper Account with elevated access. To do so, follow these 3 steps :

- Create a Twitter account
- Log in to the Twitter Developper Portal : https://developer.twitter.com/en
- In the tab "Products" of the Developper Portal, follow the procedure to gain the elevated access.

An exemple of the answers that could be given to the survey is given below : 

<div align="center"> <img src="/Pictures_README/twi3.jpg" alt="isolated" width="700" box-shadow="10px 10px 5px" /> </div>

<br>

You then have to create a file named `credentials.py` in the file "twiter_collect", containing your consumer keys and authentification tokens, that can be found in the tab "Projects & Apps" of the Twitter Developper Portal. It should look like this :

```
CONSUMER_KEY='' 
CONSUMER_SECRET=''
ACCESS_TOKEN=''
ACCESS_SECRET=''
```

### Usage

To launch to the tool, run the following command at the root of the program :

```
python app.py
```
Then click the following [link](http://127.0.0.1:8050/) in your browser in order to have access to our tool.

## Contributing

Please read [CONTRIBUTING](https://gitlab-cw6.centralesupelec.fr/fotios.kapotos/centraleanalytica/-/blob/main/CONTRIBUTING.md) for the process for submitting pull requests.

## L'equipe

* **Fotios Kapotos** - *Initial work*
* **Nicolas Charrondiere** - *Initial work*
* **Mathis RAY** - *Initial work*
* **Paul Nollet** - *Initial work*
* **Salvador Gonzalez** - *Initial work*
* **Andreï Radlovic** - *Initial work*

This project is licensed under the MIT License - see the [LICENSE.md](https://gitlab-cw6.centralesupelec.fr/fotios.kapotos/centraleanalytica/-/blob/main/LICENSE.md) file for details

<div align="right"> <img src="/Pictures_README/cs.png" alt="isolated" width="100"/> </div>
