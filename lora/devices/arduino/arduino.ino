"""Copyright (C) 2018  Eurac Research - Center for Sensing Solutions
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

#include <LoRaWan.h>
#include <stdlib.h>

char buffer[256];
char pkt[6];

int j = 0;

void setup(void)
{
  pinMode(LED_BUILTIN, OUTPUT); // Initialise the built-in LED

  SerialUSB.begin(115200);
  while(!SerialUSB);

  // Initialise the LoRa module
  lora.init();

  memset(buffer, 0, 256);
  lora.getVersion(buffer, 256, 1);
  SerialUSB.print(buffer);

  memset(buffer, 0, 256);
  lora.getId(buffer, 256, 1);
  SerialUSB.print(buffer);

  // create an ABP authentication
  lora.setKey("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"); // your network session key here (three times)
  lora.setDeciveMode(LWABP);
  lora.setDataRate(DR0, EU868);

  //Set the 3 default channels
  lora.setChannel(0, 868.1);
  lora.setChannel(1, 868.3);
  lora.setChannel(2, 868.5);

  lora.setReceiceWindowFirst(0, 868.1);
  lora.setReceiceWindowSecond(869.5, DR3);

  lora.setDutyCycle(false);
  lora.setJoinDutyCycle(false);

  // Set the TX power 
  // Set the TX power 
  lora.setPower(14); 
}

void loop(void)
{     
  j = j+1;
  char strLitt[6] = "PKT #";
  char strNum[6];
  sprintf(strNum, "%d", j);
  String strFinal = strcat (strLitt,strNum);
  strFinal.toCharArray(pkt, 12);

  """ Your own code can be written below! """;

  short rssi;

  // uplink sending
  lora.transferPacket(pkt,6);

  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW

  // downlink receiving
  memset(buffer, 0, 256);
  lora.receivePacket(buffer, 256, &rssi);
  SerialUSB.println(buffer);
}
