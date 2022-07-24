import mysql.connector
import serial
# import time

ser = serial.Serial('COM7',9600, timeout=1)
ser.flush()
    
mydb = mysql.connector.connect(
    host="localhost",
    user="smax9947_smartdoorlock",
    password="alexprojek123",
    database="padb"
)

mycursor = mydb.cursor()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        trill = float(line)
        sql = "INSERT INTO trillstatus(nilai) VALUES(%s)" %(trill)
        mycursor.execute(sql)
        mydb.commit()
        
        print(trill, "inserted.")
        # time.sleep(1)