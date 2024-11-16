import RPi.GPIO as GPIO
import time

# Configuration des GPIO
GPIO.setmode(GPIO.BCM)

# Définir les pins
LED_PINS = {
    "free": 17,
    "busy": 27,
    "on_air": 22,
    "hey": 23,
    "urgency": 24
}
BUTTON_PINS = {
    "on_air": 5,
    "hey": 6,
    "urgency": 13
}
SWITCH_PIN = 19  # Interrupteur pour Free/Busy

# Configurer les LED en sortie
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Configurer les boutons en entrée avec pull-down
for pin in BUTTON_PINS.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Configurer l'interrupteur en entrée avec pull-down
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Fonction pour clignoter une LED
def blink_led(pin, duration=1, interval=0.5):
    end_time = time.time() + duration
    while time.time() < end_time:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(interval)

# Boucle principale
try:
    while True:
        # Gérer Free/Busy via interrupteur
        if GPIO.input(SWITCH_PIN):
            GPIO.output(LED_PINS["free"], GPIO.LOW)
            GPIO.output(LED_PINS["busy"], GPIO.HIGH)
        else:
            GPIO.output(LED_PINS["busy"], GPIO.LOW)
            GPIO.output(LED_PINS["free"], GPIO.HIGH)

        # Vérifier le bouton On Air
        if GPIO.input(BUTTON_PINS["on_air"]):
            GPIO.output(LED_PINS["on_air"], GPIO.HIGH)
        else:
            GPIO.output(LED_PINS["on_air"], GPIO.LOW)

        # Vérifier le bouton Hey!
        if GPIO.input(BUTTON_PINS["hey"]):
            GPIO.output(LED_PINS["hey"], GPIO.HIGH)
        else:
            GPIO.output(LED_PINS["hey"], GPIO.LOW)

        # Vérifier le bouton Urgency!
        if GPIO.input(BUTTON_PINS["urgency"]):
            blink_led(LED_PINS["urgency"], duration=3)  # Clignote pendant 3 secondes

        time.sleep(0.1)  # Petite pause pour éviter la surcharge CPU

except KeyboardInterrupt:
    print("Arrêt du programme")
    GPIO.cleanup()
