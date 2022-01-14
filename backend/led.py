import RPi.GPIO as GPIO
import time


class LED():
    def __init__(self, R_pin, G_pin, B_pin, pwm_frequency):
        """
        Uses pin values for r, g and b pin to control the LED strip.
        The pwm_frequency determmines how fast the color updates are.
        """
        # The GPIO pins in the order of Red, Green, Blue
        self.pins = [R_pin, G_pin, B_pin]
        # how much each color is weighted; is used to create colors
        self.color_weights = [1, 1, 1]
        # configured pins after PWM
        self.conf_pins = []
        # frequency for pulse-width modulation
        self.f_pwm = pwm_frequency # in Hz
        # the current pwm dutycycle
        self.duty = 0

    def setup(self):
        """
        Sets the pins up for output and sets the PWM frequency.
        """
        # address pins via GPIO number 
        GPIO.setmode(GPIO.BCM)

        # configure all pins as output pins and set PWM frequency
        for idx in range(len(self.pins)):
            GPIO.setup(self.pins[idx], GPIO.OUT)
            self.conf_pins.append(GPIO.PWM(self.pins[idx], self.f_pwm))
            # start PWM
            self.conf_pins[idx].start(0)
    
    def set_duty_cycle(self, duty):
        """
        The duty cycle determines the brightness of the light.
        It can be a value between 0 and 100.
        """
        for idx in range(len(self.pins)):
            # multiply R,G,B with their weights to produce different colors
            weighted_duty = round(self.color_weights[idx]*duty)
            self.conf_pins[idx].ChangeDutyCycle(weighted_duty)
    
    def clip(self, var, lower, upper):
        """
        Determines if the variable 'var' is inside the interval [lower, upper].
        If it isn't inside the interval it will be set to the upper or lower boundary, 
        depending on which is nearer.
        """
        # clip a value into the range [lower, upper]
        if var < lower:
            var = lower
        elif var > upper:
            var = upper
        # if it is not to high and not to low, just return the variable
        return var

    def on(self, brightness):
        """
        Turns the light on immediately and sets it to the 'brightness' level.
        Brightness can be in the intervall [0, 100]
        """
        brightness = self.clip(brightness, 0, 100)
        print(f"Setting duty cycle to: {brightness}")
        self.set_duty_cycle(brightness)

    def off(self):
        """
        Turns the light off immediately.
        """
        print(f"Turn off LED")
        self.set_duty_cycle(0)
    
    def dim_on(self, max_brightness, dt):
        """
        Turns the light on with a dimming effect.
        It will set the light to 'max_brightness' over the duration 'dt'
        
        E.g. If 'dt' is 3 it will take 3 seconds to reach the specified 'max_brightness'
        """
        # only change brightness if the light will get brighter by it
        if max_brightness <= self.duty or not isinstance(max_brightness, int):
            return

        # clip max_brightness into [0, 100]
        max_brightness = self.clip(max_brightness, 0, 100)
        
        # calculate the pause between the dimming steps
        steps = max_brightness - self.duty 
        pause = dt/steps #steps cannot be zero, due to the guard clause in the beginning of the function

        for i in range(max_brightness):
            self.duty = round(i)
            self.on(self.duty)
            time.sleep(pause)

    def dim_off(self, dt):
        """
        It will turn off the light over the duration of 'dt'.
        """
        steps = self.duty
        pause = dt/steps

        for _ in range(self.duty):
            self.duty-=1
            self.on(self.duty)
            time.sleep(pause)
    
    def set_color(self, rgb_weights):
        """
        Sets the color of the LED to provided r,g,b values.
        rgb_weights can either be a list/tuple of three percentage values [0, 1]
        or a list/tuple of three rgb values [0, 255]
        """
        # if all values in rgb_weighs are integers
        if isinstance(all(rgb_weights), int) and len(rgb_weights) == 3:
            # this means the values are in range [0, 255]
            # we need to convert them to percentage values
            for idx in range(len(rgb_weights)):
                # make sure values are valid
                rgb_val = self.clip(rgb_weights[idx], 0, 255)
                weight = float(rgb_val / 255)
                self.color_weights[idx] = weight
        
        # if all values in rgb_weights are floats
        elif isinstance(all(rgb_weights), float) and len(rgb_weights) == 3:
            # this means the values are in range [0.0, 1.0]
            # they don't have to be converted
            for idx in range(len(rgb_weights)):
                # make sure values are valid
                weight = self.clip(rgb_weights[idx], 0.0, 1.0)
                self.color_weights[idx] = weight


if __name__ == "__main__":
    try:
        # initialize pin GPIO numbers
        # define the used pins for the light bulbs
        rgb_pins = (17, 22, 24) 

        pwm_frequency = 50 # in Hz

        led = LED(*rgb_pins, pwm_frequency)    

        led.setup()
        led.set_color([0.5, 0.2, 0.3])
        led.dim_on(10, 3)
        led.dim_off(2)

        GPIO.cleanup()
    
    except:
        GPIO.cleanup()
