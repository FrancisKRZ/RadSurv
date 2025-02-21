Radio Surveillance

## Description

Surveillance System implementing RF24 Radio Modules, Infrared Sensors and Camera Modules.
Running in several microcontroller devices (ATMega, ARM RPI) using several client nodes
and server for surveillance database.



## Goals ##

- Implement NRF24 radio frequency module running on several ATMega microcontrollers
- Capture real time surveillance data from ATMega devices and send to a converter device
- Receive ATMega data in a converter device (ARM RPI)
- Pack the data and send it to a server using INET TCP protocol
- Server analyzes data and saves it to a local database



## Background and Stategic Fit

Context, we've to cover from [50, 1000] meters squared using RF, 
within each a maximum distance of each RF device, will be a converter device
capturing the RF write operations, buffering the data and within certain conditions,
transmit the data via TCP to the server.

The RF devices, will be using the FreeRTOS scheduler in order to integrate a sequential hardware circuit
for controlling / powering energy intensive modules used in surveillance.

The sequential circuit will have an infrared module, detects desired parameter, then trigger camera devices.

Within certain conditions, the surveillance device may send the converter device a packet capture instruction,
which will initiate packet capturing, which will also be sent to the server.



## Assumptions

- Devices will have stable power delivery.
- Server / Client INET connectivity will be stable.
- Devices will not be exposed to edge climate conditions or temperatures.
- Little to no packet interference from RF and up to RF to Server.



## Requirements

| # | Title      |   UserStory                                                   | Importance | Notes
  
| 1 | Server     |  Listen to packets from rf_to_server / converter devices      |    HIGH    |

| 2 | Client(s)  |  Converter devices (rf_to_server) listens to RF and buffers   |    HIGH    |
|   |            |  content towards server                                       |            |

| 3 | RF Modules |  Surveillance devices, implements IR sensors, camera modules  |    HIGH    |
|   |            |  and triggers packet surveillance from client(s)              |            |

| 4 | Alert Mods.|  Listens to RF modules which triggers a physical sensor to    |    LOW     | Although low priority, a good chunk
|   |            |  alert personnel of surveillance device trigger               |            | of work has gone into it, haha.


Server and Client will be run from a virtual environment such as to manage their respective purposes,
database from the server and rf gpio from the client. The version is not of importance.



# Directories

   [Device  | Working Directory]
    ATMega  | receiver/
    ATMega  | transmitter/
    RPI     | server/

[Working Directory Files]
    - receiver.ino      Localized alert module when transmitter sends a true alert, managed by FreeRTOS scheduler
    - transmitter.ino   Sends true alert to receivers, including server which has an NRF24 module installed
    - server.py         Manages incoming transmitter signals for data storage
    - rf_to_server.py   Listens to transmitter's signals, writes into a buffer then writes to TCP server.

[Output Directory]
    - log/              : Contains error logs obtain at running time from server.py and rf_to_server.py
    - db/               : Database storing time, surveillance types and notable behaviors



## User Interaction and Design

Server and Client connection files, server.py and rf_to_server.py will utilize argparse for the following arguments:

    server.py:
        --hostname:         Remote Server's hostname
        --port:             Remote Server's port

    rf_to_server.py:
        --hostname:         Local device hostname running RF PIGPIO daemon
        --port:             Local device port running RF PIGPIO daemon
        --remotehostname:   Remote Server's hostname
        --remoteport:       Remote Server's port
        --address:          RF Node addresses



## TODO

    Add hooks to each tasks for managing mutex wr/rd prior to rx 
    operation from transmitter.ino inside of receiver.ino

    Database design



## Resources and References

Socket Programming TCP <Server>: https://docs.python.org/3.11/howto/sockets.html
RF24 <Transmitters and Receivers>:   https://github.com/nRF24/RF24?tab=readme-ov-file
RF24 <RF to Server Converter>: https://github.com/bjarne-hansen/py-nrf24
FreeRTOS <Scheduler>: https://www.freertos.org/Documentation/00-Overview


[Auxiliary]
    NRF24 Python by user bjarne-hansen
    - $apt install pipgpio python-pigpio python3-pigpio
    - pip install nrf24 

