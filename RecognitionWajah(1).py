import cv2, os, numpy as np
import serial
import time

serialcomm = serial.Serial('COM7',9600)
serialcomm.timeout = 1
wajahDir = 'datawajah'
latihDir = 'latihwajah'
cam = cv2.VideoCapture(0)
cam.set(3, 640)#ubah lebar cam
cam.set(4, 480)#ubah tinggi cam
faceDetector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

faceRecognizer.read(latihDir+'/training.xml')
font = cv2.FONT_HERSHEY_SIMPLEX

id = 0
names = ['Tidak Diketahui','Milzam','Ilham','Anggi','Ayah','Kiki','Ilma','Mamah']

minWidth = 0.1*cam.get(3)
minHeight = 0.1*cam.get(4)

while True:
    retV, frame = cam.read()
    frame = cv2.flip(frame, 1)#vertical flip
    abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(abuAbu, 1.2, 5,minSize=(round(minWidth),round(minHeight)),)#frame, scaleFactor, minNeighbors
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        id, confidence = faceRecognizer.predict(abuAbu[y:y+h,x:x+w]) # confidence = 0 artinya cocok sempurna
        if confidence<=45 :
            nameID = names[id]
            confidenceTxt = "{0}%".format(round(100-confidence))
            i = 'on'
            serialcomm.write(i.encode())
            time.sleep(1)
            print(serialcomm.readline().decode('ascii'))
            
        else :
            nameID = names[0]
            confidenceTxt = "{0}%".format(round(100-confidence))
            i = 'off'
            serialcomm.write(i.encode())
            time.sleep(1)
            print(serialcomm.readline().decode('ascii'))
        cv2.putText(frame,str(nameID),(x+5,y-5),font,1,(255,100,0),2)
        cv2.putText(frame,str(confidenceTxt),(x+5,y+h-5),font,1,(255,255,0),1)
    cv2.imshow('Recognition', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == ord('q'):
        
        break
print("EXIT")
serialcomm.close()
cam.release()
cv2.destroyAllWindows()