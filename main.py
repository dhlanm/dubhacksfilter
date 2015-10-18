from get_words import get_words_url

class imageObject:  
    def __init__(self, imagePath):
        self.path = imagePath
        self.score = 0
    def get_path(self):
        return self.path

def main():
        f=open('imageURLs.txt', 'r')
        images=f.readlines()
        for i in range(len(images)):
            images[i]=images[i].rstrip()
        f.close()
        ##print(images)
        blocked=['lizard']
        rank_images(images, blocked)
def rank_images(images, blockedWords):
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
            #print(word)
            if word in blockedWords:
                print("IMAGE CONTAINS EVIL WORD :O", word)
                # Subtracts the image weight from the score
                image.score -= words[word]
    rankedImages = sorted(imageObject, key=imageObject.get)
    print (rankedImages)

if __name__=='__main__': main()
