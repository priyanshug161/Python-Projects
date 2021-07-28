import cv2
import pandas as pd
import numpy as np
import datetime as dt

face_cascade=cv2.CascadeClassifier(r'C:\Users\Priyanshu\AppData\Local\Programs\Python\Python39\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer2.yml')
df=pd.read_csv(r'attendence.csv',index_col='Label_Ids')
name='Not Recognized'

#defining columns
col2=np.array(df.loc[:,'Names'])
col1=[]
n=0
for i in col2:
    col1.append(n)
    n+=1

#Defining labels
labels={v:k for k,v in zip(col2,col1)}

#Face recognition
cap=cv2.VideoCapture(0)
while(True):
    r,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray)
    
    for [x,y,w,h] in faces:
        roi_gray=gray[y:y+h,x:x+w]
        roi_color=frame[y:y+h,x:x+w]
        name='Not Recognized'

        id_,conf=recognizer.predict(roi_gray)
        if conf>=45:
            #Editing font Style
            font=cv2.FONT_HERSHEY_SIMPLEX
            name=labels[id_]
            color=(0,0,255)
            stroke=2
            cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)           
        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),0)
             
        cv2.imshow('frame',frame)
    
    k=cv2.waitKey(5)
    if(k==ord('c')):
        cv2.imwrite('Capture.png',frame)
        
    if(k==ord('q')):
        break
    
    if(k==ord('m')):
        if(name=='Not Recognized'):
            print(name)
        else:
            dates=np.array(df.columns)
            now=dt.datetime.now()
            today=str(now.date())
            hour=int(now.hour)
            minute=int(now.minute)
            
            if today not in dates:
                df[today]=df.shape[0]*['Absent']

            if(hour==9  and minute<=30):
                df.loc[id_,today]='Present'
                print('')
                print('')
                print('Attendence Marked for '+name)

            else:
                df.loc[id_,today]='Late'
                print('')
                print('')
                print('You are late '+name)
                
            print(df)
            df.to_csv(r'attendence.csv')
cap.release()
cv2.destroyAllWindows()

