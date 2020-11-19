import unittest
from TweetStockCorrelation import Tweets
from TweetStockCorrelation import Stocks
import datetime as dt
import pandas.api.types as ptypes

class testTweetClass(unittest.TestCase):
    
    def testNameDate(self):
        name = 'realDonaldTrump'
        date = '2020-04-04'
        lang = 'pt'
        test = Tweets(userName = name, sinceTime = date)
        
        self.assertEqual(test.userName, name)
        self.assertEqual(test.sinceTime, date)
        self.assertEqual(test.lang, lang)

    def testAquireTweets(self):
        date = '2020-11-04'
        test = Tweets(userName = 'realDonaldTrump', sinceTime = date)
        test.aquireTweets()
        self.assertFalse(test.tweetDf.empty)

        # This is a failiure test, so it should pop an asserion error (because username 'test' does not exist)
        with self.assertRaises(AssertionError):
            test2 = Tweets(userName = 'test', sinceTime = date)
            test2.aquireTweets()


        # This is a failiure test, so it should pop an asserion error (because username 'jmsimoni' has a closed account)
        with self.assertRaises(AssertionError):
            test3 = Tweets(userName = 'jmsimoni', sinceTime = date)
            test3.aquireTweets()

    def testSentiment(self):
        date = '2020-11-04'
        test = Tweets(userName='Sxebiel', sinceTime = date, lang='pt')
        test.aquireTweets()
        test.getSentiment()
        self.assertFalse(test.tweetSentiment.empty)

        test2 = Tweets(userName = 'Sxebiel', sinceTime = date, lang='en')
        test2.aquireTweets()
        test2.getSentiment()
        self.assertFalse(test2.tweetSentiment.empty)

        # This is a failiure test, so it should pop an exeption (because 'es' is not a supported language)
        with self.assertRaises(Exception):
            test3 = Tweets(userName = 'Sxebiel', sinceTime = date, lang='es')
            test3.aquireTweets()
            test3.getSentiment()
    
    def testDateTimeCleanup(self):
            
        date = '2020-11-04'
        test = Tweets(userName='Sxebiel', sinceTime = date, lang='pt')
        test.aquireTweets()
        test.getSentiment()
        test.cleanDateTime()
        self.assertTrue(ptypes.is_datetime64_any_dtype(test.tweetSentiment.date))

    def testTweetSentimentDF(self):

        date = '2020-11-04'
        test = Tweets(userName='Sxebiel', sinceTime = date, lang='pt')
        test.aquireTweets()
        test.getSentiment()
        test.compileSentiment()
        self.assertEqual(len(test.tweetSentiment.columns), 1)
        self.assertEqual(len(test.tweetSentiment), 9)

class testStockClass(unittest.TestCase):
    
    def testInit(self):
        ticker = '^BVSP'
        startDate = '2020-04-04'
        endDate = str(dt.datetime.now().date())
        test = Stocks(ticker=ticker, dateSince=startDate)
        self.assertEqual(test.startDate, startDate)
        self.assertEqual(test.ticker, ticker)
        self.assertEqual(test.endDate, endDate)

    def testgetPrices(self):
        ticker = '^BVSP'
        startDate = '2020-04-04'
        test = Stocks(ticker=ticker, dateSince=startDate)
        test.getPrices()
        self.assertFalse(test.prices.empty)
        self.assertEqual(len(test.prices.columns), 6)