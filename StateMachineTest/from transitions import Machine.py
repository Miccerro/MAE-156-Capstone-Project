from transitions import Machine

class MyApp:
    states = ['idle', 'calibration_on', 'calibration_off']

    def __init__(self):
        self.machine = Machine(model=self, states=MyApp.states, initial='idle')

    def on_enter_calibration_on(self):
        print("Entering calibration_on state")
        # Additional actions to perform when entering calibration_on state

    def on_enter_calibration_off(self):
        print("Entering calibration_off state")
        # Additional actions to perform when entering calibration_off state

# Create an instance of the state machine
app = MyApp()

# Trigger state transitions
app.to_calibration_on()
app.to_calibration_off()
