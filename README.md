# Yadom OLED case
Example to use the [Yadom OLED case](https://yadom.fr/plateformes-de-developpement/raspberry-pi/boitiers/boitier-din-avec-afficheur-oled-et-clavier.html) in Python.

## Prerequisites

### Install system package
```bash
sudo apt install python3-pil
```

### Install python packages
```bash
pip3 install -r requirements.txt
```

## Installation

### Add a crontab entry
Add an entry in the crontab to call the script at boot: 
```
@reboot <path_to_yadom.py>
```
The crontab can be configured with:
```bash
crontab -e
```
