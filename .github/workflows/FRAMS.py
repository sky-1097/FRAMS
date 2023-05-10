import tkinter as tk
from tkinter import Message ,Text
import shutil
import csv
from csv import DictWriter
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import cv2
import tkinter.ttk as ttk
import tkinter.font as font
import hypothesis
import os
from pandas import DataFrame

window1 = tk.Tk()
window1.title("Attendance")
window1.geometry('600x300')
window1.configure(background='grey')
message1 = tk.Label(window1, text="Attendance Portal"  ,fg="white", bg="black"  ,font=('arial', 25, 'bold underline')) 
message1.place(x=160, y=35)


def DispWin():
    
    window = tk.Tk()
    window.title("Face_Recogniser")

    dialog_title = 'QUIT'
    dialog_text = 'Are you sure?'
 
    window.geometry('1280x720')
    window.configure(background='black')


    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)


    message = tk.Label(window, text="Attendance Management System"  ,fg="white", bg="black"  ,font=('arial', 26, 'bold underline')) 

    message.place(x=300, y=50)

    lbl = tk.Label(window, text="Enter Roll No.",width=20  ,height=2, bg="grey"  ,font=('arial', 15, ' bold ') ) 
    lbl.place(x=200, y=200)

    txt = tk.Entry(window,width=20  ,bg="white" ,font=('arial', 15, ' bold '))
    txt.place(x=600, y=215)

    lbl2 = tk.Label(window, text="Enter Name",width=20  ,bg="grey"    ,height=2 ,font=('arial', 15, ' bold ')) 
    lbl2.place(x=200, y=300)

    txt2 = tk.Entry(window,width=20  ,bg="white"  ,font=('arial', 15, ' bold ')  )
    txt2.place(x=600, y=315)

    lbl3 = tk.Label(window, text="Notification : ",width=20  ,bg="grey"  ,height=2 ,font=('arial', 15, ' bold ')) 
    lbl3.place(x=200, y=400)

    message = tk.Label(window, text="" ,bg="grey"  ,width=30  ,height=2, activebackground = "yellow" ,font=('arial', 15, ' bold ')) 
    message.place(x=600, y=400)

    

    

    
    
 
    def clear():
        txt.delete(0, 'end')    
        res = ""
        message.configure(text= res)

    def clear2():
        txt2.delete(0, 'end')    
        res = ""
        message.configure(text= res)    
    
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
 
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
 
        return False
 
    def TakeImages():        
        Id=(txt.get())
        name=(txt2.get())
        if(is_number(Id) and name != ""):








            
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    sampleNum=sampleNum+1
                    cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    cv2.imshow('frame',img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum>60:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = "Images Saved for ID : " + Id +" Name : "+ name
            row = [Id , name]
            with open('StudentDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text= res)

    def TrainImages():
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        faces,Id = getImagesAndLabels("TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save("trainner.yml")
        res = "Images Trained"
        message.configure(text= res)







    def getImagesAndLabels(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        faces=[]
        Ids=[]
        for imagePath in imagePaths:
            pilImage=Image.open(imagePath).convert('L')
            imageNp=np.array(pilImage,'uint8')
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)        
        return faces,Ids

    
        
    clearButton = tk.Button(window, text="Clear", command=clear  ,width=5  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton.place(x=850, y=210)
    clearButton2 = tk.Button(window, text="Clear", command=clear2  ,width=5  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton2.place(x=850, y=310)    
    takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 17, ' bold '))
    takeImg.place(x=200, y=500)
    trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 17, ' bold '))
    trainImg.place(x=500, y=500)
    quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,width=12  ,height=2, activebackground = "Red" ,font=('times', 17, ' bold '))
    quitWindow.place(x=800, y=500)
    window.mainloop()


def MarkAttendence(attendence, filename, name):
    if (os.path.exists(filename)):
        field_names = ['Id', 'Name', 'Date', 'Time']

        res = attendence
        nm = "".join(name)
        id1 = res.iloc[0]['Id']
        dt = res.iloc[0]['Date']
        tm = res.iloc[0]['Time']

        dict = {'Id': id1, 'Name': nm, 'Date': dt, 'Time': tm}

        with open(filename, 'a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(dict)
            f_object.close()

    else:
        attendence.to_csv(filename, index=False)



def TrackImages():
        global aa
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);
        df=pd.read_csv("StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names =  ['Id','Name','Date','Time']
        attendance = pd.DataFrame(columns = col_names)
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 60):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].values
                    tt=str(Id)+"-"+aa
                    nm = "".join(aa)
                    attendance.loc[len(attendance)] = [Id,nm,date,timeStamp]
                
                else:
                    Id='Unknown'                
                    tt=str(Id)  
                        
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
            cv2.imshow('Press q to mark attendance',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Attendance\Attendance_"+date+".csv"
        MarkAttendence(attendance, fileName, aa)
        cam.release()
        cv2.destroyAllWindows()
        res = attendance
        #print(res.iloc[0])
        #print("".join(aa))
        nm = "".join(aa)
        id1 = res.iloc[0]['Id']
        dt = res.iloc[0]['Date']
        tm = res.iloc[0]['Time']
        message2.configure(text= "ID              NAME              DATE              TIME")
        message3.configure(text= str(id1)+"             "+nm+"          "+dt+"          "+tm)

Attend = tk.Button(window1, text="Attendance", command=TrackImages  ,width=10  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
Attend.place(x=110, y=140)
Register = tk.Button(window1, text="Register", command=DispWin  ,width=10  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
Register.place(x=360, y=140)
message2 = tk.Label(window1, text="" ,bg="grey",activeforeground = "black",width=40  ,height=1  ,font=('arial', 15, ' bold '))
message2.place(x=60, y=220)
message3 = tk.Label(window1, text="" ,bg="grey",activeforeground = "black",width=45  ,height=1  ,font=('arial', 15, ' bold '))
message3.place(x=40, y=255)

window1.mainloop()
