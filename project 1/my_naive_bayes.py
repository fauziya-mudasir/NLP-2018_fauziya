from math import *
import re
import random
import numpy as np
def read_reviews(*filepath):
    testClasses={}
    global pcount
    global ncount
    classes={}
    dataset=[]
    trainSet=[]
    testSet=[]
    total=0
    vocablen=0
    docs=[]
    poscount = 0
    negcount = 0
    probneg=0
    probpos=0
    neglen=0
    poslen=0
    accuracy=0
    likelihood_sump=0
    likelihood_sumn=0
    for file in filepath:
        with open(file, 'r') as doc:
            for line in doc:
                dataset.append(line)
            random.shuffle(dataset)
            trainSet=dataset[0:(len(dataset)*0.8)]
            testSet= dataset[(len(dataset)*0.8):]
            def train(data):
                for lines in data:
                    cleanline=re.sub(r"['\n\t!():;&$?*#^@+]","",lines.lower())
                    cleandoc=re.sub(r"[/,._-]"," ",cleanline.lower())

                    docs.extend(cleandoc.split()[0:-1])
                    docs_final=list(set(docs))

                    key =int(cleandoc[-1])
                    if key == 1:
                        poscount+=1
                    else:
                        negcount+=1
                    if classes.get(key)!= None:
                        classes[key].extend(cleandoc.split()[0:-1])
                    else:
                        classes[key] = [cleandoc.split()[0:-1]]
                    total+=1
                    return (docs_final)
                train(trainSet)
    posbag=classes[1]
    negbag=classes[0]        
    vocablen=len(docs)
    probneg=np.log((negcount)/(total))
    probpos=np.log((poscount)/(total))
    poslen=len(posbag)
    neglen=len(negbag)
    wordLikelihood={}
    def likeLihood(tdocs):
        for i in tdocs:
                likelihoodp=np.log(posbag.count(i)+1)/(poslen + vocablen)
                likelihoodn=np.log(negbag.count(i)+1)/(neglen + vocablen)
                wordLikelihood[i]=(likelihoodp,likelihoodn)
                return (wordLikelihood)
    likeLihood(docs_final)

  
    print("words in  vocab : {}".format(len(docs)))
    print("words in  posbag : {}".format(poslen))
    print("words in  negbag : {}".format(neglen))
    #print("Bag of vocab : {}".format(docs))
    print("Prior probneg  : {}".format((negcount)/(total)))
    print("Prior probpos : {}".format((poscount)/(total)))
    #print("Bag of  negwords : {}".format(negbag))
    #print("Bag of poswords :{}".format(posbag))
    #print("likelihood for positiveclass :{}".format(poslikelihood))
    #print("likelihood for negativeclass :{}".format(neglikelihood))


    def test(tdoc):
        corrects=0
        total=0
        for line in tdoc:

            text=re.sub(r"['\n\t!():;&$?*#^@+]","",line.lower())
            cleantext=re.sub(r"[/,._-]"," ",text.lower())

            key =int(cleantext[-1])

                if testClasses.get(key)!= None:
                    testClasses[key].extend(cleantext.split()[0:-1])
                else:
                    testClasses[key] = [cleantext.split()[0:-1]]


            for line in testClasses[1]:
                pcount=1
                ncount=1
                total+=1
                for words in line:
                    if word in wordLikelihood.keys():
                        pcount +=wordLikelihood[words][1]
                        ncount +=wordLikelihood[words][0]
                p= pcount*probpos
                n= ncount*probneg
                if p>n :
                    corrects+=1
            for line in testClasses[0]:
                pcount=1
                ncount=1
                total+=1
                for words in line:
                    if word in wordLikelihood.keys():
                        pcount +=wordLikelihood[words][1]
                        ncount +=wordLikelihood[words][0]
                p=pcount*probpos
                n= ncount * probneg
                if p < n :
                    corrects+=1
        accuracy=((corrects/total)*100)
    print("the accuracy of the clasifier is: ",accuracy)
test(testSet)
def testMain(file)






