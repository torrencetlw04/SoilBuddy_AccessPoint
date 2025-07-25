USDA Project from Torrence Washington 

SoilBuddy Access Point Manager for Irrigation System.

Sources used:

[phewap from Simon Pickett](https://github.com/simonprickett/phewap)

[sd mount & testing from Random Nerd Tutorials by Sara Santos](https://randomnerdtutorials.com/raspberry-pi-pico-microsd-card-micropython/)

[micropython uf2 file](https://micropython.org/download/RPI_PICO/)

[PyPI](https://pypi.org/)

The purpose for this program is to be used in tandem with the Irrigation System to streamline the process of modifying the systems in work. Please recognize that this is still a work in progress to include a multitude of different features, specifically connection to and from the different microcontrollers involved in the process.

Installation Process:
1. Put Pico in BOOSTEL mode by holding the small white button on the pico and plugging it into the USB port of the computer.
2. Drag and drop the micropython uf2 file to the Pico drive and wait for to finish loading.
3. Afterwards the Pico drive will disappear, which means it is now on the Pico.
4. Download or Clone project into a compiler (perferably Visual Code Studio, Thonny should be able to work though).
5. Install MicroPico if on Visual Studio, connect to the board and upload project to Pico.
6. You can run main.py in terminal or plug the Pico into a power source and it'll automactically run the main.py file. 

NOTE: 
* This was made in mind of it only being used on the Raspberry Pi Pico W made in 2022. I believe any device that can run micropython will be able to use this program if changes are made on an indiviual level.
* The sources I stated are what I used for this program. If you would like further details into how certain libraries and functions work, those links are incredibly useful in doing so. 
* Pico is prone to freezing if too many attempts at connecting to wifi. If this happens put the pico in BOOSTEL mode and then use the [nuke_flash file](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#resetting-flash-memory) to delete files. Afterwards, you can put the Pico in BOOSTEL mode again to drop in the micropython uf2 file to make it work properly again. 

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
