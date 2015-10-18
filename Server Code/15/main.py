from get_words import get_words_url
import urllib.request

class imageObject:  
    def __init__(self, imagePath):
        self.path = imagePath
        self.score = 0
    def get_path(self):
        return self.path

##def main(): #OLD
##        f=open('imageURLs.txt', 'r')
##        images=f.readlines()
##       for i in range(len(images)):
##            images[i]=images[i].rstrip()
##        f.close()
##        ##print(images)
##        blocked=['lizard']
##        rank_images(images, blocked)

#def main():
    #somehow recieve POST request

def rank_images(images, blockedWords):
    print(blockedWords)
    badfile=open('bad_images.txt', 'a')
    goodfile=open('good_images.txt', 'a')
    imageObjects = []
    for image in images:
        tempObject = imageObject(image)
        imageObjects.append(tempObject)
    i=0
    import json
    words={good: [], bad: []}
    for iO in imageObjects:
        print(i, end='')
        i+=1
        words = get_words_url(iO.get_path())
        for word in words:
            #print(word)
            if word in blockedWords:
                #print("IMAGE CONTAINS EVIL WORD :O", word)
                #print(iO.get_path, file=badfile)
                words['bad'].append(iO.get_path)
                break
                # Subtracts the image weight from the score
                # image.score -= words[word]
        else:
            #print(iO.get_path, file=goodfile)
            words['good'].append(iO.get_path)
    rankedImages = sorted(imageObject, key=imageObject.get)
    return rankedImages
    #print (rankedImages)

#if __name__=='__main__': main()
