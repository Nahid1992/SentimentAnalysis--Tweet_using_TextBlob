import tweepy
from textblob import TextBlob
import csv

SEARCH_TOPIC = 'SpaceX'
START_DATE = "2016-10-13"
END_DATE = "2018-02-14"
FETCH_COUNT = 100
DATEFETCH = False

def tweeterAuth():
    consumer_key = "CONSUMER KEY"
    consumer_secret = "CONSUMER SECRET"
    access_token = "ACCESS TOKEN"
    access_token_secret = "ACCESS TOKEN SECRET"

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

def SearchTweetTopic(api,SEARCH_TOPIC,FETCH_COUNT,START_DATE,END_DATE,DATEFETCH):
    if DATEFETCH == True:
        public_tweets = api.search(SEARCH_TOPIC, count=FETCH_COUNT, since = START_DATE, until=END_DATE)
    else:
        public_tweets = api.search(SEARCH_TOPIC, count=FETCH_COUNT)
    return public_tweets

def Print_and_Save(public_tweets):
    num_pos = 0
    num_neg = 0
    num_neu = 0
    ann = []
    tweetList = []

    csvFile = open('tweetSave.csv','w')
    fieldName = ['Serial','Tweet','Label']
    writer = csv.DictWriter(csvFile, fieldnames=fieldName)
    writer.writerow({'Serial':'Serial','Tweet': 'Tweet', 'Label':'Label'})
    count = 0

    for tweet in public_tweets:
        count = count+1
        analysis = TextBlob(tweet.text)
        tweetList.append(tweet.text)
        ann.append(analysis.sentiment)

        resultLabel = analysis.sentiment[0]
        if resultLabel == 0:
            result = 'Neutral'
            num_neu = num_neu+1
        if resultLabel < 0:
            result = 'Negative'
            num_neg = num_neg+1
        if resultLabel > 0:
            result = 'Positive'
            num_pos = num_pos+1

        print('Serial_'+str(count)+': '+tweet.text)
        print('{'+result+'}')
        print('')
        writer.writerow({ 'Serial': count,'Tweet': tweet.text.encode('utf8'), 'Label': result })
    return num_neu,num_neg,num_pos

if __name__== "__main__":

    api = tweeterAuth()
    public_tweets = SearchTweetTopic(api,SEARCH_TOPIC,FETCH_COUNT,START_DATE,END_DATE,DATEFETCH)
    num_neu,num_neg,num_pos = Print_and_Save(public_tweets)
    print('----------------------------')
    print('Neutral = '+str(num_neu))
    print('Negative = '+str(num_neg))
    print('Positive = '+str(num_pos))
    print('----------------------------')

breakPoint=1
