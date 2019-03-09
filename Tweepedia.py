#Essentially, this bot will take the content of a tweet it is mentioned and check against Wikipedia and
# returns snippet of the article with link to continue reading.
import tweepy
import requests
import urllib.parse
import time
#concumer ID's -When you create an app with developers account, you will be issued these
CONSUMER_KEY ='consumer key goes here'
CONSUMER_SECRET ='consumer secret goes here'
ACCESS_KEY ='access key goes here'
ACCESS_SECRET = 'access secret goes here'

#set up fpr authentication with tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#create a file that stores the tweet ID, to avoid responding to the same tweet multiple times
FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def tweepedia():


    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    #reading the mentions and responding
    mentions = api.mentions_timeline(
            	last_seen_id,
            	tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        article = mention
        link = 'https://en.wikipedia.org/api/rest_v1/page/summary/'
        web = 'https://en.wikipedia.org/wiki/'
        url = link + article + '?redirect=true'
        website = web + article
        json_data = requests.get(url).json()
        json_extract = json_data['extract']
        data= json_extract
        data = data[:240]
        api.update_status('@' + mention.user.screen_name +
            data + '...' + website, mention.id)

while True:
    tweepedia()
time.sleep(15)
