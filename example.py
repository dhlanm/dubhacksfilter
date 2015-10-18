"""
Simple example showing Clarifai Custom Model training and prediction

This example trains a concept classifier that recognizes photos of the band Phish.
"""

from clarifai_basic import ClarifaiCustomModel
import os

os.environ["CLARIFAI_APP_ID"]="f_LGpdh9gta77vih9bOl-96qNU4Nbn5_x6j412N_"
os.environ["CLARIFAI_APP_SECRET"]="_daBl2t7eC9nAGb-IBOdYLfm1uqoCQH6MPlvAJR1"


# instantiate clarifai client
clarifai = ClarifaiCustomModel()

concept_name = 'phish'

# find some positive and negative examples
PHISH_POSITIVES = [
  'http://clarifai-test.s3.amazonaws.com/phish/positive/3652848536_c72244dc88_o.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/positive/4840976460_8463f9f319_b.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/positive/4904257471_20c0ff714f_b.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/positive/4904842036_6806f5fd25_b.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/positive/4904845798_aaf3392666_b.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/positive/6030148539_5d6da277c0_b.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/positive/9381652037_7e5e7665ab_k.jpg'
]

# add the positive example images to the model
for positive_example in PHISH_POSITIVES:
  clarifai.positive(positive_example, concept_name)


# negatives are not required but will help if you want to discriminate between similar concepts
PHISH_NEGATIVES = [
  'http://clarifai-test.s3.amazonaws.com/phish/negative/5587410471_cf932bf9fa_o.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/negative/7367377586_f5e7c59ef8_k.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/negative/8422034157_1fbe437d3a_b.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/negative/8464327405_5eaf39e6e2_o.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/negative/8804958484_9dcba3da19_k.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/negative/8805067594_f2abc5c751_k.jpg',
  'http://clarifai-test.s3.amazonaws.com/phish/negative/9583629691_a1594637a9_k.jpg'
]

# add the negative example images to the model
for negative_example in PHISH_NEGATIVES:
  clarifai.negative(negative_example, concept_name)

# train the model
clarifai.train(concept_name)


PHISH_EXAMPLES = [
  'https://clarifai-test.s3.amazonaws.com/photo-1-11-e1342391144673.jpg',
  'https://clarifai-test.s3.amazonaws.com/DSC01226-e1311293061704.jpg'
]

NOT_PHISH = [
  'https://clarifai-test.s3.amazonaws.com/2141620332_2b741028b3.jpg',
  'https://clarifai-test.s3.amazonaws.com/grateful_dead230582_15-52.jpg'
]

# If everything works correctly, the confidence that true positive images are of Phish should be
# significantly greater than 0.5, which is the same as choosing at random. The confidence that true
# negative images are Phish should be significantly less than 0.5.

# use the model to predict whether the test images are Phish or not
for test in PHISH_EXAMPLES + NOT_PHISH:
  result = clarifai.predict(test, concept_name)
  print(result['status']['message'], "%0.3f" % result['urls'][0]['score'], result['urls'][0]['url'])

# Our output is the following. Your results will vary as there are some non-deterministic elements
# of the algorithms used.

# Success 0.797 http://phishthoughts.com/wp-content/uploads/2012/07/photo-1-11-e1342391144673.jpg
# Success 0.706 http://bobmarley.cdn.junip.com/wp-content/uploads/2014/10/DSC01226-e1311293061704.jpg
# Success 0.356 http://farm3.static.flickr.com/2161/2141620332_2b741028b3.jpg
# Success 0.273 http://www.mediaspin.com/joel/grateful_dead230582_15-52.jpg
