import RPi.GPIO as GPIO
import urllib.request
import LCD1602 as LCD
from flask import Flask
import PCF8591 as ADC 
import serial
import time
from flask import send_file
from datetime import datetime
from picamera import PiCamera
GPIO.setwarnings(False)
ADC.setup(0x48)

#TODO default and static
app= Flask(__name__)
    
@app.route('/')
def index():
    return "Welcome to the health monitoring system!"
#Static route (Heart rate)
@app.route('/HR')
def Hrate():
    ADC_units = ADC.read(2)
    ADC_volts = (ADC_units * 3.3) / 256
    ADC_HR = (ADC_volts * 240) / 3.3
    
    buf='Heart rate is=%f'%(ADC_HR)
    return buf
#Static route (Oxygen Level)
@app.route('/OL')
def OXlevel():
    ADC_units = ADC.read(1)
    ADC_volts = (ADC_units * 3.3) / 256
    ADC_OL = (ADC_volts * 100) / 3.3
    
    buf='Oxygen Level is=%f'%(ADC_OL)
    return buf
#Dynamic route (Heart Rate)
@app.route('/HR_alert/<HR>')
def HRalert(HR):
    HeartRate = float(HR) #Heart Rate
    
    ADC_units = ADC.read(2)
    ADC_volts = (ADC_units * 3.3) / 256
    ADC_HR = (ADC_volts * 240) / 3.3
    
    if ADC_HR > HeartRate:
        
            timestamp = datetime.now().isoformat()

            camera = PiCamera()
            camera.rotation = 180
            
            camera.resolution = (640,480)
            camera.annotate_text = "Picture was taken at time {}; with Heart Rate {}".format(timestamp, ADC_HR)
            
            camera.capture('/home/pi/Desktop/S22 Sec 2 THR/myPic.jpg')
            resp = send_file('/home/pi/Desktop/S22 Sec 2 THR/myPic.jpg',mimetype="image/jpg")
            return resp
        
    else:
            return ("Heart Rate is normal.")
        
    #Dynamic Route (Oxygen Level)
@app.route('/OL_alert/<OL>')
def OLalert(OL):
    OxygenLevel= float(OL) #Oxygen Level
    
    ADC_units = ADC.read(1)
    ADC_volts = (ADC_units * 3.3) / 256
    ADC_OL = (ADC_volts * 100) / 3.3
    
    if ADC_OL > OxygenLevel:
        
            timestamp = datetime.now().isoformat()

            camera = PiCamera()
            camera.rotation = 180
            
            camera.resolution = (640,480)
            camera.annotate_text = "Picture was taken at time {}; with speed {}".format(timestamp, ADC_OL)
            
            camera.start_recording('/home/pi/Desktop/S22 Sec 2 THR/myVid.h264')
            time.sleep(5)
            camera.stop_recording()
            resp = send_file('/home/pi/Desktop/S22 Sec 2 THR/myVid.h264',mimetype="video/h264")
            return resp
        
    else:
            return ("Oxygen Level is normal at %f."%(ADC_OL))
    


CH_ID=1715596
API_KEY = "AT2ZJVOAWVABC27N"

Field_No=1
Numberofreadings=10
elementnumber=3
values=[]

SERIAL_PORT = '/dev/ttyS0'


#Setting the pins
OL_led=16 #green
HR_led=12 #blue
DR_led=13 #red
IB=17
BUZZER=6
ECHO=5
TRIG=18
PB2=4 #emergency interrupt

