from machine import enable_irq, disable_irq
import time

def getval(pin) :
    ms = [1]*300
    pin(0)
    time.sleep_us(20000)
    pin(1)
    irqf = disable_irq()
    for i in range(len(ms)):
        ms[i] = pin()      ## sample input and store value
    enable_irq(irqf)
    return ms





def DHT22(pin) :
    res = decode(getval(pin))
    hum = res[0]*256+res[1]
    temp = res[2]*256 + res[3]
    if (temp > 0x7fff):
        temp = 0x8000 - temp
    return temp, hum
