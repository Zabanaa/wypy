# Wypy 

WyPy is a command line utility to manage network connections.

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

## Installation 

```python
pip install WyPy
pipenv install WyPy
```

## Usage

- [General](###General)
    - [Print hostname](####Print%20hostname)
    - [Show general status info](####Show%20general%20status%20info)

- [Networking](###Networking)
    - [Get current connectivity state](####Get%20current%20connectivity%20state)
    - [Force connectivity check](####Force%20connectivity%20check)
    - [Enable networking](####Enable%20networking)
    - [Disable networking](####Disable%20networking)

- [Connection](###Connection)
    - [List active connections](####List%20active%20connections)
    - [Delete connection](####Delete%20connection)
    - [Deactivate connection](####Deactivate%20connection)
    - [List all connections](####List%20all%20connections)

- [Wi-Fi](###Wi-Fi)
    - [List available access points](####List%20available%20access%20points)
    - [Switch wireless on](####Swtich%20wireless%20on)
    - [Switch wireless off](####Swtich%20wireless%20off)
    - [Show wifi status](####Show%20wifi%20status)
    - [Scan for access points](####Scan%20for%access%20points)

- [Device](###Device)
    - [List all devices](####List%20all%20devices)
    - [Print details for a device](####Print%20details%20for%20a%20device)
    - [Tell network manager to manage a device](####Tell%20network%20manager%20to%20manage%20a%20device)
    - [Tell network manager to stop managing a device](####Tell%20network%20manager%20to%20stop%20managing%20a%20device)
    - [Enable autoconnect on a device](####Enable%20autoconnect%20on%20a%20device)
    - [Disable autoconnect on a device](####Disable%20autoconnect%20on%20a%20device)
    - [Print overall device information](####Print%20overall%20device%20information)
    - [Delete a device](####Delete%20a%20device)
    - [Disconnect a device](####Disconnect%20a%20device)
    - [Reapply connection settings for a device](####Reapply%20connection%20settings%20for%20a%20device)

<!-- toc -->

### General
-----------

#### Print hostname

```
wypy general hostname
```

#### Show general status info

```
wypy general status
```

### Networking
--------------

#### Get current connectivity state

```
wypy network connectivity
```

#### Force connectivity check

```
wypy network connectivity --check
```

#### Enable networking

```
wypy network enable
```

#### Disable networking

```
wypy network disable
```

### Connection
--------------

#### List active connections

```
wypy connection active
```

#### Delete connections

```
wypy connection delete
```

#### Deactivate connection

```
wypy connection down <connection>
```

#### List all connections

```
wypy connection list
```

### Wi-Fi
---------

#### List available access points

```
wypy wifi list
```

#### Switch wireless on

```
wypy wifi on
```

#### Switch wireless off

```
wypy wifi off
```

#### Show wifi status

```
wypy wifi status
```

#### Scan for access points

```
wypy wifi rescan
```

### Device
---------

#### List all devices
```
wypy device list
```

#### Print details for a device
```
wypy device get <device_name>
```

#### Tell network manager to manage a device
```
wypy device manage <device_name>
```

#### Tell network manager to stop managing a device
```
wypy device manage <device_name> --off
```


#### Enable autoconnect on a device
```
wypy device autoconnect <device_name>
```

#### Disable autoconnect on a device
```
wypy device autoconnect <device_name> --disable
```

#### Print overall device status
```
wypy device status
```

#### Delete a device
```
wypy device delete <device_name>
```

#### Disconnect a device
```
wypy device disconnect <device_name>
```

#### Reapply connection settings for a device
```
wypy device update <device_name>
```

---
## List of features / commands coming in the next versions

- [ ] wypy connection up 
- [ ] wypy connection get 
- [ ] wypy connection modify
- [ ] wypy connection edit
- [ ] wypy connection clone
- [ ] wypy connection load
- [ ] wypy connection export
- [ ] wypy connection import
- [ ] wypy connection monitor
- [ ] wypy connection add
- [ ] wypy wwan enable
- [ ] wypy wwan disable
- [ ] wypy wifi hotspot
- [ ] wypy device monitor
- [ ] wypy device modify
- [ ] wypy device connect