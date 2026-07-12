# Calibration Guide

This project uses the formula below to convert voltage to pressure:

psi = ((voltage - zero_voltage) * psi_per_volt) * pressure_scale + pressure_offset

Runtime calibration values are exposed to Home Assistant as `number` entities through MQTT discovery.

## Typical Sensor Model

Many pressure transducers output 0.5V to 4.5V across full scale.

If your sensor range is 0-100 psi, then:

- zero_voltage = 0.5
- psi_per_volt = 100 / (4.5 - 0.5) = 25

## Recommended Workflow

1. Vent line to known zero pressure.
2. Read `Pressure Voltage` and set `Zero Voltage` to that value.
3. Apply a known pressure reference (for example, 40 psi).
4. Adjust `PSI Per Volt` until reported pressure matches the reference.
5. Use `Pressure Offset` for small additive correction.
6. Use `Pressure Scale` for small multiplicative correction.

## Notes

- ESP8266 NodeMCU uses ADC on `A0`; confirm the allowed voltage range on your exact board before wiring the sensor.
- Keep `Pressure Scale` at 1.0 unless you need proportional correction.
- Avoid over-correcting with both slope and scale at the same time.
- Recheck calibration at low and high pressure points.

## Example Calibration

If a gauge shows 70 PSI while Home Assistant shows 83.86 PSI, use:

- pressure_scale = 70 / 83.86 = 0.835
- new pressure_scale = 6.967 × 0.835 = 5.816

That correction is proportional, so it is the right first adjustment when the error tracks the entire range.
