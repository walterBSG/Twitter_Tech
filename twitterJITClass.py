# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 13:18:39 2022

@author: walter.b.gomes
"""

import re
import config
import tweepy
import datetime
import community
import itertools
import tweetClass
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from pyvis.network import Network
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, STOPWORDS

def countElements(elements):
    elements = Counter(elements)
    elements = [(k, elements[k]) for k in sorted(elements, key=elements.get, reverse=True)]
    return elements

def getHashtag(tweets):
    hashtags = []
    r = re.compile('#\w+')
    for tweet in tweets:
        print(tweet)
        hashtags = hashtags + list(filter(r.match, tweet))
    return hashtags

def getUsers(tweets, exception = ''):
    users = []
    r = re.compile('@\w+')
    for tweet in tweets:
        users = users + list(filter(r.match, tweet))
    users = [user for user in users if user != exception]
    return users

def getElements(tweets, exception = ''):
    users = hashtags = []
    hashreg = re.compile('#\w+')
    userreg = re.compile('@\w+')
    for tweet in tweets:
        users = users + userreg.findall(tweet)
        hashtags = hashtags + hashreg.findall(tweet)
    users = [user for user in users if user != exception]
    return hashtags, users

def getTweets(word, amount):
    query = word + ' lang:en -is:retweet'
    
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
    response = []
    for i in range(amount):
        date = datetime.datetime.now() - datetime.timedelta(hours = i)
        temp_res = client.search_recent_tweets(query=query, max_results=100, start_time = date)
        response = response + [tweet.text for tweet in temp_res.data]
    return response

def evalAccount(name, amount = 1):
    classifier = tweetClass.getClassifier()

    tweets = getTweets(name, amount)
    
    res = tweetClass.evalTweets(classifier, tweets)
    hashtags, users = getElements(tweets, name)
    return res, hashtags, users, tweets

def evalContext(element, amount = 1):
    classifier = tweetClass.getClassifier()
    tweets = getTweets(element, amount)
    
    res = tweetClass.evalTweets(classifier, tweets)
    hashtags, users = getElements(tweets)
    return res, hashtags, users, tweets

def createGraph(data):
    data = dict(Counter(data))
    data = [[key[0], key[1], data[key]] for key in data.keys()]
    df = pd.DataFrame(data, columns = ['R1', 'R2', 'value'])
    g = nx.from_pandas_edgelist(df, source='R1', target='R2', edge_attr='value', edge_key=None, create_using = nx.Graph())
    plt.figure(figsize=(10,10))
    net = Network(notebook = True, width="1500px", height="1200px", bgcolor='#222222', font_color='white')
    net.repulsion()
    node_degree = dict(g.degree)
    com = community.best_partition(g)
    nx.set_node_attributes(g, node_degree, 'size')
    nx.set_node_attributes(g, com, 'group')
    net.from_nx(g)
    net.show("img/tweet_graph.html")
    return df

def grafEval(tweets):
    classifier = tweetClass.getClassifier()
    data = []
    for tweet in tweets:
        hashtags, users = getElements([tweet])
        res = tweetClass.evalTweets(classifier, [tweet])
        data += list(itertools.combinations(dict.fromkeys(hashtags + users + res), 2))
    df = createGraph(data)
    return df

def eval(classifications):
    classifications = Counter(classifications)
    return classifications['Positive'], classifications['Negative']

def plotCloud(text):
    wordcloud = WordCloud(width= 3000, height = 2000, random_state=1, background_color='black', colormap='Dark2', collocations=False, stopwords = STOPWORDS).generate(text)
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    wordcloud.to_file("img/wordcloud.png")

def makeWordCloud(text):
    custom_tokens = tweetClass.remove_noise(word_tokenize(text))
    plotCloud(' '.join(custom_tokens))
    
def createBarGraph(positive, negative):
    fig, ax = plt.subplots()

    types = ['Positive', 'Negative']
    counts = [positive, negative]
    bar_colors = ['tab:blue', 'tab:red']
    
    ax.bar(types, counts, color=bar_colors)
    fig.set_dpi(300)
    ax.set_ylabel('Number of twwets')
    ax.set_title('Positive and Negative Tweets by color')
    plt.savefig('img/tweetBar.png')

def main():
    cont = input("What's your search? ")
    count = input("How many searchs? ")
    res, hashtags, users, tweets = evalContext(cont, int(count))
    pos, neg = eval(res)
    createBarGraph(pos, neg)
    grafEval(tweets)
    makeWordCloud(' '.join(tweets))
    
if __name__ == '__main__':
    main()

































