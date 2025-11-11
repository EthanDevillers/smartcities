from machine import Pin 
from utime import sleep
import network
import ntptime
from servo import SERVO
import time
# Config WiFi
ssid = 'extension salon'
password = 'Fanfan2112'

# Fuseaux horaires disponibles
TIMEZONES = {
    0: ('UTC (Londres)', 0),     
    1: ('UTC+1 (Bruxelles)', 1),  
    2: ('UTC+9 (Tokyo)', 9),   
    3: ('UTC-5 (New York)', -5),   
    4: ('UTC-8 (Los Angeles)', -8),  
}

current_timezone_index = 1  # Par défaut à UTC+1 (Buxelles, Paris)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Connexion au WiFi...")
    
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        # Attente de la connexion
        while not wlan.isconnected():
            sleep(1)
    
    print("Connection au WiFi faites !")
    print(wlan.ifconfig())

def get_current_hour(timezone_offset):
    try:
        ntptime.settime()
        current_time = time.localtime()
        hour = current_time[3]
        # Appliquer le fuseau horaire
        hour = (hour + timezone_offset) % 24
        # Convertir en format 12h
        if hour > 12:
            hour -= 12
        elif hour == 0:
            hour = 12
        return hour
    except Exception as e:
        print("Erreur de synchronisation de l'heure:", e)
        return None

def button(pin):
    global current_timezone_index
    # Délai anti-rebond 
    sleep(0.1)
    # Changer le fuseau horaire au prochain appui
    current_timezone_index = (current_timezone_index + 1) % len(TIMEZONES)
    name, offset = TIMEZONES[current_timezone_index]
    print(f"Nouveau fuseau horaire : {name}")


# Initialisation du servo et du bouton
servo = SERVO(Pin(20))
BUTTON = Pin(16, Pin.IN,Pin.PULL_DOWN)
BUTTON.irq(trigger=Pin.IRQ_RISING, handler=button)
# Connexion WiFi
connect_wifi()
# Boucle principale
while True:
        name, offset = TIMEZONES[current_timezone_index]
        hour = get_current_hour(offset)
        
        if hour:
            print(f"Fuseau: {name} | Heure actuelle: {hour}h")
            servo.hour(hour)
        else:
            print("Heure non disponible, nouvelle tentative dans 60s...")
        
        sleep(60)  # Mise à jour toutes les minutes