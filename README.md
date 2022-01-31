# SmartLight
This project takes place as part of our lecture "Integrationsseminar" at DHBW Mannheim.

The Team Members of this Project are:
- Ann-Kathrin Kälberer (5799502)
- Canberk Alkan (3275561)
- Dominic Viola (1044258)

## Description
This project focuses on the creation of a light alarm clock. It will integrate with pre-existing devices like a smartphone with a alarm clock capability. The purpose of the light alarm clock is to wake users naturally by first using ambient light and then ringing the alarm. 

The alarm clock functionality is applicable via two different applications. If you are using an iPhone the idea was to use the app "Shortcuts" (z. Dt. Kurzbefehle) for the alarm clock implementation. Another way of accessing the clock is via the web. So both Apple and Android devices are capable of using this functionality. For the web application any browser can be used.

The following list consists of the used tools to realize this platform.
- Raspberry Pi 4
- LED strip
- Adapter
- Power supply
- Jumper
- Plug-in board

The following software packages were used:
- Raspberry Pi OS -> Operating System of the Raspberry Pi 4. Used for development environment to directly communicate with the Raspberry Pi.
- Python -> This programming language is used to implement the logic for the GPIO Pins
- Flask -> Is used for the backend programming of the web server
- Shortcuts -> Is used to have an implementation of this platform in the form of a smartphone app (Apple devices only)


To measure the performance of the platform, functional and non-functional requirements were defined.

Functional requirements (Purpose and functions of the device)
- At a defined time, the light should turn on
- Turn on/off the clock
- Set alarm clock time
- Control via smartphone

Non-functional requirements (How well does the device implement the functions)
- Ease of use
- Effectiveness (Brightness of the light)
- Extensibility (Set many different alarms)
- Functionality 

Tasks can be devided in
- Flask Webserver implementation: Ann-Kathrin Kälberer 
- Logic of LED and GPIO Pins: Dominic Viola, Canberk Alkan
- Presentation and Documentation: Canberk Alkan 


## Implementation 
We use a Raspberry Pi 4 to controll a LED strip. (Any other Raspberry Pi model or an Arduino would also work, if you install a network antenna.) The Raspberry Pi hosts a REST API Server that exposes controlls for the LED Strip to the LAN. 

The alarm clock application of a Smartphone will serve as a trigger, that sends an HTTP request to the REST server.  

![architecture](assets/implementation_architecture.png)

---
## Developer Notes

<br>

### Folders
The files to setup and modify the Flask REST server are in the folder [backend](backend).

The subfolder [/backend/scripts](backend/scripts) contains python scripts that help to debug the API server.

The [assets](assets) folder is meant for pictures and other materials that are included in this README.

<br>

### Setup for the backend
Install the dependencies:
```bash
pip install -r requirements.txt
```

Start the server:
```bash
python backend/server.py
```
This should start the server and create the files ```.secret``` and ```secret_clear.txt``` the server will use those as a store for the server password.

## Website
Install the dependencies:
```bash
pip install flask
pip install SQLAlchemy
```
Start the Website:
```bash
python "app.py"
```
