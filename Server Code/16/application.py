import cgi
import collections
import json
import logging
import logging.handlers
import os
import tweepy
from tweepy.parsers import JSONParser

os.environ["CLARIFAI_APP_ID"] = "f_LGpdh9gta77vih9bOl-96qNU4Nbn5_x6j412N_"
os.environ["CLARIFAI_APP_SECRET"] = "_daBl2t7eC9nAGb-IBOdYLfm1uqoCQH6MPlvAJR1"

from clarifai.client import ClarifaiApi
from wsgiref.simple_server import make_server


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/opt/python/log/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

Tweet = collections.namedtuple('Tweet', ['media', 'text', 'username'])

def hashtag_search(hashtag):
    consumer_key = "9OT94a5luVczCAghfq4v2gLFp"
    consumer_secret = "oR7zYIgDmRmiCz5Lz4uwElbcmFQD4MciFtSesu4Tm69n35tqag"
    access_token = "325100141-YmUeuptbDm4Xk65o2ePAEWs1p8NNEtUnfqvqS0vt"
    access_token_secret = "fEb30xYgF4g6qDKVXZLoStnqgtoASDv7dqbDX92LMwI7z"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, parser=JSONParser())

    x = api.search(q=hashtag, rpp=20)['statuses']
    tweets = []
    for d in x:
        if 'entities' in d and 'media' in d['entities']:
            tweets.append(Tweet(d['entities']['media'][0]['media_url_https'], d['text'], d['user']['screen_name']))
    return tweets


def get_words_url(url):
    clarifai_api = ClarifaiApi() # assumes environment variables are set.
    result = clarifai_api.tag_image_urls(url)

    tags=result['results'][0]['result']['tag']['classes']
    probs=result['results'][0]['result']['tag']['probs']
    return { tags[i] : probs[i] for i in range(len(tags)) }
    
class ImageObject:  
    def __init__(self, tweet):
        self.tweet = tweet
        self.tags = get_words_url(tweet.media)
        
    def to_dict(self):
        return {
            'path': self.tweet.media,
            'username': self.tweet.username,
            'text': self.tweet.text,
            'tags': self.tags
        }

def rank_images(tweets, blockedWords):
    logging.info('Ranking images')
    blockedWords = [ word.strip() for word in blockedWords ]
    imageObjects = [ ImageObject(tweet) for tweet in tweets ]
    
    worddict = {
        'good': [],
        'bad': []
    }
    for i, img in enumerate(imageObjects):
        logging.info('Ranking {}/{}'.format(i, len(imageObjects)))
        for w in img.tags:
            if w in blockedWords:
                worddict['bad'].append(img.to_dict())
                break
        else:
            worddict['good'].append(img.to_dict())
    return worddict

status_data = {
    'processing': False,
    'finished': False
}
def application(environ, start_response):
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']

    status = '200 OK'
    response = ''
    headers = []
    
    logging.info('Request {}: {}'.format(method, path))
    if method == 'POST':
        if path == '/':
            status_data['processing'] = True
            status_data['finished'] = False
            request_body_size = int(environ['CONTENT_LENGTH'])

            request_body = environ['wsgi.input'].read(request_body_size).decode()
            logger.info("Received message: %s" % request_body)

            #split request_body to hashtag, banned words
            data = cgi.parse_qs(request_body)
            info = data.get(" name")
            hashtag = info[1][
                info[1].find("\"input_hashtag\"") + 16 : info[1].find("-----------------------------")
            ] 
            
            logging.info('Seaching twitter')
            tweets = hashtag_search(hashtag)
            logging.info('Got {} tweets'.format(len(tweets)))
            bannedWords = info[2][
                info[2].find("\"blocked_text\"")  + 15 : info[2].find("-----------------------------")
            ].split(',')
            
            
            headers.append(('Content-type', 'application/json'))
            response = json.dumps({
                'tweets': tweets,
                'bannedWords': bannedWords,
                'ranked': rank_images(tweets, bannedWords)
            })
            
            status_data['processing'] = False
            status_data['finished'] = True
        elif path == '/scheduled':
            logger.info("Received task %s scheduled at %s", environ['HTTP_X_AWS_SQSD_TASKNAME'], environ['HTTP_X_AWS_SQSD_SCHEDULED_AT'])
    elif method == 'GET':
        if path in ['/', '/main.html', '/main.css', '/request_handler.js']:
            if path == '/':
                path = '/main.html'
            headers.append(('Content-type', 'text/html'))
            with open(path[1:], 'r') as f:
                response = f.read()
        else:
            status = '404 Not Found'
            response = '{} not found'.format(path)
    start_response(status, headers)
    return [response.encode('utf-8')]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()
