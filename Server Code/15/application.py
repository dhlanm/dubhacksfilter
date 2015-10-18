import logging
import logging.handlers

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

welcomeBefore = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<body>
<h1>It works!</h1>
"""
text = """"""
welcomeAfter = """
</body>
</html>
"""
#from main import rank_images

def printStuff(stuff):
    global text
    text += stuff


from main import rank_images
from clarifai.client import ClarifaiApi
import os, json

os.environ["CLARIFAI_APP_ID"]="f_LGpdh9gta77vih9bOl-96qNU4Nbn5_x6j412N_"
os.environ["CLARIFAI_APP_SECRET"]="_daBl2t7eC9nAGb-IBOdYLfm1uqoCQH6MPlvAJR1"

def get_words_url(url):
    clarifai_api = ClarifaiApi() # assumes environment variables are set.
    result = clarifai_api.tag_image_urls(url)
    #print(result)

    tags=result['results'][0]['result']['tag']['classes']
    probs=result['results'][0]['result']['tag']['probs']
    d={}
    for i in range(len(tags)):
        d[tags[i]]=probs[i]
    return d
def rank_images(images, blockedWords):
    print(blockedWords)
    badfile=open('bad_images.txt', 'a')
    goodfile=open('good_images.txt', 'a')
    imageObjects = []
    for image in images:
        tempObject = imageObject(image)
        imageObjects.append(tempObject)
    i=0
    for iO in imageObjects:
        print(i, end='')
        i+=1
        words = get_words_url(iO.get_path())
        for word in words:
            printStuff(word)
            if word in blockedWords:
                #print("IMAGE CONTAINS EVIL WORD :O", word)
                print(iO.get_path, file=badfile)
                break
                # Subtracts the image weight from the score
                # image.score -= words[word]
        else:
            print(iO.get_path, file=goodfile)
    rankedImages = sorted(imageObject, key=imageObject.get)
    print (rankedImages)
##from main import rank_images

from cgi import parse_qs, escape
from hashtag_search import hashtag_search

def application(environ, start_response):
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            if path == '/':
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size).decode()
                logger.info("Received message: %s" % request_body)

                #split request_body to hashtag, banned words
                data = parse_qs(request_body)
                info = data.get(" name")
                showBanned = info[0][info[0].find("\"show_blocked\"") + 15:info[0].find("-----------------------------")] 
                hashtag = info[1][info[1].find("\"input_hashtag\"") + 16:info[1].find("-----------------------------")] 
                bannedWords = info[2][info[2].find("\"blocked_text\"")  + 15 :info[2].find("-----------------------------")]
                printStuff("showBanned:" + showBanned + "<br />")
                printStuff("Hashtag:" + hashtag + "<br />")
                printStuff("bannedWords:" + bannedWords + "<br />")
                printStuff("End")
                #call twitter api code to get a list of images for the hashtag
                urls = hashtag_search(hashtag)
                printStuff(str(urls))
                #call rank_images(list of hashtag images, banned words)
                rank_images(["https://pbs.twimg.com/media/CRjx-wjUcAAQsDL.jpg"],[request_body]) 
            elif path == '/scheduled':
                logger.info("Received task %s scheduled at %s", environ['HTTP_X_AWS_SQSD_TASKNAME'], environ['HTTP_X_AWS_SQSD_SCHEDULED_AT'])
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        response = welcomeBefore + text + welcomeAfter
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()
