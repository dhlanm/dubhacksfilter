import tweepy
import sys
import json
from tweepy.parsers import JSONParser
from pprint import pprint

def hastag_search(hashtag)
    consumer_key = "9OT94a5luVczCAghfq4v2gLFp"
    consumer_secret = "oR7zYIgDmRmiCz5Lz4uwElbcmFQD4MciFtSesu4Tm69n35tqag"
    access_token = "325100141-YmUeuptbDm4Xk65o2ePAEWs1p8NNEtUnfqvqS0vt"
    access_token_secret = "fEb30xYgF4g6qDKVXZLoStnqgtoASDv7dqbDX92LMwI7z"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, parser=JSONParser())

    x = api.search(q=hashtag, rpp = 2)['statuses']
    urls=[]
    for d in x:
            try:
                    urls.append((d['entities']['media'][0]['media_url_https']))
            except:
                    trash = True
            print ('')
    return urls
