from clarifai_basic import ClarifaiCustomModel
import os
os.environ["CLARIFAI_APP_ID"]="f_LGpdh9gta77vih9bOl-96qNU4Nbn5_x6j412N_"
os.environ["CLARIFAI_APP_SECRET"]="_daBl2t7eC9nAGb-IBOdYLfm1uqoCQH6MPlvAJR1"


concept = ClarifaiCustomModel()

concept.positive('https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/BMW_E90_Kirrinsannassa_2.jpg/280px-BMW_E90_Kirrinsannassa_2.jpg', 'car')

concept.train('car')

