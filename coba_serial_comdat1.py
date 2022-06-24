import serial
import time

serialcomm = serial.Serial('COM7',9600)
time.sleep(2)

while True:
    data = input()
    if data == 'done':
        print ('finished program')
        break
    if data == '1':
        serialcomm.write(b'1')
        print("LED hidup")
    if data == '0':
        serialcomm.write(b'0')
        print("LED mati")  
