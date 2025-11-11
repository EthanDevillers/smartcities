from machine import Pin, PWM

class SERVO :
    def __init__(self, pin):
        self.pin = pin 
        self.pwm = PWM(self.pin)

    def turn(self,val):
        self.pwm.freq(100)
        self.pwm.duty_u16(int(val/180*13000+4000))
        
    def hour(self, hour):
        # Dictionnaire des heures et leurs angles correspondants
        hour_angles = {
            0: 0, 1: 15, 2: 30, 3: 45,
            4: 60, 5: 75, 6: 90,
            7: 105, 8: 120, 9: 135, 
            10: 150, 11: 165, 12: 180
        }
        
        # Vérifier si l'heure est valide (entre 1 et 12)
        if hour < 0 or hour > 12:
            print("Erreur: L'heure doit être entre 1 et 12")
            return
            
        # Tourner le servo à l'angle correspondant à l'heure
        angle = hour_angles[hour]
        self.turn(angle)