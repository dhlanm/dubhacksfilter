from get_words import get_words_here
import glob     

class imageObject:  
    def __init__(self, imagePath):
        self.path = imagePath
        self.score = 0
    def get_path(self):
        return self.path

def main():
        images=[]
        for i in glob.glob("./images/*.jpg"):
            images.append(i)
        ##print(images)
        blocked=['marijuana']
        rank_images(images, blocked)
def rank_images(images, blockedWords):
    imageObjects = []
    for image in images:
        tempObject = imageObject(image)
        imageObjects.append(tempObject)
    i=0
    for iO in imageObjects:
        print(i)
        i+=1
        words = get_words_here(iO.get_path())
        for word in words:
            if word in blockedWords:
                print("IMAGE CONTAINS EVIL WORD :O", word)
                # Subtracts the image weight from the score
                image.score -= words[word]
    rankedImages = sorted(imageObject, key=imageObject.get)
    print (rankedImages)

if __name__=='__main__': main()
