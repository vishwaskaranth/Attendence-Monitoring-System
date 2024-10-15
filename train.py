from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Train :
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face recognition System")

        title_lb1=Label(self.root,text="TRAIN DATASET",font=("times new roman",35,"bold"),bg="Red",fg="white")
        title_lb1.place(x=0,y=0,width=1530,height=45)

        b1l=Button(self.root,text="TRAIN DATA",command=self.train_classifier,cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="black")
        b1l.place(x=650,y=150,width=200,height=60)

    def train_classifier(self):
        data_dir=("data")
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]

        faces=[]
        ids=[]

        for image in path:
            img=Image.open(image).convert('L') #GRey scale img
            imageNp=np.array(img,'uint8')
            id=int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)==13
        ids=np.array(ids)

        #===========tarining the classifier====
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows
        messagebox.showinfo("Result","TRAINING THE DATASET COMPLETED!!!")







if __name__ == "__main__":
     root=Tk()
     obj= Train(root)
     root.mainloop()