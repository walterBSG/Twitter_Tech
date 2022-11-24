# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 13:18:39 2022

@author: walter.b.gomes
"""

import tweetClass
import config
import tweepy
import re
from collections import Counter
import datetime

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

def eval(classifications):
    classifications = Counter(classifications)
    return classifications['Positive'], classifications['Negative']


res, hashtags, users, tweets = evalContext('covid', 10)
pos, neg = eval(res)
print (pos, neg)
hashtags = countElements(hashtags)
ython pusers = countElements(users)


































