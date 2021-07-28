import smtplib
import pandas as pd
import numpy as np

df1=pd.read_csv(r'attendence.csv',index_col='Label_Ids')
df2=pd.read_csv(r'mailids.csv',index_col='Label_Ids')
late=0
present=0
absent=0

#defining columns
names=np.array(df2.loc[:,'Names'])
mailids=np.array(df2.loc[:,'email'])
ids=[]
n=0
for i in names:
    ids.append(n)
    n+=1
'''
print(names)
print(mailids)
print(ids)
'''
for j in ids:
    late=0
    present=0
    absent=0
    arr1=(np.array(df1.loc[j,:]))
    total=len(arr1)-1
    #print(total)
    for i in arr1:
        if i=='Late':
            late=late+1
        elif i=='Absent':
            absent+=1
        elif i=='Present':
            present+=1
    percent=str(present*100/total)
    content1='Percentage of attendence=',percent
    content=str(df1.loc[j,:])+str(content1)
    print(content)
   
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("f20180509@goa.bits-pilani.ac.in", "i@universe")
    server.sendmail("f20180509@goa.bits-pilani.ac.in",mailids[j],content)
    server.quit()

