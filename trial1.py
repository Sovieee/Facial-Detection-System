import face_recognition
import cv2
import numpy as np
import csv
import os
#import glob
from datetime import datetime
import numpy
import serial
import time
import getch



SERIAL_PORT = 'COM8'  # Change this to your Arduino's serial port
BAUD_RATE = 9600

PIN_FACE_DETECTED = 13
PIN_RED_LIGHT = 12

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow time for Arduino to initialize

video_capture = cv2.VideoCapture(0)


ratan_tata_image = face_recognition.load_image_file(r"D:\pythonattendancesystem\sampleImages\ratan.jpeg")
ratan_tata_encoding= face_recognition.face_encodings(ratan_tata_image)[0]

emily_clarke_image = face_recognition.load_image_file(r"D:\pythonattendancesystem\sampleImages\emily.jpeg")
emily_clarke_encoding = face_recognition.face_encodings(emily_clarke_image)[0]

#tinku_kumar_image = face_recognition.load_image_file(r"D:\pythonattendancesystem\sampleImages\WhatsApp Image 2024-04-24 at 1.24.05 AM.jpeg")
#tinku_kumar_encoding = face_recognition.face_encodings(tinku_kumar_image)[0]

honey_singh_image = face_recognition.load_image_file(r"D:\pythonattendancesystem\sampleImages\honey.jpeg")
honey_singh_encoding = face_recognition.face_encodings(honey_singh_image)[0]

shrutika_girhe_image = face_recognition.load_image_file(r"D:\pythonattendancesystem\sampleImages\WhatsApp Image 2024-04-24 at 3.28.56 PM.jpeg")
shrutika_girhe_encoding= face_recognition.face_encodings(shrutika_girhe_image)[0]


known_face_encoding = [
    
    ratan_tata_encoding,
    emily_clarke_encoding,
    #tinku_kumar_encoding,
    honey_singh_encoding,
    #shrutika_girhe_encoding
]

known_faces_names = [
    
    "ratan_tata",
    "emily_clarke",
    #"tinku_kumar",
    "honey_singh",
    #"shrutika_girhe"

]

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date+'.csv',"w+",newline = '')
#lnwriter = csv.writer(f)

while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
   # frame_process = [:, :, ::-1]
    rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])

   # rgb_small_frame = small_frame[:,:,::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)
            ser.write(bytes([PIN_RED_LIGHT]))

            if name in known_faces_names:
                if name in students:
                    #temp = name
                    students.remove(name)

                    current_time = now.strftime("%H:%M:%S")

                    print(name)
                    print(current_time)

                    if len(name) > 0:
                        # Face detected, send data to pin 13
                        ser.write(bytes([PIN_FACE_DETECTED]))
                        time.sleep(3)
                        #char = getch.getch()
                        
                        #print("Face Detected")
                   # else:
                        # No face detected, send data to pin 12
                        #ser.write(bytes([PIN_RED_LIGHT]))
                        #print("No Face Detected")
                    
                    lnwriter = csv.writer(f)
                    lnwriter.writerow([name,current_time]) 

    
    cv2.imshow("attendance system",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



video_capture.release()
cv2.destroyAllWindows()
f.close()
