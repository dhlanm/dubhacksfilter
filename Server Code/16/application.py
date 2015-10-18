import cgi
import hashtag_search
import json
import logging
import logging.handlers
import os

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

class ImageObject:  
    def __init__(self, imagePath):
        self.path = imagePath
        self.score = 0
    def get_path(self):
        return self.path

def get_words_url(url):
    clarifai_api = ClarifaiApi() # assumes environment variables are set.
    result = clarifai_api.tag_image_urls(url)

    tags=result['results'][0]['result']['tag']['classes']
    probs=result['results'][0]['result']['tag']['probs']
    return { tags[i] : probs[i] for i in range(len(tags)) }

def rank_images(images, blockedWords):
    blockedWords = [ word.strip() for word in blockedWords ]
    imageObjects = [ ImageObject(image) for image in images ]
    
    worddict = {
        'good': [],
        'bad': []
    }
    for iO in imageObjects:
        words = get_words_url(iO.get_path())
        for word in words:
            if word in blockedWords:
                worddict["bad"].append(iO.get_path())
                break
        else:
            worddict["good"].append(iO.get_path())
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
            
            urls = hashtag_search.hashtag_search(hashtag)
            bannedWords = info[2][
                info[2].find("\"blocked_text\"")  + 15 : info[2].find("-----------------------------")
            ].split(',')
            
            
            headers.append(('Content-type', 'application/json'))
            response = json.dumps({
                'urls': urls,
                'bannedWords': bannedWords,
                'ranked': rank_images(urls, bannedWords)
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
            print('=============open', path[1:])
            with open(path[1:], 'r') as f:
                response = f.read()
        else:
            status = '404 Not Found'
            response = '{} not found'.format(path)
    print('=========================================', status, headers, response)
    start_response(status, headers)
    return [response.encode('utf-8')]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()
