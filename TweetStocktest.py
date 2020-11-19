import unittest
from TweetStockCorrelation import Tweets

class testTweetClass(unittest.TestCase):
    
    def testNameDate(self):
        name = 'realDonaldTrump'
        date = '2020-04-04'
        test = Tweets(userName = name, sinceTime = date)
        
        self.assertEqual(test.userName, name)
        self.assertEqual(test.sinceTime, date)


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
        test = Tweets(userName='Sxebiel', sinceTime='2020-10-01')
        test.aquireTweets()
        test.getSentiment()
        self.assertFalse(test.tweetSentiment.empty)
