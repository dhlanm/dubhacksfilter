from clarifai.client import ClarifaiApi
import os, json

os.environ["CLARIFAI_APP_ID"]="QazpKOnoaYgNshSDVw4mGGENejQiVWTvWxJMxpyn"
os.environ["CLARIFAI_APP_SECRET"]="8Lin5aSiWpTj201phfBlN5-Bg0lu7reJQFLHn5Zh"

def get_words(url):
    clarifai_api = ClarifaiApi() # assumes environment variables are set.
    result = clarifai_api.tag_image_urls(url)
    #print(result)

    tags=result['results'][0]['result']['tag']['classes']
    probs=result['results'][0]['result']['tag']['probs']
    d={}
    for i in range(len(tags)):
        d[tags[i]]=probs[i]
    return d

