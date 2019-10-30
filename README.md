# Wypy is a command line utility to manage network connections.

## Pre-Requisites
Before you can start using WyPy, you need to make sure `NetworkManager` is installed on your system.
If you don't have it, download it through your system's package manager.

### Debian / Ubuntu 
```
sudo apt-get install network-manager
```

### Arch 

```
sudo pacman -S network-manager
```

**Instructions for other linux distros coming soon ...**


The _base_ list of features will include:

- Scanning the network for access points
- turn the radio on
- turn the radio off
- connect to an access point
- disconnect from an access point
- check if an access point was saved
- list access points
- listing devices

## Some litterature

- https://www.freedesktop.org/wiki/IntroductionToDBus/
- https://dbus.freedesktop.org/doc/dbus-tutorial.html
- https://dbus.freedesktop.org/doc/dbus-python/tutorial.html
