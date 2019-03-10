#Essentially, this bot will take the content of a tweet it is mentioned and check against Wikipedia if a content
#with ssuch topic exists. It then returns snippets of the article if it exists with a link to continue reading if
#you so wish. Does not currently support wrong casing i.e if you write lagos state university instead of Lagos State
#University, you will probably not get any result. Open to collaboration and ideas. I gladly welcome then!
import tweepy
import requests
import urllib.parse
import time
#consumer ID's - When you create an app on twitter, you will be issued these
CONSUMER_KEY ='consumer key goes here'
CONSUMER_SECRET ='consumer secret goes here'
ACCESS_KEY ='access key goes here'
ACCESS_SECRET = 'access secret goes here'

#create a file that stores the tweet ID, to avoid responding to the same tweet multiple times
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

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
        foo = mention.full_text
        bar = str(foo.strip().lstrip("@mahveo_"))
        article = str(bar.strip().lstrip())
        foobar =article.replace(" ", "_")
        link = 'https://en.wikipedia.org/api/rest_v1/page/summary/'
        web = 'https://en.wikipedia.org/wiki/'
        url = link + article + '?redirect=true'
        website = web + foobar
        json_data = requests.get(url).json()
        json_extract = json_data['extract']
        data= json_extract
        data = data[:230]
        api.update_status('@' + mention.user.screen_name + ' ' +
            data+'...'+website, mention.id)

def not_exist():

    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    #reading the mentions and responding
    mentions = api.mentions_timeline(
                last_seen_id,
                tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        mtn = mention.full_text
        article = str(mtn.strip().lstrip("@mahveo_"))
        api.update_status('@' + mention.user.screen_name + ' ' +
            'Unfortunately, Wikipedia does not have an article about the subject right now')
        print('article does not exist')


while True:
    try:
        tweepedia()
        time.sleep(15)
    except:
        not_exist()
        time.sleep(30)

