import pandas as pd
import datetime as dt
import twint
import nest_asyncio
import unittest
import leia
import nltk.sentiment.vader as vader

nest_asyncio.apply()


class Tweets:
    '''
    Class responsible for aquirering, processing and given sentiments to tweets, given a username.
    Objects:
        userName: given by user
        sinceTime: time to start getting tweets (default to 1 year ago from today)
        tweetDf: stores the dataframe returned by twint
        tweetSentiment: stores the tweets and the dates of the tweets as well as each tweet sentiment given by LeIA ou Vader
    '''

    def __init__(self, userName, sinceTime = str((dt.datetime.now() - dt.timedelta(days=365)).date())):
        
        self.userName = userName
        self.sinceTime = sinceTime

    def aquireTweets(self):
        
        c = twint.Config()
        c.Username = self.userName
        c.Since = self.sinceTime
        c.Pandas = True
        c.Hide_output = True
        twint.run.Search(c)
        
        self.tweetDf = twint.storage.panda.Tweets_df
        
        assert self.tweetDf.empty == False, "Did not get any tweets. Please check if the username you typed exists and has an open account"
    
    def getSentiment(self, lang = 'pt'):
        
        self.tweetSentiment = self.tweetDf[['date', 'timezone', 'tweet']]
        if lang == 'pt':
            s = leia.SentimentIntensityAnalyzer()
            self.tweetSentiment['textPolarity'] = self.tweetSentiment.tweet.apply(lambda frase: s.polarity_scores(frase)['compound'])
        elif lang == 'en':
            a = vader.SentimentIntensityAnalyzer()
            self.tweetSentiment['textPolarity'] = self.tweetSentiment.tweet.apply(lambda frase: a.polarity_scores(frase)['compound'])
        else:
            raise Exception('Please type \'pt\' for Portuguese or \'en\' for English')


## CREATE FUNCTION TO SET TIME TO YY-m-d
   


