import tweepy
import sys
import json
from tweepy.parsers import JSONParser
from pprint import pprint


consumer_key = "9OT94a5luVczCAghfq4v2gLFp"
consumer_secret = "oR7zYIgDmRmiCz5Lz4uwElbcmFQD4MciFtSesu4Tm69n35tqag"
access_token = "325100141-YmUeuptbDm4Xk65o2ePAEWs1p8NNEtUnfqvqS0vt"
access_token_secret = "fEb30xYgF4g6qDKVXZLoStnqgtoASDv7dqbDX92LMwI7z"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=JSONParser())

#api.send_direct_message("A_K_aries", "hi, test")
#api.verify_credentials()
#api.create_favorite(655686047829880834)
#statuses = tweepy.Cursor(api.home_timeline).items(20)
#statuses = tweepy.Cursor(api.search("hi")).items(20)
#data = [s.text.encode('utf8') for s in statuses]
#print (data)


#with open(api.search(q="#bader") as data_file:    
#    data = json.load(data_file)
#pprint(data)
#open (api.search(q="#good"))


#x = api.search(q="#good")['statuses'].pop()['text']
#print  (dir(x))
#print (x)

x = api.search(q="#ducks", rpp = 2)['statuses']
for d in x:
	try:
		print (d['entities']['media'][0]['media_url_https'])
	except:
		trash = True
	print ('')
