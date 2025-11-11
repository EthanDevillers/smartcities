from machine import Pin
from utime import sleep
import network
import ntptime
from servo import SERVO
import time

# Configuration WiFi
ssid = 'nom du wifi'
password = 'mdp du wifi'

# Fuseau horaire en heures (+1 pour CET)
TIMEZONE_OFFSET = 1

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Connexion au WiFi...")
    
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        # Attente de la connexion
        while not wlan.isconnected():
            sleep(1)
    
    print("Connecté au WiFi!")
    print(wlan.ifconfig())

def get_current_hour():
    try:
        ntptime.settime()
        current_time = time.localtime()
        hour = current_time[3]
        hour = (hour + TIMEZONE_OFFSET) % 24	
        # Convertir en format 12h
        if hour > 12:
            hour -= 12
        elif hour == 0:
            hour = 12
        return hour
    except:
        print("Erreur de synchronisation de l'heure")
        return None

# Initialisation du servo
servo = SERVO(Pin(20))

# Connexion WiFi
connect_wifi()

# Boucle principale
while True:
    hour = get_current_hour()
    if hour:
        print(f"Heure actuelle: {hour}h")
        servo.hour(hour)  
    sleep(60)  # Mise à jour toutes les minutes