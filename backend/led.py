import RPi.GPIO as GPIO
import time


class LED():
    def __init__(self, R_pin, G_pin, B_pin, pwm_frequency) -> None:
        self.pins = [R_pin, G_pin, B_pin]
        # configured pins after PWM
        self.conf_pins = []
        # frequency for pulse-width modulation
        self.f_pwm = pwm_frequency # in Hz
        # the current pwm dutycycle
        self.duty = 0

    def setup(self):
        # address pins via GPIO number 
        GPIO.setmode(GPIO.BCM)

        # configure all pins as output pins and set PWM frequency
        for idx in range(len(self.pins)):
            GPIO.setup(self.pins[idx], GPIO.OUT)
            self.conf_pins.append(GPIO.PWM(self.pins[idx], self.f_pwm))
            # start PWM
            self.conf_pins[idx].start(0)
    
    def set_duty_cycle(self, duty):
        for pin in self.conf_pins:
            pin.ChangeDutyCycle(duty)

    def on(self, brightness):
        print(f"Setting duty cycle to: {brightness}")
        self.set_duty_cycle(brightness)

    def off(self):
        print(f"Turn off LED")
        self.set_duty_cycle(0)
    
    def dim_on(self, max_brightness, dt):
        for i in range(max_brightness):
            self.duty = round(i)
            self.on(self.duty)
            time.sleep(dt)

    def dim_off(self, dt):
        for i in range(self.duty):
            self.duty-=1
            self.on(self.duty)
            time.sleep(dt)



# initialize pin GPIO numbers
# define the used pins for the light bulbs
rgb_pins = (17, 22, 24) 

pwm_frequency = 50 # in Hz

led = LED(*rgb_pins, pwm_frequency)    

led.setup()
led.dim_on(10, 0.1)
led.dim_off(0.1)
