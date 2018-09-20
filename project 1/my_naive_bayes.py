from math import *
import re
def read_reviews(filepath,textdoc):
    
    classes={}
    total=0
    vocablen=0
    docs=[]
    poscount = 0
    negcount = 0
    probneg=0
    probpos=0
    neglen=0
    poslen=0
    likelihood_sump=0
    likelihood_sumn=0
    with open(filepath, 'r') as doc:
        for line in doc:
            cleanline=re.sub(r"['\n\t!():;&$?*#^@+]","",line.lower())
            cleandoc=re.sub(r"[/,._-]"," ",cleanline.lower())
            docs.extend(cleandoc.split()[0:-1])
            docs=list(set(docs))
            
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
    posbag=classes[1]
    negbag=classes[0]        
    vocablen=len(docs)
    probneg=(negcount)/(total)
    probpos=(poscount)/(total)
    poslen=len(posbag)
    neglen=len(negbag)
    poslikelihood={}
    neglikelihood={}
    for i in docs:
            likelihoodp=(posbag.count(i)+1)/(poslen + vocablen)
            poslikelihood[i]={likelihoodp}
            likelihoodn=(negbag.count(i)+1)/(neglen + vocablen)
            neglikelihood[i]={likelihoodn}
            
  
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
   
    def testpos(tdoc):
        with open(tdoc, 'r') as doc:
            for line in doc:
                text=re.sub(r"['\n\t!():;&$?*#^@+]","",line.lower())
                cleantext=re.sub(r"[/,._-]"," ",text.lower())
                texts=(cleantext.split())
                poslike={}
                for i in texts:
                    likepos=(posbag.count(i)+1)/(poslen + vocablen)
                    poslike[i]={likepos}
                pvalues =poslike.values()
                sum1 =0 
                for i in pvalues:
                    for r in i:
                        sum1 += r
                #print(sum1)
                likelihood_sump =sum1 *probpos
                print("The probability that the statement is positive is : {}".format(likelihood_sump))
                return (likelihood_sump)
                 
    testpos(textdoc)
    def testneg(tdoc):
       with open(tdoc, 'r') as doc:
            for line in doc:
                text=re.sub(r"['\n\t!():;&$?*#^@+]","", line.lower())
                cleantext=re.sub(r"[/,._-]"," ",text.lower())
                texts=(cleantext.split())
                neglike={}
                for i in texts:
                    likeneg=(negbag.count(i)+1)/(neglen + vocablen)
                    neglike[i]={likeneg}
                nvalues =neglike.values()
                sum2 =0 
                for i in nvalues:
                    for r in i:
                        sum2 += r
                #print(sum2)
                likelihood_sumn =sum2 *probneg
                print("The probability that the statement is negative is : {}".format(likelihood_sumn))
                return (likelihood_sumn)
    testneg(textdoc)
    
    if likelihood_sump > likelihood_sumn:
        print('The statement is positive')
    else:
        print('The statement is negative')
    
