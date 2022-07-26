import requests
import serial

ser = serial.Serial('COM7', 9600)
ser.flush()



while True:
    r = requests.get('http://smart.smarthomesecuritysytem.online/getlampstatus.php')

    # print(r.text)
    statuslamp = str(r.text)
    print(statuslamp)
    if statuslamp == 'lampon':
        ser.write(b"lampon\n")
    elif statuslamp == 'lampoff':
        ser.write(b"lampoff\n")
            