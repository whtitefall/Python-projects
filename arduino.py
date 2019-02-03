import serial

arduino = serial.Serial('com3', 9600)

while True:

    a = input('type: ').encode()
    if a == 'q'.encode():
        break
    arduino.write(a)
