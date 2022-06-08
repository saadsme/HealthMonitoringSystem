# HealthMonitoringSystem
This project is a health monitoring system that measures blood oxygen levels and body temperature level, using a Raspberry Pi and sensors. 

This system has the following technical specifications:
  - Ultrasonic Sensor
  - Potentiometers - x2
  - Raspberry Pi Camera
  - 16x2 LCD Screen
  - RFID Sensors - for authentication
  - PCF8591 - Analog to digital convertor (ADC)
  - Buzzer

The Pi uploads the data obtained on the could using the ThingSpeak API. This data can then be viewed on ThingSpeak.

Additionally, the data is also uploaded to a web server using Flask, which utilizes a number of static and dynamic flask routes to show the data.


