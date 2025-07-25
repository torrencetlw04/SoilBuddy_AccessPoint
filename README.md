USDA Project from Torrence Washington 

Access Point Manager for Irrigation System.

Sources used:

[phewap from Simon Pickett](https://github.com/simonprickett/phewap)

[sd mount & testing from Random Nerd Tutorials by Sara Santos](https://randomnerdtutorials.com/raspberry-pi-pico-microsd-card-micropython/)

[micropython uf2 file](https://micropython.org/download/RPI_PICO/)

Steps to using SoilBuddy Access Point:
 1. Connect Raspberry Pi Pico W to a power source, or if on Compiler run main.py.
 2. Go to wifi settings and connect to "USAP".
 3. Go to 192.168.4.1 in a browser of your choosing at you'll arrive at the SoilBuddy AP!

You can configure to connect to wifi but accessing the IP the Access Point is connected to can be an issue.

Features in Access Point:
* Create/Edit Save Files for Irrigation System
* Rename Files
* Delete Files from SoilBuddy
* Reset & Disconnect from WiFi to use in Access Point Mode (192.168.4.1)
* Upload Files to SoilBuddy (Work In Progress)
* Apply changes from the files to Irrigation System

Installation Process:
1. Put Pico in BOOSTEL mode by holding the small white button on the pico and plugging it into the USB port of the computer.
2. Drag and drop the micropython uf2 file to the Pico drive and wait for to finish loading.
3. Afterwards the Pico drive will disappear, which means it is now on the Pico.
4. Download or Clone project into a compiler (perferably Visual Code Studio, Thonny should be able to work though).
5. Install MicroPico if on Visual Studio, connect to the board and upload project to Pico.
6. You can run main.py in terminal or plug the Pico into a power source and it'll automactically run the main.py file. 

NOTE: 
Pico is prone to freezing. If this happens put the pico in BOOSTEL mode and then use the [nuke_flash file](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#resetting-flash-memory) to delete files. Afterwards, you can put the Pico in BOOSTEL mode again to drop the micropython uf2 file to make it work again. 
