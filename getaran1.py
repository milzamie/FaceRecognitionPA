import serial
import requests
import time

ser = serial.Serial('/dev/ttyACM0',9600)
ser.flush()
#start_time = time.time()
while True:
    #print (time.time()-start_time, "detik")
    if ser.in_waiting > 0:
        read_serial=ser.readline().decode('utf-8').rstrip()
        trill = float(read_serial)
        if read_serial.strip()!= 'x':
            response = requests.post('url', json = {'in_current_value' : read_serial})
            print (read_serial)