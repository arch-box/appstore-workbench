# About
Appstore-workbench - A wip tool for Nintendo Switch and WiiU users

[![Appstore-workbench](https://raw.githubusercontent.com/LyfeOnEdge/appstore-workbench/master/docu/main.png)]()

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)]() [![Releases](https://img.shields.io/github/downloads/LyfeOnEdge/appstore-workbench/total.svg)]() [![LatestVer](https://img.shields.io/github/release-pre/LyfeOnEdge/appstore-workbench.svg)]() 

![[Brew Tools](https://discord.gg/de7tdqe)](https://github.com/LyfeOnEdge/appstore-workbench/blob/master/docu/SwitchToolsDiscordBanner.png?raw=true)

# About
A desktop gui for the Homebrew Appstore written in python.

Uses the switchbru/4TU team's site as a backend for image and package downloads.

One of the main goals of this app is to provide a homebrew management tool that doesn't require the Nintendo Switch / WiiU to access the internet. Especially useful for people who always keep their switch in airplane mode. 

#### Features:
- Homebrew for both WiiU and Nintendo Switch
- Dynamic Search
- Categories
- Downloading directly from the switchbru/4TU site
- Compatible with the Homebrew Appstore package manager
- Easily open project pages
- Threaded operations mean the app stays responsive with big downloads
- Scalable window

# Requirements:
    Works on: macOS, Windows, Linux
    Python 3.6 or greater

# How to use:
##### Windows:
- Extract appstore-workbench.zip
- Install [python](https://www.python.org/downloads/release/python-373/)
  - You *must* restart your pc after installing python for the first time.
  - If you do a custom installation remember to install tcl/tk, add python to the path, and include pip
- In a command prompt navigate to the dir you extracted the app to and type ```pip install -r requirements``` to install dependencies
- Double-click appstoreworkbench.bat

##### Macintosh:
- Extract appstore-workbench.zip
- Mac users may already have a compatible version of python installed, try double-clicking appstoreworkbench.py
- In a command prompt navigate to the dir you extracted the app to and type ```pip3 install -r requirements``` to install dependencies
  - If the file opens in a text reader, close the reader and right-click the file and open it with pylauncher
- If this still doesn't work, install [python](https://www.python.org/downloads/release/python-373/)
- To run the app: double-click unofficial-appstore.py

##### Linux:
- Extract appstore-workbench.zip
- Navigate to the directory in a terminal
- Type ```pip3 install -r requirements``` to install dependencies
- Type `python appstoreworkbench.py`
  - If you are missing dependencies do the following:
  - `sudo apt install python3 python3-pip python3-tk python3-pil.imagetk`
- If you don't know how to do this you should probably be using Windows.

## Trouble Shooting:
##### Mac:
- Error:
  - ```ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1056)```
- Solution:
  - Macintosh HD > Applications > Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file

# How to use:
- Connect your SD card to your computer
- Start the app
- If you are using a console other than the Nintendo Switch go to the settings menu and select you console and restart the app for your changes to take effect.
- Click the "Select SD root" button
- A file dialog should appear, select the root of your SD card
- Select an app you'd like to see more about
- Click install to have the app properly installed on to the SD card
- When you're done, unmount your SD card, put it in your homebrewed Nintendo Switch or WiiU, and reboot.

### Troubleshooting:
- If you are getting errors about tkinter or pillow look above at the setup instructions for your OS
- Image download errors are to be expected, please do not report them.

## Special Thanks:
- pwscind
  - Answered all sorts of questions about the appstore repos
- vgmoose
  - <3
- The rest of the 4TU team
- CrafterPika
  - Helped me get the app working with the WiiU since I don't have a one.