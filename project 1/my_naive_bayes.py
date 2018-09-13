from math import *
import re
def read_reviews(filepath):
    
    classes={}
    total=0
    docs=[]
    poscount = 0
    negcount = 0
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
    print("words in  vocab : {}".format(len(docs)))
    print("Bag of vocab : {}".format(docs))
    print("Prior probneg  : {}".format((negcount)/(total)))
    print("Prior probpos : {}".format((poscount)/(total)))
    print("Bag of  negwords : {}".format(negbag))
    print("Bag of poswords :{}".format(posbag))
   
  

