from get_words import get_words

class imageObject:  
    def __init__(self, imagePath):
        self.path = imagePath
        self.score = 0
    def get_path(self):
        return self.path

def main():
        images=['http://www.clarifai.com/img/metro-north.jpg']
        blocked=['road']
        rank_images(images, blocked)
def rank_images(images, blockedWords):
    imageObjects = []
    for image in images:
        tempObject = imageObject(image)
        imageObjects.append(tempObject)
    for iO in imageObjects:
        words = get_words(iO.get_path())
        for word in words:
            if word in blockedWords:
                print("IMAGE CONTAINS EVIL WORD :O")
                # Subtracts the image weight from the score
                image.score -= words[word]
    rankedImages = sorted(imageObject, key=imageObject.get)
    print (rankedImages)

if __name__=='__main__': main()
