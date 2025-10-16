from lcd1602 import LCD1602
from machine import I2C,ADC, Pin, PWM
from utime import sleep
from dht20 import DHT20

A4 = 440
C5 = 523
E5 = 659

LED = Pin(18, Pin.OUT)
pot = ADC(0)
buzzer = PWM(Pin(27))
buzzer.freq(440)

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
i2c2 = I2C(1)
lcd = LCD1602(i2c, 2, 16) 
dht20 = DHT20(i2c2)
lcd.display() 

while True:
    ambient = dht20.dht20_temperature()
    potvalue = pot.read_u16()
    ratio = potvalue / 65535
    set_temp = round(15 + ratio * 20, 1)

    if ambient is not None and ambient > set_temp and ambient <= set_temp + 3:
        buzzer.duty_u16(0)
        lcd.clear()
        lcd.setCursor(0,0)
        lcd.print("Set: {:.1f}C".format(set_temp))
        lcd.setCursor(0,1)
        lcd.print("Ambient: {:.1f}C".format(ambient))
        if LED.value() == 0:
            LED.value(1)
        else:
            LED.value(0)    
        sleep(1)

        
    elif ambient is not None and ambient > set_temp + 3:
        lcd.clear()
        lcd.setCursor(0,0)
        lcd.print("ALARM")
        lcd.setCursor(0,1)
        lcd.print("Set:{:.1f} Amb:{:.1f}".format(set_temp, ambient))
        LED.value(1)
        buzzer.freq(A4)
        buzzer.duty_u16(32768)
        sleep(0.25)
        LED.value(0)
        buzzer.freq(C5)
        buzzer.duty_u16(32768)
        sleep(0.25)
        LED.value(1)
        buzzer.freq(E5)
        buzzer.duty_u16(32768)
        sleep(0.25)
        LED.value(0)
        buzzer.duty_u16(0)
        sleep(0.25) 
 

    else:
        buzzer.duty_u16(0)
        lcd.clear()
        lcd.setCursor(0,0)
        lcd.print("Set: {:.1f}C".format(set_temp))
        lcd.setCursor(0,1)
        if ambient is None:
            lcd.print("Ambient: N/A")
        else:
            lcd.print("Ambient: {:.1f}C".format(ambient)) 
     