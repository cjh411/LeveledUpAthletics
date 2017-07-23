# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import numpy  as np
import pandas as pd
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
exercise="bcurl"
path='/Users/christopherhedenberg/Documents/Recess/rep_models/data/train/'

hpath='/Users/christopherhedenberg/Documents/Recess/rep_models/data/train/'
readings=40
def tv_split(row):
    r=np.random.uniform(0,1)
    if r<.7:
        return 'T'
    else:
        return 'V'

bcurl_hout=pd.read_csv(path+exercise+"/dumbell/"+exercise+"_overlap.txt")
bcurl_final=pd.read_csv(hpath+exercise+"/dumbell/"+exercise+"_overlap.txt")
bcurl_final=bcurl_final.fillna(0,axis=0)
bcurl_hout=bcurl_hout.fillna(0,axis=0)
#for i in os.listdir(path)[1:]:
#    if i!=exercise:
#        file=pd.read_csv(path+i+"/"+i+"_overlap.txt")
#        file=file.fillna(0,axis=0)
#        file[file['rep']==1]=0
#        bcurl_final=bcurl_final.append(file)
        

bcurl_final=bcurl_final.iloc[:,1:]
bcurl_hout=bcurl_hout.iloc[:,1:]
#split dataset into train 'T' and test 'V'
bcurl_final['TV']=bcurl_final.apply(tv_split, axis=1)
train=bcurl_final[bcurl_final.TV=='T']
val=bcurl_final[bcurl_final.TV=='V']

#split data into predictors and target
cols=readings*4
x_train=train.ix[:,0:cols]
y_train=train['rep']
x_val=val.ix[:,0:cols].copy()
y_val=val['rep']

x_holdout=bcurl_hout.ix[:,0:cols].copy()
y_holdout=bcurl_hout['rep']

#fit model
clf = RandomForestClassifier(n_estimators=100,min_samples_leaf=5,oob_score=False)
clf = clf.fit(x_train,y_train)

#fit model
gbm = GradientBoostingClassifier(n_estimators=500, learning_rate=.1, random_state=0)
gbm = gbm.fit(x_train,y_train)

#score model
print(clf.score(x_train,y_train))
est=clf.predict(x_val)
print(clf.score(x_val,y_val))
print(metrics.confusion_matrix(y_val,est))

print(gbm.score(x_train,y_train))
est=gbm.predict(x_val)
print(gbm.score(x_val,y_val))
print(metrics.confusion_matrix(y_val,est))

est=clf.predict(x_holdout)
print(metrics.confusion_matrix(y_holdout,est))
#
##read raw data for scoring real time streaming
#bcurl=pd.read_csv('/Users/elizabethvassallo/Documents/Recess/rep_models/data/train/bcurl/bcurl_tv.txt')
#
##id creation
#bcurl['id']=(bcurl['rep']!=bcurl['rep'].shift()).cumsum()-1
#
##index creation
#i,ind=0, []
#while i < len(bcurl):
#    ind.append(i)
#    i+=1    
#bcurl['index']=ind          
#bcurl.sort(['index'],ascending=[0],inplace=1)
#
##reading=
#bcurl['one']=1
#bcurl['reading']=bcurl.groupby('id')['one'].cumsum()
#bcurl=bcurl.iloc[:,1:]
#
##create inputs to real time scoring
#index=['x','y','z','gyro']
#reading=[]
#for i in range(1,readings+1):
#    reading.append(i)
#score=pd.DataFrame(index=reading,columns=index)
#score=score.fillna(0)
#bcurl['rep2']=0
#bcurl=bcurl.fillna(0)
#
#
##function to score model on real time data. Using a window of 40 readings, it starts with
##readings 1-40, predicting whether its a rep. If it isn't a rep, move to window
## 2:41, 3:42, etc.. until a rep is found. Once a rep is found at window 3:42,skip ahead 9
##readings to 12:51 and look for a rep. 
#def scorestream(dsn,i,readno,reading,index,jmp):
#
#    while i<len(bcurl)-readno:
#        score=dsn.iloc[i:readno+i,:4]
#        score['id']=1
#        score['reading']=reading
#        if clf.predict(pd.pivot_table(score,index='id', columns='reading',values=['x','y','z','gyro']))[0]==1:
#            dsn['rep2'].iloc[i]=1
#            i=i+9
#
#
#        i=i+1
##score model and save results
#scorestream(bcurl,0,readings,reading,index,20)
#print (bcurl.groupby('rep').sum())
#bcurl.to_csv('/Users/elizabethvassallo/Documents/Recess/rep_models/data/model_output/bcurl_score.txt')

#save model
model_path='/Users/christopherhedenberg/Documents/Recess/rep_models/models/%s/%s_rf_out.pkl' %(exercise,exercise)
joblib.dump(clf,model_path)

#code to load model again
joblib.load(model_path)