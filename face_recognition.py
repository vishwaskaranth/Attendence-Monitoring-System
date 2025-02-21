from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np
from time import strftime
from datetime import datetime

class Face_recognition:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face recognition System")

        title_lb1=Label(self.root,text="FACE RECOGNITION",font=("times new roman",35,"bold"),bg="Red",fg="white")
        title_lb1.place(x=0,y=0,width=1530,height=45)

        b1l=Button(self.root,text="RECOGNIZE FACE",command=self.face_recog,cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="black")
        b1l.place(x=650,y=150,width=200,height=60)

    def mark_attendence(self,n,d,r):
        with open("vk.csv","r+",newline="\n") as f:
            myDataLiist=f.readlines()
            name_list=[]
            for line in myDataLiist:
                entry=line.split((","))
                name_list.append(entry[0])
            if((n not in name_list) and (d not in name_list) and (r not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{n},{d},{r},{dtString},{d1},present")

            

#=====FACE RECOGNITION======
    def face_recog(self):
        def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

            coord=[]

            for(x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                confidence=int((100*(1-predict/300)))

                conn=mysql.connector.connect(host="localhost",username="root",password="****",database="face_recognition")
                my_cursor=conn.cursor()

                my_cursor.execute("select Name from student where USN="+str(id))
                n=my_cursor.fetchone()
                n="+".join(n)

                my_cursor.execute("select Department from student where USN="+str(id))
                d=my_cursor.fetchone()
                d="+".join(d)

                my_cursor.execute("select Year from student where USN="+str(id))
                r=my_cursor.fetchone()
                r="+".join(r)
                
                
                

                if confidence>77:
                    cv2.putText(img,f"Name:{n}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Dept:{d}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Year:{r}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendence(n,d,r)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknow face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                coord=[x,y,w,h]
            return coord
        
        def recognize(img,clf,faceCascade):
            coord=draw_boundray(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
            return img
        
        faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap=cv2.VideoCapture(0)

        while True:
            ret,img=video_cap.read()
            img=recognize(img,clf,faceCascade)
            cv2.imshow("Welcome to face Recognition",img)
            if cv2.waitKey(1)==13:
                break
        video_cap.release()
        cv2.destroyAllWindows()

    




if __name__ == "__main__":
     root=Tk()
     obj= Face_recognition(root)
     root.mainloop()
