from gpiozero import PWMLED 
from time import sleep

red = PWMLED(26)
green = PWMLED(19)
blue = PWMLED(13)

red.pulse(0.5,3)
green.pulse(1,1.5)
blue.pulse(1.5,.75)