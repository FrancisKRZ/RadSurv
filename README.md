[Radio Surveillance]

Utilizes ATMega microcontrollers with radio modules for transmitting and receiving real time data
Uses FreeRTOS Scheduler for synchronizing alert modules in accordance to live data.

Will send data to a local server for hosting and back ups.


_____________________________________________________________________
TODO:
    Add hooks to each tasks for managing mutex wr/rd
    prior to rx operation from transmitter.ino inside of receiver.ino
_____________________________________________________________________



[Files]
    - server.py         Manages incoming transmitter signals for data storage
    - receiver.ino      Localized alert module when transmitter sends a true alert, managed by FreeRTOS scheduler
    - transmitter.ino   Sends true alert to receivers, including server which has an NRF24 module installed
	[Auxiliary]
		- $apt install pipgpio python-pigpio python3-pigpio
		- pip install nrf24 

[Platforms]
    - Raspberry Pi Zero :   server.py
    - Arduino Uno R3    :   receiver.ino
    - Arduino Mega      :   transmitter.ino 
