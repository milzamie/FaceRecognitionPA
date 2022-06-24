from ctypes.wintypes import RGB
import cv2, os, numpy as np
from PIL import Image

wajahDir = 'datawajah'
latihDir = 'latihwajah'
cam = cv2.VideoCapture(0)
cam.set(3, 640)#ubah lebar cam
cam.set(4, 480)#ubah tinggi cam
faceDetector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyeDetector = cv2.CascadeClassifier('haarcascade_eye.xml')
faceID = input("Masukkan Face ID yang akan Direkam Datanya [kemudian tekan Enter]: ")
print ("Tatap wajah Anda ke dalam webcam. Tunggu proses pengambilan data wajah selesai..")
ambilData = 1

while True:
    retV, frame = cam.read()
    abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(abuAbu, 1.3, 5)#frame, scaleFactor,
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        namaFile = 'wajah.'+str(faceID)+'.'+str(ambilData)+'.jpg'
        cv2.imwrite(wajahDir+'/'+namaFile,frame)
        ambilData += 1 
        roiAbuAbu = abuAbu[y:y+h,x:x+w]
        roiWarna = frame[y:y+h,x:x+w]
        eyes = eyeDetector.detectMultiScale(roiAbuAbu)
        for (xe,ye,we,he) in eyes:
            cv2.rectangle(roiWarna,(xe,ye),(xe+we,ye+he),(100,150,250),1)
    cv2.imshow('Webcamku', frame)
    #cv2.imshow('Webcamku - Grey', abuAbu)
    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == ord('q'):
        break
    elif ambilData>=100:
        break
print("Pengambilan data selesai")
cam.release()
cv2.destroyAllWindows()

latihDir = 'latihwajah'
def getImageLabel(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples = []
    faceIDs = []
    for imagePath in imagePaths:
        PILImg = Image.open(imagePath).convert('L')#convert kedalam gray
        imgNum = np.array(PILImg,'uint8')
        faceID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = faceDetector.detectMultiScale(imgNum)
        for (x,y,w,h) in faces:
            faceSamples.append(imgNum[y:y+h,x:x+w])
            faceIDs.append(faceID)
    return faceSamples, faceIDs
    
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

print("Mesin sedang melakukan training data wajah. Tunggu dalam beberapa detik.")
faces, IDs = getImageLabel(wajahDir)
faceRecognizer.train(faces,np.array(IDs))

faceRecognizer.write(latihDir+'/training.xml')
print("Sebanyak {0} data wajah telah di trainingkan ke mesin",format(len(np.unique(IDs))))