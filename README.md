# ubuntu-bios-settings-checker
Provide a API to check BIOS setting for Ubuntu installer

# Usage
## UbuntuBIOSSettingsChecker class
This class will provide an abstract level. 
According the manufacter (read from DMI) to load the manufacter class.
### Syntax

```
class UbuntuBIOSSettingsChecker:
   def __init__(self, configFile = "" )
```

####Parameters
##### configFile
The full file patch of the configure file.
If you don't set it. The default configure file patch is
/usr/share/UbuntuBIOSSettingsChecker/config.

####member
#####status
######0: class is initialized successfully.

######-1: There are something wrong. Maybe the manufacturer is not support yet.

#####support:

######True: The BIOS settings is proper.

######False: The BIOS settings is not proper.


## DellChecker class
Using the libsmbios to check the BIOS settings.
### Syntax

```
class DellChecker():
	configure = None
	def __init__(self, configFile = "")
	def check(self)
	def readConfigure(self, configFile = "")
	def tokenInfo(self, tokenObj, action)
```

####Parameters
#####configFile
The full file patch of the configure file.
If you don't set it. The default configure file patch is
/usr/share/UbuntuBIOSSettingsChecker/config.

#####tokenObj
The tokenObj come from smbios-token-ctl.

```
tokenTable = smbios_token.TokenTable()
tokenObj = tokenTable[smbios_keys]
```

#####action
This parameter come from smbios-token-ctl.

"is-bool": the method wil return the value of a bool.

"is-string": the method wil return the value of a string.

"is-active": the method wil return the active state


### Example 

```
import UbuntuBIOSSettingsChecker
def main():
    ubsc=UbuntuBIOSSettingsChecker("config")
    if ubsc.status == 0:
        if ubsc.support :
            print("Ubuntu can be installed with this BIOS settings.")
        else:
            print("The BIOS settings is not proper.")
    else:
        print("This utility does not support {} yet.".format(ubsc.manufacturer))

```

## Comand line
### Syntax

```
sudo python3 UbuntuBIOSSettingsChecker.py 
```