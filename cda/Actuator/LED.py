from gpiozero import PWMLED 
from time import sleep

red = PWMLED(26)
green = PWMLED(19)
blue = PWMLED(13)

while(True):
    red.pulse(3, 5)    # 8-second total cycle
    green.pulse(4, 7)  # 11-second total cycle
    blue.pulse(5, 3)
    sleep(30)   # 8-second total cycle
