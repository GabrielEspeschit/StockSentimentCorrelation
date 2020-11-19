import pandas as pd
import datetime as dt
import twint
import nest_asyncio
import unittest
import leia
import nltk.sentiment.vader as vader
import pandas_datareader as data
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
nest_asyncio.apply()

## CREATE FUNCTION TO SET TIME TO YY-m-d
## Implement Global timezone diferences

class Tweets:
    '''
    Class responsible for aquirering, processing and given sentiments to tweets, given a username.
    Objects:
        userName (given): given by user
        sinceTime (given): time to start getting tweets (default to 1 year ago from today)
        lang (given): language to analise tweets in
        tweetDf: stores the dataframe returned by twint
        tweetSentiment: stores the tweets and the dates of the tweets as well as each tweet sentiment compound score
    Methods:
        __init__: initializes class
        aquireTweets: aquires tweets using twint
        getSentiment: gets sentiment using LeIA or Vader (depending on the language)
        cleanDateTime: cleans datetime and transforms it into usable dtype
        compileSentiment: compile the mean daily sentiment

    '''

    def __init__(self, userName, sinceTime = str((dt.datetime.now() - dt.timedelta(days=365)).date()), lang = 'pt'):
        
        self.userName = userName
        self.sinceTime = sinceTime
        self.lang = lang

    def aquireTweets(self):
        
        c = twint.Config()
        c.Username = self.userName
        c.Since = self.sinceTime
        c.Pandas = True
        c.Hide_output = True
        twint.run.Search(c)
        
        self.tweetDf = twint.storage.panda.Tweets_df
        
        assert self.tweetDf.empty == False, "Did not get any tweets. Please check if the username you typed exists and has an open account or if there are any tweets for the timeframe selected."
    
    def getSentiment(self):
        
        self.tweetSentiment = self.tweetDf[['date', 'tweet']]
        if self.lang == 'pt':
            s = leia.SentimentIntensityAnalyzer()
            self.tweetSentiment['textPolarity'] = self.tweetSentiment.tweet.apply(lambda frase: s.polarity_scores(frase)['compound'])
        elif self.lang == 'en':
            a = vader.SentimentIntensityAnalyzer()
            self.tweetSentiment['textPolarity'] = self.tweetSentiment.tweet.apply(lambda frase: a.polarity_scores(frase)['compound'])
        else:
            raise Exception('Please type \'pt\' for Portuguese or \'en\' for English')

        del self.tweetSentiment['tweet']

    def cleanDateTime(self):
        self.tweetSentiment['date'] = pd.to_datetime(self.tweetSentiment['date'])
        self.tweetSentiment['onlyDate'] = [d.date() for d in self.tweetSentiment.date]
        self.tweetSentiment['onlyTime'] = [d.time() for d in self.tweetSentiment.date]

    def compileSentiment(self):
        self.cleanDateTime()
        self.tweetSentiment = self.tweetSentiment.groupby(['onlyDate']).mean()


class Stocks():
    def __init__(self, ticker, startDate = str((dt.datetime.now() - dt.timedelta(days=365)).date())):
        self.ticker = ticker
        self.endDate = str(dt.datetime.now().date())
        self.startDate = startDate
        
    def getPrices(self):    
        self.prices = data.DataReader(self.ticker, 'yahoo', self.startDate, self.endDate)

    def getDailyVar(self):
        self.prices['var'] = (self.prices.Close - self.prices.Close.shift(1))/(self.prices.Close.shift(1))*100


class TweetAndStockData():

    def __init__(self, ticker, username, startDate = str((dt.datetime.now() - dt.timedelta(days=365)).date()), lang = 'pt'):
        
        self.username = username
        self.ticker = ticker
        
        tweets = Tweets(userName=username, sinceTime=startDate, lang=lang)
        tweets.aquireTweets()
        tweets.getSentiment()
        tweets.compileSentiment()
        self.tweetStockData = tweets.tweetSentiment

        stocks = Stocks(ticker=ticker, startDate=startDate)
        stocks.getPrices()
        stocks.getDailyVar()
        self.tweetStockData['change'] = stocks.prices['var']
        self.tweetStockData.dropna(inplace=True)
        self.tweetStockData['varNorm'] = (stocks.prices['var']-stocks.prices['var'].min())/(stocks.prices['var'].max()-stocks.prices['var'].min())
        self.tweetStockData['polNorm'] = (tweets.tweetSentiment['textPolarity']-tweets.tweetSentiment['textPolarity'].min())/(tweets.tweetSentiment['textPolarity'].max()-tweets.tweetSentiment['textPolarity'].min())
        

    def avaragingNaN(self):
        pass
    
    def plotCorrelation(self, pearson = True):
        if pearson:
            data1 = self.tweetStockData.change.to_numpy()
            data2 = self.tweetStockData.textPolarity.to_numpy()
            corr, _ = pearsonr(data1, data2)
            print('Pearsons correlation: %.3f' % corr)
            cor = self.tweetStockData.change.rolling(3).corr(self.tweetStockData.textPolarity)
            plt.plot(cor)
            plt.show()


        
        else:
            plt.plot(self.tweetStockData[['varNorm', 'polNorm']])
            plt.title('Variação do Índice Ibovespa e sentimento do twitter analisadas (valores normalizados)', fontsize = 16)
            plt.xlabel('Dia', fontsize=12)
            plt.ylabel('Valor', fontsize=12)
            plt.legend(['Variação do Ibovespa', f'Sentimento do twitter do @{self.username}'], loc='lower right')
            plt.show()

        


if __name__ == '__main__':
    ticker = '^BVSP'
    username = 'folha'
    lang = 'pt'
    startDate = '2020-10-01'
    test = TweetAndStockData(ticker=ticker, username=username, startDate= startDate, lang=lang)
    test.plotCorrelation(pearson=True)