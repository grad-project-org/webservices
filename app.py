from flask import Flask
import json
from flask import Flask, jsonify, request,session,Response
from flask import Flask, request, render_template, send_from_directory
import cv2
import random
import os
###############################
from StoredProc import Model



# Initialize Flask
app = Flask(__name__)



from flask_cors import CORS

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True
app.config['TESTING'] = True
import pymysql
##### Connection #####


ob = Model()
##@app.route('/checkCamera',methods=['GET','POST'])
#def checkCamera():##########
#check_camera.camer()
##  frame=ob.camer()
## ret=ob.camer() 
### return render_template("results.html",frame=frame,ret=ret) #######

@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/capture')
def capture():
    return render_template('capture.html')


@app.route('/recogntion')
def recogntion():
    return render_template('recogntion.html')


@app.route('/video_feed', methods=['GET','POST'])
def video_feed():
    return Response(ob.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/ca', methods=['GET','POST'])
def ca():
    return Response(ob.takeImages(),mimetype='multipart/x-mixed-replace; boundary=img')
  
@app.route('/tr')
def tr():
    return Response(ob.Trainimages(), mimetype='multipart/x-mixed-replace; boundary=frame')
   
      
@app.route('/re')
def re():
    return Response(ob.recognize_attendence(), mimetype='multipart/x-mixed-replace; boundary=frame')
# Start App
if __name__ == '__main__':
    app.run()
    app.run(host='10.10.20.233', port=8088)

