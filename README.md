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

- [General](#General)
    - [Print hostname](#Print-hostname)
    - [Show general status info](#Show-general-status-info)

- [Networking](#Networking)
    - [Get current connectivity state](#Get-current-connectivity-state)
    - [Force connectivity check](#Force-connectivity-check)
    - [Enable networking](#Enable-networking)
    - [Disable networking](#Disable-networking)

- [Connection](#Connection)
    - [List active connections](#List-active-connections)
    - [Delete connection](#Delete-connection)
    - [Deactivate connection](#Deactivate-connection)
    - [List all connections](#List-all-connections)

- [Wi-Fi](#Wi-Fi)
    - [List available access points](#List-available-access-points)
    - [Switch wireless on](#Swtich-wireless-on)
    - [Switch wireless off](#Swtich-wireless-off)
    - [Show wifi status](#Show-wifi-status)
    - [Scan for access points](#Scan-for-access-points)

- [Device](#Device)
    - [List all devices](#List-all-devices)
    - [Print details for a device](#Print-details-for-a-device)
    - [Tell network manager to manage a device](#Tell-network-manager-to-manage-a-device)
    - [Tell network manager to stop managing a device](#Tell-network-manager-to-stop-managing-a-device)
    - [Enable autoconnect on a device](#Enable-autoconnect-on-a-device)
    - [Disable autoconnect on a device](#Disable-autoconnect-on-a-device)
    - [Print overall device information](#Print-overall-device-information)
    - [Delete a device](#Delete-a-device)
    - [Disconnect a device](#Disconnect-a-device)
    - [Reapply connection settings for a device](#Reapply-connection-settings-for-a-device)

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