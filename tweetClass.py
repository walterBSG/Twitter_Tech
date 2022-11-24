# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 10:05:13 2022

@author: walter.b.gomes
"""

import re
import string
import random
from nltk import NaiveBayesClassifier
from nltk.tag import pos_tag
from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        token = re.sub(r'\b\w{1,3}\b', '', token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens
            
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def getClassifier():
    stop_words = stopwords.words('english')
    
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
    positive_cleaned_tokens_list = [remove_noise(tokens, stop_words) for tokens in positive_tweet_tokens]
    negative_cleaned_tokens_list = [remove_noise(tokens, stop_words) for tokens in negative_tweet_tokens]
    
    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)
    positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
    negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]
    
    dataset = positive_dataset + negative_dataset
    random.shuffle(dataset)
    
    classifier = NaiveBayesClassifier.train(dataset)
    return classifier

def evalTweet(classifier, tweet):
    custom_tokens = remove_noise(word_tokenize(tweet))
    ans = classifier.classify(dict([token, True] for token in custom_tokens))
    return ans
    
def evalTweets(classifier, tweets):
    ans =[]
    tweets_tokens = [remove_noise(word_tokenize(tweet)) for tweet in tweets]
    for tokens in tweets_tokens:
        ans.append(classifier.classify(dict([token, True] for token in tokens)))
    return ans


































