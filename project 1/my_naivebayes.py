
# coding: utf-8

# In[108]:


from math import *
import re
import random
import sys
import numpy as np


# In[109]:


def my_naive_bayes(textdoc):
    testClasses={}
    global pcount
    global ncount
    classes={}
    dataset=[]
    trainSet=[]
    testSet=[]
    vocablen=0    
    probneg=0
    probpos=0
    neglen=0
    poslen=0
    accuracy=0
    likelihood_sump=0
    likelihood_sumn=0
    def read_reviews():
       
        ##SPLITTING DATA INTO TRAIN AND TEST
        filepath=("yelp_labelled.txt","amazon_cells_labelled.txt","imdb_labelled.txt")
        for file in filepath:
            with open(file, 'r') as doc:
                for line in doc:
                    dataset.append(line)
                random.shuffle(dataset)
                trainSet=dataset[0:int(len(dataset)*0.8)]
                testSet= dataset[int(len(dataset)*0.8):]
        return(trainSet,testSet)

    train_set, test_set=read_reviews()



# In[ ]:


    def train(data):
       docs=[]
       poscount=0
       negcount=0
       total=0
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
           cleandocs=re.sub(r"[0-9]+","",cleandoc)
       return (docs_final,poscount,negcount,total)
    
    docsFinal,poscount,negcount,total=train(train_set)
    
    posbag=classes[1]
    negbag=classes[0]        
    vocablen=len(docsFinal)
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
    
    word_likelihood=likeLihood(docsFinal)


    print("words in  vocab : {}".format(len(docsFinal)))
    print("words in  posbag : {}".format(poslen))
    print("words in  negbag : {}".format(neglen))
    #print("Bag of vocab : {}".format(docs))
    print("Log_prior neg  : {}".format((negcount)/(total)))
    print("Log_prior pos : {}".format((poscount)/(total)))
    #print("Bag of  negwords : {}".format(negbag))
    #print("Bag of poswords :{}".format(posbag))
    #print("likelihood for positiveclass :{}".format(poslikelihood))
    #print("likelihood for negativeclass :{}".format(neglikelihood))


    def test(tdoc):
        for line in tdoc:
            text=re.sub(r"['\n\t!():;&$?*#^@+]","",line.lower())
            cleantext=re.sub(r"[/,._-]"," ",text.lower())
            
            
            key =int(cleantext[-1])
            if testClasses.get(key)!= None:
                testClasses[key].extend(cleantext.split()[0:-1])
            else:
                testClasses[key] = [cleantext.split()[0:-1]]
        cleantexts=re.sub(r"[0-9]+","",cleantext)
        return(testClasses)
    testClasses=test(test_set)
    def tests(classtest,likelihood):
        corrects=0
        total=0    
        for line in testClasses[1]:
            pcount=1
            ncount=1
            total+=1
            for words in line:
                if words in wordLikelihood.keys():
                    pcount +=wordLikelihood[words][1]*probpos
                    ncount +=wordLikelihood[words][0]*probneg
                    p= pcount
                    n= ncount
            if p>n :
                corrects+=1
        for line in testClasses[0]:
            pcount=1
            ncount=1
            total+=1
            for words in line:
                if words in wordLikelihood.keys():
                    pcount *=wordLikelihood[words][1]*probpos
                    ncount *=wordLikelihood[words][0] * probneg
                    p=pcount
                    n= ncount
            if p < n :
                corrects+=1
        accuracy=((corrects/total)*100)
        print("the accuracy of the clasifier is: ",accuracy)
    tests(testClasses,wordLikelihood)


# In[ ]:


    def testpos(tdoc):
        with open(tdoc, 'r') as doc:
            for line in doc:
                text=re.sub(r"['\n\t!():;&$?*#^@+]","",line.lower())
                cleantexts=re.sub(r"[/,._-]"," ",text.lower())
                cleantext=re.sub(r"[0-9]+","",cleantexts)
                texts=(cleantext.split())
                poslike={}
                for i in texts:
                    likepos=np.log((posbag.count(i)+1)/(poslen + vocablen))
                    poslike[i]={likepos}
                    pvalues =poslike.values()
                    sum1 =0
                    for i in pvalues:
                        for r in i:
                            sum1 += r
        likelihood_sump =sum1 *probpos
        print("The probability that the statement is positive is : {}".format(likelihood_sump))
        return (likelihood_sump)
    p=testpos(textdoc)
     
    def testneg(tdoc):
         with open(tdoc, 'r') as doc:
             for line in doc:
                 text=re.sub(r"['\n\t!():;&$?*#^@+]","", line.lower())
                 cleantexts=re.sub(r"[/,._-]"," ",text.lower())
                 cleantext=re.sub(r"[0-9]+","",cleantexts)
                 texts=(cleantext.split())
                 
                 neglike={}
                 for i in texts:
                     likeneg=np.log((negbag.count(i)+1)/(neglen + vocablen))
                     neglike[i]={likeneg}
                     nvalues =neglike.values()
                     sum2 =0 
                     for i in nvalues:
                         for r in i:
                             sum2 += r
         likelihood_sumn =sum2 *probneg
         print("The probability that the statement is negative is : {}".format(likelihood_sumn))                
             
         return (likelihood_sumn)
    n=testneg(textdoc)
     
    results =open("result.txt","w+")
    if p > n:
        results .write('The statement has a  positive sentiment 1')
        print('The statement has a positive sentiment 1')
    else:
        results .write('The statement has a  negative sentiment 0')
        print('The statement is negative 0')


# In[ ]:


def main():
    script = sys.argv[0]
    file_name=sys.argv[1]
    my_naive_bayes(file_name)


# In[ ]:


main()

