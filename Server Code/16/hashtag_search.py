import collections
import tweepy
from tweepy.parsers import JSONParser

Tweet = collections.namedtuple('Tweet', ['media', 'text', 'username'])

def hashtag_search(hashtag):
    consumer_key = "9OT94a5luVczCAghfq4v2gLFp"
    consumer_secret = "oR7zYIgDmRmiCz5Lz4uwElbcmFQD4MciFtSesu4Tm69n35tqag"
    access_token = "325100141-YmUeuptbDm4Xk65o2ePAEWs1p8NNEtUnfqvqS0vt"
    access_token_secret = "fEb30xYgF4g6qDKVXZLoStnqgtoASDv7dqbDX92LMwI7z"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, parser=JSONParser())

    x = api.search(q=hashtag)['statuses']
    tweets = []
    for d in x:
        if 'entities' in d and 'media' in d['entities']:
            tweets.append(Tweet(d['entities']['media'][0]['media_url_https'], d['text'], d['user']['screen_name']))
    return tweets

