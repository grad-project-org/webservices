# execute SP_ServicePhoto
# @ID =-1,	@photoFilePath = 'www.jhb.com',	@Nzha_Service_ID =8,
# @Nzha_User_ID= -1
import pymysql
import  json
from sqlalchemy import MetaData
import sqlalchemy as db
import urllib.parse
from flask import Flask
import json
from dict import dict
from flask import Flask, jsonify, request
from flask import Flask, request, render_template, send_from_directory
import pickle
import cv2
import pandas as pd
import datetime
import time
import os
import check_camera
import Capture_Image
import Train_Image
import Recognize

import csv
##############################


class Model:

    def connection(self):
        server = 'EVAL-FCI\HAMEDAHMED'
        database = 'NuzhaTec'
        username = 'sa'
        password = 'Ou@12345607'
        params = urllib.parse.quote_plus(
            'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        engine = db.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        return engine


    def storedProc(self,data):
        dict={}
        for key in data.keys():
         dict[key] = data[key]

        ##Create SQL Command
        variables = ""
        Nstored = ""
        for key, value in dict.items():
            if key == "stored":
                Nstored = value
            else:
                variables += f"@{key}={value},"

        variables = variables[:-1]

        sql = f"""EXEC {Nstored} {variables}"""
        print(sql)

        engine = self.connection()
        connectionn = engine.raw_connection()
        cursor = connectionn.cursor()

        cursor.execute(sql)
        records = cursor.fetchall()
        #print(records)
        # for row in records:
        #jsonn = str(records)[1:-1]
        #print(json.dumps(jsonn))

        jsonn = str(records)[3:-5]

        Modifedjsonn = jsonn.replace("', ), (',", ",")

        print(Modifedjsonn)


        #aa=json.load(jsonn)
        #print(records)
        #print(type(records))





            #print(jsonn)
        #print(jsonn[0])

        # aa='{    "Nzha_Service_ID": 37,    "Nzha_User_ID": 23,    "extendedTableID": 27,    "Nzha_CityName_ID": 22,    "Nzha_ServiceStatus_ID": 44,    "Nzha_Status_ID": 1,    "serviceName": "etfaas7",    "longtiude": 0.000000000,    "latitude ": 0.000000000,    "addressField": "Suez,musuem",    "extendedServiceName": "NzhaSrv_TrainingSession",    "descriptionField": "lkjlkj",    "NzhaSrv_TrainingSession": [      {        "Course_ID": 27,        "Topics": "It is an ICDL C ourse",        "sessionCode": "12021",        "onlineContact": "www.SuezUni_Courses.com",        "contactEmail": "SuezuniCourse@suezuni.com",        "contactPhoneNum": "01120399755",        "InstructorName": "Amir Ahmed",        "Instructor NationalSecNum": "29852360400278",        "fromDate": "2020-01-09T00:00:00",        "toDate": "2020-01-10T00:00:00",        "Nzha_Service_ID": 37      }    ]  },  {    "Nzha_Service_ID": 32,    "Nzha_User_ID": 22,    "extendedTableID": 22,    "Nzha _CityName_ID": 5,    "Nzha_ServiceStatus_ID": 22,    "Nzha_Status_ID": 1,    "serviceName": "dddd",    "longtiude": 0.000000000,    "latitude": 0.000000000,    "addressField": "asdasd",    "extendedServiceName": "NzhaSrv_Tr ainingSession",    "descriptionField": "NkdklfdkULL",    "NzhaSrv_TrainingSession": [      {        "Course_ID": 28,        "Topics": "It is an ICDsdsL Course",        "sessionCode": "1244021",        "onlineContact": "www.SuezUni_Courses. com",        "contactEmail": "dd",        "contactPhoneNum": "44",        "InstructorName": "Amir Ahmed",        "InstructorNationalSecNum": "23",        "fromDate": "2020-01-09T00:00:00",        "toDate": "2020-01-10T00:00:00",        "Nzha_Service _ID": 32      }    ]  }'
        # details = eval(aa)
        # #details = eval(jsonn.text)
        # length = len(details)
        # i=0
        # while(i<length):
        #    for course in details[i]['NzhaSrv_TrainingSession']:
        #        print(course['sessionCode'])
        #        i+=1

        # # < tr >
        # < td > {{course['sessionCode']}} < / td >
        # < td > {{course['Topics']}} < / td >
        # < td > {{course['fromDate']}} < / td >
        # < td > {{course['toDate']}} < / td >

        # records = cursor.fetchone()
        # for row in records:
        #       jsonn = str(row)[1:-1]
        # print(jsonn)
        # print(type(jsonn))
        connectionn.commit()
        return Modifedjsonn
     

  
    
    
    def gen_frames(self):  
        while True:
            camera = cv2.VideoCapture(0)
            
            success, frame = camera.read()  # read the camera frame
            
            if not success:
             
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
             
    
    

    
    
    
# counting the numbers


    def is_number(s ,self):
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



# Take image function

    def takeImages(self):
    

       Id = input("Enter Your Id: ")
       name = input("Enter Your Name: ")

       if((Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            
            
            

            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for(x,y,w,h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    #incrementing sample number
                    sampleNum = sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage" + os.sep +name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                 #display the frame
                    #cv2.imshow('frame', img)
                   

                       

                #Display the resulting frame in browser
                if not ret:
                        break
                else:
                    success, buffer = cv2.imencode('.jpg', img)
                    img = buffer.tobytes()
                    yield (b'--frame\r\n'
                              b'Content-Type: image/jpeg\r\n\r\n' + bytearray(img) + b'\r\n')  # concat frame one by one and show result
    
            #wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                  break
            # break if the sample number is morethan 100
                elif sampleNum > 80:
                 break
            
            
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for ID : " + Id + " Name : " + name
            row = [Id, name]
            with open("StudentDetails"+os.sep+"StudentDetails.csv", 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
             
                       
             
       else:
            if((Id)):
              print("Enter Alphabetical Name")
            if(name.isalpha()):
              print("Enter Numeric ID")
               
        
   


    
    
    

#-------------------------
    def recognize_attendence(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
        recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Id', 'Name', 'Date', 'Time']
        attendance = pd.DataFrame(columns=col_names)

        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for(x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
                Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

                if(conf < 50):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(
                        ts).strftime('%H:%M:%S')
                    aa = df.loc[df['Id'] == Id]['Name'].values
                    tt = str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

                else:
                    Id = 'Unknown'
                    tt = str(Id)
                if(conf > 75):
                    noOfFile = len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown"+os.sep+"Image"+str(noOfFile) +
                                ".jpg", im[y:y+h, x:x+w])
                cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
            attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
            cv2.imshow('im', im)
            if (cv2.waitKey(1) == ord('q')):
                break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName, index=False)
        cam.release()
        cv2.destroyAllWindows()

        print("Attendance Successfull")

    
    
    
    
    
    
    
    
    
    
     
    def CaptureFaces(self):
        Capture_Image.takeImages()
        key = input("Enter any key to return main menu")
        
        
    
    def Trainimages(self):
        Train_Image.TrainImages()
        key = input("Enter any key to return main menu")
    
    def RecognizeFaces(self):
        Recognize.recognize_attendence()
        key = input("Enter any key to return main menu")
     