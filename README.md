# Pipboy-3000
 Python code recycled and forked to create a UI for a raspi TFT 3.5" using the ytech pipboy.
 




Sources:
- Code base: https://github.com/sabas1080/pypboy
- 3d Model: https://ytec3d.com/pip-boy/
- Electrical diagram: https://learn.adafruit.com/raspberry-pi-pipboy-3000/circuit-diagram
  - (*does not include wiring for front three LEDs*)
![](./Finished_product_Images/PiTFT_Touchscreen_pinout.png) 
  - Red are LED pins
    - ![](./Finished_product_Images/IMG_1663.jpg)
    - **Each** LED needs a 330ohm resistor, I used some cheap PCB and had my friend wired the LEDs and resistors onto to save space.
  - Black are Rotary encoder pins
    - The rotary set with three gpio with be the non-scroll wheel button.