import machine
import utime

BUTTON = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
LED = machine.Pin(18, machine.Pin.OUT)

cpt = 0
freq = 1

def animation():
    LED.value(1)
    utime.sleep(1)
    for i in range(3):
        LED.value(0)
        utime.sleep(0.1)
        LED.value(1)
        utime.sleep(0.1)
    utime.sleep(0.5)


# fonction appelée lors du front montant du bouton
def Bouton(pin):
    global cpt
    cpt += 1
    if cpt > 5:
        cpt = 0
    print("compteur =", cpt)

    if cpt ==2 or cpt ==4 or cpt ==0: 
        animation()

# configurer l'interrupt sur front montant
BUTTON.irq(trigger=machine.Pin.IRQ_RISING, handler=Bouton)

while True:
    if cpt == 0:
        LED.value(0)
    else:
        if cpt == 2:
            freq = 0.5
        elif cpt == 4:
            freq = 2
        if cpt >=2:
            LED.value(1)
            utime.sleep(1/freq/2)
            LED.value(0)
            utime.sleep(1/freq/2)
