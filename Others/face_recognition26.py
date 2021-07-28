import cv2
import pickle
import numpy as np

face_cascade=cv2.CascadeClassifier(r'C:\Users\Priyanshu\AppData\Local\Programs\Python\Python39\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
specs=0

labels={}
with open('labels.pickle','rb') as f:
    og_labels=pickle.load(f)
    labels={v:k for k,v in og_labels.items()}

cap=cv2.VideoCapture(0)
while(True):
    r,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray)
    
    for [x,y,w,h] in faces:
        roi_gray=gray[y:y+h,x:x+w]
        roi_color=frame[y:y+h,x:x+w]

        id_,conf=recognizer.predict(roi_gray)
        if conf>=45:
            #print(labels[id_])
            font=cv2.FONT_HERSHEY_SIMPLEX
            name=labels[id_]
            color=(255,255,255)
            stroke=2
            cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
            
        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),0)
        
        if(specs==1):
            cv2.circle(frame,(int(x+w/3.5),int(y+h/2.5)),int(h/7),(0,0,0),2)
            cv2.circle(frame,(int(x+w-w/3.5),int(y+h/2.5)),int(h/7),(0,0,0),2)
            cv2.line(frame,(int(x+w/3.5+h/7),int(y+h/2.5)),(int(x+w-w/3.5-h/7),int(y+h/2.5)),(0,0,0),2)
            cv2.line(frame,(int(x+w/3.5+h/7),int(y+h-h/3.5)),(int(x+w-w/3.5-h/7),int(y+h-h/3.5)),(0,0,0),10)
        
        cv2.imshow('frame',frame)
    
    k=cv2.waitKey(5)
    
    if(k==ord('s')):
        if(specs==1):
            specs=0
            #pass
        elif(specs==0):
            specs=1
    if(k==ord('c')):
        cv2.imwrite('Capture.png',frame)
        
    if(k==ord('q')):
        break
cap.release()
cv2.destroyAllWindows()
