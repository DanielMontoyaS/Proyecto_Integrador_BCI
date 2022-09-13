import RPi.GPIO as GPIO  
import time  
import signal  
import atexit  

atexit.register(GPIO.cleanup)    

GPIO.setmode(GPIO.BCM)  

# Seleccion del pin 17 
GPIO.setup(17, GPIO.OUT, initial=False)  

p = GPIO.PWM(17,50) # Frecuencia del
                    # servo 50HZ  

p.start(0)  

def Cerrado():

  p.ChangeDutyCycle(12.5) # Ubicacion en
                          # angulo de 0°
  time.sleep(0.5)


def Abierto():

  p.ChangeDutyCycle(2.5)  # Ubicacion en
                          # angulo de 180°
  time.sleep(0.5)

