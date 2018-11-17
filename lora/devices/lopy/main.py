"""Lora module running on the Lopy v4

Copyright (C) 2018  Smart Bivouac
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA"""

import time
import pycom
import struct
import socket
import ubinascii
from network import LoRa
from machine import Pin, PWM, ADC

def temp_read():
    a = sensorAnalogPin.value()
    return a//100+2

def read_keypad():
    ko1.value(1)
    if(ki1.value() == 1):
        return "1"
    elif(ki2.value() == 1):
        return "2"
    elif(ki3.value() == 1):
        return "3"
    elif(ki4.value() == 1):
        return "A"
    ko1.value(0)
    ko2.value(1)
    if(ki1.value() == 1):
        return "4"
    elif(ki2.value() == 1):
        return "5"
    elif(ki3.value() == 1):
        return "6"
    elif(ki4.value() == 1):
        return "B"
    ko2.value(0)
    ko3.value(1)
    if(ki1.value() == 1):
        return "7"
    elif(ki2.value() == 1):
        return "8"
    elif(ki3.value() == 1):
        return "9"
    elif(ki4.value() == 1):
        return "C"
    ko3.value(0)
    ko4.value(1)
    if(ki1.value() == 1):
        return "*"
    elif(ki2.value() == 1):
        return "0"
    elif(ki3.value() == 1):
        return "#"
    elif(ki4.value() == 1):
        return "D"
    ko4.value(0)
    return "None"

def acquire_code():
    pycom.rgbled(0x007f00)
    time_start = time.time()
    n = 0
    code = ""
    reset = False
    while(n<4 and time.time()-time_start<10):
        k = read_keypad()
        if k != "None":
            if reset:
                code+=k
                reset = False
                n+=1
        else:
            reset = True
    if n<4:
        pycom.rgbled(0x7f0000)
        time.sleep(1)
    pycom.rgbled(0x000000)
    return code


pycom.heartbeat(False) # Initialise built-in LED

p0 = Pin('G10',Pin.OUT)
p0.value(0)

ko1 = Pin('G9',Pin.OUT)
ko2 = Pin('G8',Pin.OUT)
ko3 = Pin('G7',Pin.OUT)
ko4 = Pin('G6',Pin.OUT)
ki1 = Pin('G30',Pin.IN)
ki2 = Pin('G31',Pin.IN)
ki3 = Pin('G0',Pin.IN)
ki4 = Pin('G4',Pin.IN)


#p0.value(1)
#time.sleep(1)
#p0.value(0)

# Initialise LoRa in LORAWAN mode
lora = LoRa(mode=LoRa.LORAWAN, device_class=LoRa.CLASS_C)

adc = ADC(0)
sensorAnalogPin = adc.channel(pin='P13', attn=ADC.ATTN_11DB)

# Create an ABP authentication
dev_addr = struct.unpack(">l", ubinascii.unhexlify('015867ed'))[0] # your device address here
nwk_swkey = ubinascii.unhexlify('03b8955a6e0460921059d79863f0e0c7') # your network session key here
app_swkey = ubinascii.unhexlify('15c6ee6365e2070ce14e6b79776cafde') # your application session key here

# Join the network using ABP (Activation By Personalisation)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# Remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# Set the 3 default channels to the same frequency
lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

""" Your own code can be written below! """

# uplink sending and downlink receiving
i = 0
temp_i = 0
while(True):
    code_requested = False
    if read_keypad() == 'A':
        c = acquire_code()
        if len(c)==4:
            code_requested = True
    #print(temp_read())

    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW) # create a LoRa socket
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5) # set the LoRaWAN data rate
    s.setblocking(False) # make the socket non-blocking

    i += 1
    temp_i += 1
    # uplink sending

    pkt = b'PKT #' + str(i)
    if code_requested:
        pkt += " code=" + str(c)
    elif temp_i>20:
        pkt += " temo=" + str(temp_read())
    s.send(pkt)
    print(pkt + " sent")
    time.sleep(6) # this dead-time is needed by the network to gather to your LoRa packets

    # LED blinking
    pycom.rgbled(0x000033)
    time.sleep(1)
    pycom.rgbled(0x000000)

    # downlink receiving
    rx, port = s.recvfrom(4096)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
        if rx == b'correct':
            pycom.rgbled(0x007f00)
            time.sleep(0.1)
            pycom.rgbled(0x000000)
            time.sleep(0.1)
            pycom.rgbled(0x007f00)
            time.sleep(0.1)
            pycom.rgbled(0x000000)
            time.sleep(0.1)
            pycom.rgbled(0x007f00)
            time.sleep(0.1)
            pycom.rgbled(0x000000)
        elif rx == b'incorrect':
            pycom.rgbled(0x7f0000)
            time.sleep(0.1)
            pycom.rgbled(0x000000)
            time.sleep(0.1)
            pycom.rgbled(0x7f0000)
            time.sleep(0.1)
            pycom.rgbled(0x000000)
            time.sleep(0.1)
            pycom.rgbled(0x7f0000)
            time.sleep(0.1)
            pycom.rgbled(0x000000)
        elif rx == b'open':
            p0.value(1)
        elif rx == b'close':
            p0.value(0)



    s.close() # close the LoRa socket
    time.sleep(1)
    pycom.rgbled(0x000000)
