from tkinter import *
import tensorflow as tf
from keras import backend as K
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import face_recognition as fc
import numpy as np
import imutils
import cv2
import vlc
import time
import threading
import os
import copy
import random as r

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
music_dir=os.path.join(BASE_DIR,'Songs')
path=copy.copy(music_dir)

model=load_model('Keras_Model\_mini_XCEPTION.106-0.65.hdf5')
graph = tf.get_default_graph()
fd=cv2.CascadeClassifier(r'C:\Users\Priyanshu\AppData\Local\Programs\Python\Python36\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
em=['angry','disgust','fear','happy','sad','surprised','neutral']
v=cv2.VideoCapture(0)
exp=''
label_ids=[]

pl= vlc.MediaPlayer(path)
act="play"


def start1():

    global exp
    global graph

    while(1):
        
        r,i=v.read()
        gray=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
        faces=fd.detectMultiScale(gray)
        
        for [x,y,w,h] in faces:
            cv2.rectangle(i,(x,y),(x+w,y+h),(0,0,255),1)
            roi=gray[y:y+h,x:x+w]
            roi=cv2.resize(roi,(48,48))
            roi=roi.astype('float')/255.0
            roi=img_to_array(roi)
            roi=np.expand_dims(roi,axis=0)
            
            with graph.as_default():
                p=list(model.predict(roi)[0])
            exp=em[p.index(max(p))]
            

        cv2.imshow('frame',i)
        k=cv2.waitKey(5)
         

def play():
   
    global label_ids
    
    label_ids=[]
    
    global exp
    global path
    
    global pl
    global act
    
    if not exp=='':
        pl.stop()
        path=os.path.join(music_dir,exp)
        for root,dirs,files in os.walk(path):
            for file in files:
                if file.endswith('mp3') or file.endswith('wav'):
                    path=os.path.join(root,file)
                    label=os.path.basename(file)
                    #print(label,path)
                    if not label in label_ids:
                        label_ids.append(label)
                    
        print(label_ids)
        ran=r.choice(label_ids)
        print(ran)
        path_final=os.path.join(music_dir,exp,ran)
        print(path_final)
        pl= vlc.MediaPlayer(path_final)
        pl.play()
        act='play'
        print(exp)

def pause():

    global act
    status = b3['text']
    
    if(status=='Pause'):
        b3.config(text='Play',bg='green')
    else:
        b3.config(text='Pause',bg='yellow')
    pl.pause()
    act='pause'

def quit1():
    global v
    global pl
    
    v.release()
    pl.stop()
    cv2.destroyAllWindows()
    window.destroy()

def mul():
    p1=threading.Thread(target=start1)
    p1.start()


window=Tk()

mul()

b2=Button(window,text='Play New',bg='skyblue',command=play)
b2.grid(row=0,column=0)

b3=Button(window,text='Pause',bg='yellow',command=pause)
b3.grid(row=0,column=1)

b4=Button(window,text='Quit',bg='red',command=(quit1))
b4.grid(row=0,column=2)

window.mainloop()



