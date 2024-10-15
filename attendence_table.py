from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import csv
from tkinter import filedialog

mydata=[]
class attendence :
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face recognition System")

        title_lb1=Label(self.root,text="ATTENDENCE",font=("times new roman",35,"bold"),bg="Red",fg="white")
        title_lb1.place(x=0,y=0,width=1530,height=45)

        img3=Image.open(r"D:\PROJECTS\Attendence system_yt\images\bg.jpeg")
        img3=img3.resize((1530,710))
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=710)

        main_frame=Frame(bg_img,bd=2)
        main_frame.place(x=5,y=50,width=1500,height=600)


        Left_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student  Attendence Details",font=("times new roman",12,"bold"))
        Left_frame.place(x=10,y=10,width=760,height=580)

        left_inside_frame=Frame(Left_frame,bd=2)
        left_inside_frame.place(x=5,y=50,width=1500,height=600)

        

        #label and entry
        #attendence id
        attendenceid_label=Label(left_inside_frame,text="USN:",font=("times new roman",12,"bold"))
        attendenceid_label.grid(row=0,column=0)
        attendenceid_entry=ttk.Entry(left_inside_frame,width=20,font=("times new roman",13,"bold"))
        attendenceid_entry.grid(row=0,column=1,padx=10,sticky=W)

        #date
        date_label=Label(left_inside_frame,text="Date:",font=("times new roman",12,"bold"))
        date_label.grid(row=2,column=0)
        date_label_entry=ttk.Entry(left_inside_frame,width=20,font=("times new roman",13,"bold"))
        date_label_entry.grid(row=2,column=1,padx=10,sticky=W)\
        
        #TIME
        time_label=Label(left_inside_frame,text="Time:",font=("times new roman",12,"bold"))
        time_label.grid(row=2,column=2)
        time_label_entry=ttk.Entry(left_inside_frame,width=20,font=("times new roman",13,"bold"))
        time_label_entry.grid(row=2,column=3,padx=10,sticky=W)

        #attendence status
        status_label=Label(left_inside_frame,text="Status:",font=("times new roman",12,"bold"))
        status_label.grid(row=4,column=0)
        search_combo=ttk.Combobox(left_inside_frame, font=("times new roman", 13, "bold"), state="readonly ",width=20)
        search_combo["values"]=("Select ", "Preaent", "Absent")
        search_combo.current(0)
        search_combo.grid(row=4,column=1, padx=2, pady=1, sticky=W)

        

        # buttons

        btn_frame=Frame(left_inside_frame,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=130,width=715,height=145)

        #save button
        save_btn=Button(btn_frame,text="Inport csv",command=self.importcsv,width=20,font=("times new roman",12,"bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0)

        #export
        update_btn=Button(btn_frame,text="Export csv",command=self.exportcsv,width=20,font=("times new roman",12,"bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=1)

        #delete
        delete_btn=Button(btn_frame,text="Update",width=20,font=("times new roman",12,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)

        #reset
        delete_btn=Button(btn_frame,text="Reset",width=20,font=("times new roman",12,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=3)

        btn_frame2=Frame(left_inside_frame,bd=2,relief=RIDGE)
        btn_frame2.place(x=0,y=175,width=715,height=100)

        #right panel
        Right_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Attendence Details",font=("times new roman",12,"bold"))
        Right_frame.place(x=780,y=10,width=660,height=580)

        table_frame=Frame(Right_frame,bd=2,relief=RIDGE)
        table_frame.place(x=0,y=0,width=650,height=500)
        
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)
        self.report_table=ttk.Treeview(table_frame,column=("dept","USN","Name","date","time","Attendence status"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.report_table.xview)
        scroll_y.config(command=self.report_table.yview)

        self.report_table.heading("dept",text="Department")
        self.report_table.heading("USN",text="USN")
        self.report_table.heading("Name",text="Name")
        self.report_table.heading("time",text="Time")
        self.report_table.heading("date",text="Date")
        self.report_table.heading("Attendence status",text="Attendence status")

        self.report_table["show"]="headings"
        
        
        


        self.report_table.pack(fill=BOTH,expand=1)

#======fetch data=========
    def fetchdat(self,rows):
        self.report_table.delete(*self.report_table.get_children())
        for i in rows:
            self.report_table.insert("",END,values=i)

    def importcsv(self):
        global mydata
        mydata.clear
        fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("ALL FILE","*.*")),parent=self.root)
        with open(fln) as myfile:
            csvread=csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchdat(mydata)

    #expoert csv

    def exportcsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("no data","No data found",parent=self.root)
                return False
            fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("ALL FILE","*.*")),parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write=csv.writer(myfile,delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("data","Your data exported to "+os.path.basename(fln)+"successfully")
        except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)














if __name__ == "__main__":
     root=Tk()
     obj= attendence(root)
     root.mainloop()
