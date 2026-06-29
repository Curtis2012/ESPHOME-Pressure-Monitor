# ESPHome Pressure Monitor

ESPHome firmware for a simple water pressure monitor that reports to Home Assistant through MQTT.

## Features

- ESP8266 (NodeMCU Amica) pressure monitor
- MQTT only (no native Home Assistant API)
- Configurable Wi-Fi, MQTT, sensor pin, and update interval
- Runtime calibration controls exposed to Home Assistant

## Project Files

- `pressure-monitor.yaml`: Main ESPHome firmware config
- `secrets.example.yaml`: Example secrets file template
- `docs/CALIBRATION.md`: Calibration workflow

## Quick Start

1. Install ESPHome (choose one)

```powershell
pip install esphome
```

2. Copy secrets template and fill in values

```powershell
Copy-Item secrets.example.yaml secrets.yaml
```

3. Validate config

```powershell
esphome config pressure-monitor.yaml
```

4. Compile firmware

```powershell
esphome compile pressure-monitor.yaml
```

5. Flash over USB

```powershell
esphome run pressure-monitor.yaml
```

6. Monitor logs

```powershell
esphome logs pressure-monitor.yaml
```

## Notes

- This configuration is set for ESP8266 NodeMCU (`nodemcuv2`).
- Default pressure input is `A0`.
- ESP8266 ADC input range depends on board design. Verify your NodeMCU A0 maximum input and ensure your transducer output is scaled safely.
- MQTT discovery is enabled so Home Assistant can auto-discover entities.
