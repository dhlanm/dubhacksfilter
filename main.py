def rankImages(images, blockedWords):
	imageObjects = []
	for (image in images)
		imageObject = imageObject(image)
		imageObjects.add(imageObject)
	for (imageObject in imageObjects):
		words = getWords(imageObject.image)
		for (word in words):
			if (blockedWords contains word)
				image.score -= wordWeight
	rankedImages = sort(imageObjects by score)
	return rankedImage

class imageObject:
	path = '';
	words = None; 
	score = 0;
	
	def __init__(imagePath):
		path = imagePath
