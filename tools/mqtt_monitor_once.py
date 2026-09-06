import pathlib
import statistics
import time

import paho.mqtt.client as mqtt
import yaml

SECRETS_PATH = pathlib.Path("secrets.yaml")
secrets = yaml.safe_load(SECRETS_PATH.read_text(encoding="utf-8")) or {}

broker = str(secrets.get("mqtt_broker", "")).strip()
port = int(secrets.get("mqtt_port", 1883) or 1883)
username = str(secrets.get("mqtt_username", "") or "").strip()
password = str(secrets.get("mqtt_password", "") or "").strip()

pressure_topic = "water_pressure_monitor/sensor/water_pressure_monitor_pressure/state"
voltage_topic = "water_pressure_monitor/sensor/water_pressure_monitor_pressure_voltage/state"
status_topic = "water_pressure_monitor/status"

pressure_vals = []
voltage_vals = []
status_events = []
last_messages = []


def _as_float_or_none(value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def on_connect(client, userdata, flags, rc, properties=None):
    if rc != 0:
        print(f"MQTT connect failed rc={rc}")
        return
    print(f"Connected to MQTT broker {broker}:{port}")
    client.subscribe(pressure_topic)
    client.subscribe(voltage_topic)
    client.subscribe(status_topic)


def on_message(client, userdata, msg):
    payload = msg.payload.decode(errors="ignore").strip()
    ts = time.strftime("%H:%M:%S")

    last_messages.append((ts, msg.topic, payload))
    if len(last_messages) > 20:
        last_messages.pop(0)

    if msg.topic == pressure_topic:
        val = _as_float_or_none(payload)
        if val is not None:
            pressure_vals.append(val)
    elif msg.topic == voltage_topic:
        val = _as_float_or_none(payload)
        if val is not None:
            voltage_vals.append(val)
    elif msg.topic == status_topic:
        status_events.append((ts, payload))


client = mqtt.Client()
if username:
    client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_start()

observe_seconds = 45
print(f"Observing topics for {observe_seconds}s...")
end = time.time() + observe_seconds
while time.time() < end:
    time.sleep(1)

client.loop_stop()
client.disconnect()

print("\n--- Monitoring Summary ---")
if status_events:
    print("Status events:")
    for t, s in status_events[-10:]:
        print(f"  {t}  {s}")
else:
    print("Status events: none seen during window")

if pressure_vals:
    print(f"Pressure samples: {len(pressure_vals)}")
    print(f"Pressure min/max: {min(pressure_vals):.2f} / {max(pressure_vals):.2f} psi")
    print(f"Pressure avg: {statistics.fmean(pressure_vals):.2f} psi")
else:
    print("Pressure samples: none")

if voltage_vals:
    print(f"Voltage samples: {len(voltage_vals)}")
    print(f"Voltage min/max: {min(voltage_vals):.3f} / {max(voltage_vals):.3f} V")
    print(f"Voltage avg: {statistics.fmean(voltage_vals):.3f} V")
else:
    print("Voltage samples: none")

print("Recent messages:")
for t, topic, payload in last_messages:
    print(f"  {t}  {topic}  {payload}")
