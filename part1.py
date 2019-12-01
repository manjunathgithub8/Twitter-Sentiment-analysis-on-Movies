from __future__ import absolute_import, division, print_function, unicode_literals

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd

#!pip install -q tensorflow-hub
#!pip install -q tensorflow-datasets
import tensorflow_hub as hub
import tensorflow_datasets as tfds

#model.save('my_model.h5')
new_model = tf.keras.models.load_model('my_model.h5',custom_objects={'KerasLayer':hub.KerasLayer})

new_model.summary()

from twitterscraper import query_tweets
import datetime as dt
import pandas as pd

begindate=dt.date(2019,9,15)
enddate=dt.date(2019,11,16)
mn=""
global restvander
ct=0
count=0
tot=0
pos=0
neg=0
neu=0

def getmov(movname):
    global mn
    mn=movname


    tweets=query_tweets(mn,begindate=begindate,enddate=enddate,limit=100,lang='english')

    import re
    tweetfa=[]

    for t in tweets:
        #tweetf=re.sub(r'[^\w]', ' ', t.text)
        tweetftemp = t.text.split()
        cw=0
        leng=len(tweetftemp)
        while(cw!=leng):

            #print(cw)
            #print(word)

            if 'http' in tweetftemp[cw]:
                tweetftemp.remove(tweetftemp[cw])
            elif '@' in tweetftemp[cw]:
                tweetftemp.remove(tweetftemp[cw])
            elif 'pic.' in tweetftemp[cw]:
                tweetftemp.remove(tweetftemp[cw])

            else:cw+=1
            leng=len(tweetftemp)

        tweetfa.append(' '.join(tweetftemp))
    print("\n",tweetfa)
    print(len(tweetfa),"length")

    #print(tweetfa," \n ")
        #print("after remove :"+tweetf,"before : "+t.text)

    coun=0
    avg=0
    for t in tweetfa:
        print(t)
        result=new_model.predict([t])
        temp=result[0]
        avg+=float(temp[0])
        print("start ",temp[0],"--->",t,"End ")
        coun=coun+1;
    print("Final: ",(avg/coun),"count:",coun)
    restmodel=avg/coun

    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    from textblob import TextBlob

    def sentiment_scores(sentence):
        global pos,neg,neu
        print("start ",sentence," End ")
        #sen1=TextBlob(sentence)
        #print("text blob :", sen1.sentiment)

        # Create a SentimentIntensityAnalyzer object.
        sid_obj = SentimentIntensityAnalyzer()

        sentiment_dict = sid_obj.polarity_scores(sentence)

        print("Overall sentiment dictionary is : ", sentiment_dict)
        print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
        print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
        print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")

        print("Sentence Overall Rated As", end = " ")
        global ct,count,tot
        tot+=(sentiment_dict['pos']-sentiment_dict['neg'])+sentiment_dict['neu']
        if sentiment_dict['compound']!=0.0:
            ct+=sentiment_dict['compound']
            count+=1

        # decide sentiment as positive, negative and neutral
        if sentiment_dict['compound'] >= 0.05 :
            print("Positive")
            pos+=1

        elif sentiment_dict['compound'] <= - 0.05 :
            print("Negative")
            neg+=1

        else :
            print("Neutral")
            neu+=1

            # function calling
    for t in tweetfa:
        sentiment_scores(t)
    print("new:",tot/count,((tot/count)/2)*100,"%")
    restvander=(((tot/count)/2)+restmodel)/2*100
    restvander=str(restvander)+" %"
    print(restvander)

    return restvander,pos,neg,neu
