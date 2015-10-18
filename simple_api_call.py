from clarifai.client import ClarifaiApi
import os

os.environ["CLARIFAI_APP_ID"]="QazpKOnoaYgNshSDVw4mGGENejQiVWTvWxJMxpyn"
os.environ["CLARIFAI_APP_SECRET"]="8Lin5aSiWpTj201phfBlN5-Bg0lu7reJQFLHn5Zh"
clarifai_api = ClarifaiApi() # assumes environment variables are set.
result = clarifai_api.tag_image_urls('http://www.clarifai.com/img/metro-north.jpg')
print(result)

