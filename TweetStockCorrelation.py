import pandas as pd
import datetime as dt
import twint
import nest_asyncio
nest_asyncio.apply()


class Tweets:
    '''
    Class responsible for aquirering and processing tweets, given a username.
    Objects:
        userName: given by user
        sinceTime: time to start getting tweets (default to 1 year ago from today)
        tweetDf: stores the dataframe returned by twint
        tweetAndDates: stores only the tweets and the dates of the tweets
    '''

    def __init__(self, username, sinceTime = dt.datetime.now() - dt.timedelta(days=365)):
        self.userName = username
        self.sinceTime = sinceTime
        self.aquireTweets()
        self.storeTweetAndDates()
    
    def aquireTweets(self):
        c = twint.Config()
        c.Username = self.userName
        c.Since = str(self.sinceTime.date())
        c.Pandas = True
        c.Hide_output = True
        twint.run.Search(c)
        self.tweetDf = twint.storage.panda.Tweets_df
    
    def storeTweetAndDates(self):
        self.tweetAndDates = self.tweetDf[['date', 'tweet', 'timezone']]