GPIO.setmode(GPIO.BCM)
#IO Setup
GPIO.setup(HR_led,GPIO.OUT)
GPIO.setup(OL_led,GPIO.OUT)
GPIO.setup(DR_led,GPIO.OUT)
GPIO.setup(BUZZER,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
BUZZ = GPIO.PWM(BUZZER,50)
GPIO.setup(IB,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(PB2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
LCD.init(0x27,1) #0x27 is the I2C address of LCD

BUZZ.start(0) #starting PWM

flag=0
intx=0
def action(self):
  global flag
  global intx
  if flag==1:
    print("SOS signal detected. Emergency Services Dialed.")
    while 1:
        BUZZ.ChangeDutyCycle(50)
        time.sleep(0.5)
        BUZZ.ChangeDutyCycle(0)
        time.sleep(0.5)
        intx=2

GPIO.add_event_detect(PB2,GPIO.RISING,callback=action,bouncetime=2000)


#function to flash the LEDs
def flashLED(a):
  
  for i in range(0,3):
        GPIO.output(HR_led,GPIO.LOW)
        GPIO.output(DR_led,GPIO.LOW)
        GPIO.output(OL_led,GPIO.LOW)
        GPIO.output(a,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(a,GPIO.LOW)
        time.sleep(0.2)
  GPIO.output(a,GPIO.HIGH)

#function to calculate and return the distance
def distance(): 
    GPIO.output(TRIG, GPIO.LOW)  
    time.sleep(0.000002) 
    GPIO.output(TRIG, 1) 
    time.sleep(0.00001) 
    GPIO.output(TRIG, 0) 

    while GPIO.input(ECHO) == 0: 
        a = 0                                           
    time1 = time.time()                         
    while GPIO.input(ECHO) == 1: 
        a = 0                                                   
    time2 = time.time()                         
    duration = time2 - time1 
    return duration*1000000/58    

#setting the pins for the keypad
GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(23, GPIO.OUT) 
GPIO.setup(24, GPIO.OUT) 
GPIO.setup(25, GPIO.OUT) 
GPIO.setup(26, GPIO.OUT)

def keypad(): 
    while(True): 

        GPIO.output(26, GPIO.LOW)
        GPIO.output(25, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)

        if (GPIO.input(22)==0):
            return(1,"!")
            break

        if (GPIO.input(21)==0):
            return(4,"$")
            break

        if (GPIO.input(20)==0):
            return(7,"&")
            break

        if (GPIO.input(19)==0):
            return(0xE)
            break

        GPIO.output(26, GPIO.HIGH)
        GPIO.output(25, GPIO.LOW)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)

        if (GPIO.input(22)==0):
            return(2,"@")
            break

        if (GPIO.input(21)==0):
            return(5,"%")
            break

        if (GPIO.input(20)==0):
            return(8,"*")
            break
 
        if (GPIO.input(19)==0):
            return(0,")")
            break


        GPIO.output(26, GPIO.HIGH)
        GPIO.output(25, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)

        if (GPIO.input(22)==0):
            return(3,"#")
            break

        if (GPIO.input(21)==0):
            return(6,"^")
            break
        #Scan row 2
        if (GPIO.input(20)==0):
            return(9,"(")
            break
 
        if (GPIO.input(19)==0):
            return(0XF)
            break

        GPIO.output(26, GPIO.HIGH)
        GPIO.output(25, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)

        if (GPIO.input(22)==0):
            return(0XA)
            break

        if (GPIO.input(21)==0):
            return(0XB)
            break

        if (GPIO.input(20)==0):
            return(0XC)
            break

        if (GPIO.input(19)==0):
            return(0XD)
            break
          
def validate_rfid(code):
    s = code.decode("ascii")
    if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
        return s[1:-1]
    else:
        return False

ser = serial.Serial(baudrate = 2400,  bytesize = serial.EIGHTBITS,  parity = serial.PARITY_NONE,  port = SERIAL_PORT, stopbits = serial.STOPBITS_ONE,  timeout = 1)



#Running the program

#password checking

password="67"
print("Login to system: ")
while(True):
    key1,key1s = keypad();
    
    if(GPIO.input(IB)==1):
      key1=key1s
    else:
      key1 = key1
    time.sleep(1)
    key2,key2s = keypad();
    
    if(GPIO.input(IB)==1):
      key2=key2s
    else:
      key2 = key2
    time.sleep(1)
    
    keyf=str(key1) + str(key2)
    if (keyf!=password):
      print("wrong password. re-enter password!")
    else:
      break


#starting program
print("Start health monitoring system.")
LCD.write(1,0,"Start System!")
while (GPIO.input(IB)==0):
    w=0 
print("System ON: ", time.ctime())
x=""
code=False



while True:
    flag=0
    z=input("Select Flask or TS: F or T") #user input for flask or thingspeak
    if(z=="F" or z=="f"):   #if flask
        if __name__ == '__main__':
            app.run(host='0.0.0.0', port=5070)
    elif(z=="T" or z=="t"): #if thingspeak
        
        LCD.clear()
        LCD.write(3,1,"Select mode")
        y=input("Select input mode: R or K") ##user input for RFID or Keyboard
        if(y=="K" or y=="k"): #if keyboard is selected
          x=input("Select aspect to measure: Heart Rate (H) or Blood-Oxygen Level (O) or Both {Thingspeak} (D)") #asking input for which thing to measure
        elif(y=="R" or y=="r"): #if RFID is chosen
          while (code==False):
            #scanning RFID
            #while keeping looping until RFID is scanned
            print(code)
            print("Scan Tag")
            data = ser.read(12)
            code = validate_rfid(data)

        if(x=="H" or x=="h" or code == "5400653CCF"): #Heart Rate, Square Card
            
            flag=0
            flashLED(HR_led)
            print("Measurement of Heart Rate taken at time:",time.ctime())
            
            while True:
              print("Reading Heart Rate...")
              dist=distance()
              #print("Distance = ",dist,"cm")
              time.sleep(0.25)
              if(dist>50):
                  BUZZ.ChangeDutyCycle(50)
                  print("Bring your finger closer!")
              else:
                  BUZZ.ChangeDutyCycle(0)
                  ADC_units = ADC.read(2) #reading from second potentiometer
                  ADC_volts = (ADC_units * 3.3) / 256
                  ADC_BPM = (ADC_volts * 240) / 3.3
                  ADC.write(ADC_units) #final heart rate value
                  print("ADC Heart Rate = {0:2.2f} BPM".format(ADC_BPM))
                  if(ADC_BPM>120 or ADC_BPM<55): #check for abnormalities
                      print("Heart rate abnormal. Seek help.")
                  else:
                      print("Heart rate normal. Stay safe.")
            
                  #printing heart rate on LCD    
                  LCD.clear()
                  LCD.write(3,0,"Heart Rate:")
                  LCD.write(3,1, "{0:2.2f} BPM".format(ADC_BPM))
                  time.sleep(3) #sleeping to avoid spam readings
                  flag =1
                  
                  if intx==2:
                       while True:
                           a=0       
              
             # print ("intx{}".format(intx))
              

        elif(x=="O" or x=="o" or code == "46003BB194"): #oxygen level
            
         flag=0
         flashLED(OL_led)
         print("Measurement of Oxygen Level taken at time:",time.ctime())
         #if potentiometer is selected
         while True:
              print("Reading Oxygen Level...")
              dist=distance()
              #print("Distance = ",dist,"cm")
              time.sleep(0.25)
              if(dist>50):
                  BUZZ.ChangeDutyCycle(50)
                  print("Bring your finger closer!")
              else:
                  BUZZ.ChangeDutyCycle(0) 
                  ADC_units = ADC.read(1) #reading from first potentiometer
                  ADC_volts = (ADC_units * 3.3) / 256
                  ADC_SpO2 = (ADC_volts * 100) / 3.3
                  ADC.write(ADC_units) #final oxygen level value
                  print("ADC Oxygen Level = {0:2.2f} %".format(ADC_SpO2))
                  if(ADC_SpO2<95): #check for abnormalities
                      print("Oxygen Level abnormal. Seek help.")
                      #TODO add camera stuff
                  else:
                      print("Oxygen Level normal. You are healthy!")
                  #printing oxygen level on LCD    
                  LCD.clear()
                  LCD.write(2,0,"Oxygen Level:")
                  LCD.write(3,1, "{0:2.2f} % SpO2".format(ADC_SpO2))
                  time.sleep(3) #sleeping to avoid spam readings
                  flag =1
                  if intx==2:
                       while True:
                           a=0
                  
              
            
        elif(x=="D" or x=="d" or code == "12006B0517"):
            x="D"
            while True:
                        x = urllib.request.urlopen("https://api.thingspeak.com/channels/{}/fields/{}.csv?results={}".format(CH_ID, Field_No, Numberofreadings))
                        data = x.read().decode("ascii")
                        print(data)
   
                        ADC_units = ADC.read(1)
                        ADC_volts = (ADC_units * 3.3) / 256
                        ADC_OL = (ADC_volts * 100) / 3.3
                        ADC.write(ADC_units)
                        
                        ADC_units2 = ADC.read(2)
                        ADC_volts2 = (ADC_units * 3.3) / 256
                        ADC_HR = (ADC_volts * 240) / 3.3
                        ADC.write(ADC_units2)
                        
                        print("Oxygen Levels = {0:2.2f} ".format(ADC_OL))
                        print("Heart Rate = {0:2.2f} ".format(ADC_HR))
                        y = urllib.request.urlopen("https://api.thingspeak.com/update?api_key={}&field1={}&field2={}".format(API_KEY, ADC_OL, ADC_HR))
                        
                        LCD.clear()
                        LCD.write(0,0, "OX = {0:2.2f}".format(ADC_OL))
                        LCD.write(0,1, "HR = {0:2.2f}".format(ADC_HR))
                        time.sleep(1)
                        flag=1
                        if intx==2:
                         while True:
                           a=0
