from gpiozero import PWMLED 
from time import sleep

red = PWMLED(26)
green = PWMLED(19)
blue = PWMLED(13)

while(True):
    red.pulse(15,30,50)
    green.pulse(20,25,50)
    blue.pulse(25,20,50)
