# publisher.py, UNO R4 route (runs on the Pi)
import time
import paho.mqtt.client as mqtt
from pyfirmata2 import Arduino
import config

TOPIC = f"vanier/iot/{config.STATION}/light"

board = Arduino(Arduino.AUTODETECT)
board.samplingOn(1000) # one reading per second

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(config.BROKER_IP, 1883, 60)
client.loop_start()

def on_light(value):
	if value is not None:
		client.publish(TOPIC, f"{value:.3f}")
		print("sent", round(value, 3))

board.analog[0].register_callback(on_light)
board.analog[0].enable_reporting()

try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	client.loop_stop()
	board.exit()
