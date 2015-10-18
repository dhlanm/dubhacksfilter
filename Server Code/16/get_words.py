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

#doesn't work :'(
def get_words_here(path):
    clarifai_api = ClarifaiApi() # assumes environment variables are set.
    result = clarifai_api.tag_images(open(path))
    #print(result)

    tags=result['results'][0]['result']['tag']['classes']
    probs=result['results'][0]['result']['tag']['probs']
    d={}
    for i in range(len(tags)):
        d[tags[i]]=probs[i]
    return d

