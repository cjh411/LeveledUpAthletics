import os
import csv
import pandas as pd
import numpy as np

exercise='bcurl'
path='/Users/christopherhedenberg/Documents/Recess/rep_models/data/train/%s/dumbell' %exercise
outfile=path+'/'+'%s_tv.txt' %exercise
outfile_final=path+'/'+'%s_overlap.txt' %exercise
outfile_java=path+'/'+'%s_overlap_java.txt' %exercise

outdf=pd.DataFrame(columns=['x','y','z','gyro','rep','ts'],)

for i in os.listdir(path+'/raw'):
    if i.endswith(".txt"):
        file=pd.read_csv(path+'/raw/'+i,header=None,index_col=False,names=['x','y','z','gyro','rep','ts'])
        outdf=outdf.append(file)
        

def tv_split(row):
    r=np.random.uniform(0,1)
    if r<.7:
        return 'T'
    else:
        return 'V'



outdf=outdf.convert_objects(convert_numeric=True)
outdf.to_csv(outfile)        

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd


bcurl=outdf

bcurl=bcurl.iloc[1:,0:7]
n=0

readings=40
buffer=1

j=0
k=1
startind=0



#id creation
bcurl['id']=(bcurl['rep']!=bcurl['rep'].shift()).cumsum()-1

bcurl['rep'].replace(to_replace=0,value=2,inplace=True)
bcurl['rep'].replace(to_replace=1,value=0,inplace=True)
bcurl['rep'].replace(to_replace=2,value=1,inplace=True)
#index creation
i,ind=0, []
while i < len(bcurl):
    ind.append(i)
    i+=1    
bcurl['index']=ind          
bcurl.sort(['index'],ascending=[0],inplace=1)
bcurl=bcurl.reset_index().drop('level_0',1)

#reading=
bcurl['one']=1
bcurl['reading']=bcurl.groupby('id')['one'].cumsum()



#filtering fields
bcurl['rep2']=bcurl['rep']-bcurl['rep'].shift()
bcurl['l5']=bcurl[(bcurl['reading']<6) & (bcurl['rep']==1)]['one']
bcurl.fillna(0,inplace=True)  


#repdata
temp=bcurl.iloc[0:0+readings,:]
temp['reading']=temp['one'].cumsum()
index=bcurl[bcurl['rep2']==1].index.values
bcurl_rep=pd.DataFrame(index=[],columns=pd.pivot_table(temp,index='one',columns='reading',values=['x','y','z','gyro']).columns.values)
for i in index:
    temp=bcurl.loc[i:i+readings+1,:]
    temp['reading']=temp['one'].cumsum()
    n+=1
    bcurl_rep.loc[n,:]=pd.pivot_table(temp,index='one',columns='reading',values=['x','y','z','gyro']).iloc[0,:]

bcurl_rep['rep']=1



#nonrep data
temp=bcurl.iloc[0:0+readings,:]
temp['reading']=temp['one'].cumsum()
bcurl_nrep=pd.DataFrame(index=[],columns=pd.pivot_table(temp,index='one',columns='reading',values=['x','y','z','gyro']).columns.values)
i, n = 0, bcurl_rep.index.max()      
for row in bcurl.iterrows():

    n+=1
    
    if bcurl['l5'].iloc[i:i+7].max()==0:
        temp=bcurl.iloc[i:i+readings,:]
        temp['reading']=temp['one'].cumsum()
        bcurl_nrep.loc[n,:]=pd.pivot_table(temp,index='one',columns='reading',values=['x','y','z','gyro']).iloc[0,:]

    i+=3

bcurl_nrep['rep']=0    

    
bcurl_rep.append(bcurl_nrep).to_csv(outfile_final)
bcurl_rep.append(bcurl_nrep).to_csv(outfile_java,index=False,header=False)
#def rep_output(dsn,i,readno,readarr,index,jmp):        
    