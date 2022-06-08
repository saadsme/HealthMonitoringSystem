# HealthMonitoringSystem
This project is a health monitoring system that measures blood oxygen levels and body temperature level, using a Raspberry Pi and sensors. 

This system has the following technical specifications:
  - Ultrasonic Sensor
  - Potentiometers - x2
  - Raspberry Pi Camera

The Pi then uploads the data obtained on the could using the ThingSpeak API. This data can then be viewed on ThingSpeak.

Additionally, the data is alos uploaded to a web server using Flask, which utilizes a number of static and dynamic flask routes to show the data.


