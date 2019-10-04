#!/usr/bin/env python3
import os
import subprocess
import sys
import json
from libsmbios_c import smbios_token
import logging

logging.basicConfig(level=logging.WARNING)

DEFAULT_CONFIGURE_PATH="/usr/share/UbuntuBIOSSettingsChecker/config"

class CheckerTemplator:
    def __init__(self):
        pass
    def readConfigure():
        pass

class DellChecker(CheckerTemplator):
    configure = None
    tokenTable = smbios_token.TokenTable()
    def __init__(self, configFile = ""):
        self.readConfigure(configFile)
        pass

    def check(self) -> bool:
        ret = True
        try:
            productName = subprocess.Popen("dmidecode -s system-product-name".split(),stdout=subprocess.PIPE ).stdout.read().strip().decode("utf-8")
        except(e):
            logging.critical("{}".format(e))
            pass
        
        # check the default settings
        logging.debug(self.configure["default"])
        for key in self.configure["default"].keys():
            if key != "url":
                tokenObj = self.tokenTable[int(key)]
                if type(self.configure["default"][key]["value"]) == bool:
                    (exit_code, t, value) = self.tokenInfo(tokenObj, "is-bool" )
                else:
                    (exit_code, t, value) = self.tokenInfo(tokenObj, "is-string" )
                
                if self.configure["default"][key]["value"] != value:
                    
                    return False

        if productName in self.configure.keys():
            logging.info(self.configure[productName])

        return True

    def readConfigure(self, configFile = ""):
        configFilePath = None
        if os.path.isfile(configFile):
            configFilePath = configFile
            if os.path.isfile(DEFAULT_CONFIGURE_PATH):
                configFilePath = DEFAULT_CONFIGURE_PATH
        if configFilePath:
            with open(configFilePath) as f:
                self.configure = json.load(f)

    def tokenInfo(self, tokenObj, action):
        '''
        I copy this function from smbios-token-ctl that come from smbios-utils package.
        '''
        exit_code=1

        type = _("<weird unknown type>")
        value = _("<unknown value>")
        if tokenObj.isBool():
            if action == "is-bool": exit_code = 0
            type="bool"
            value=False
            if tokenObj.isActive():
                if action == "is-active": exit_code = 0
                value=True

        elif tokenObj.isString():
            if action == "is-string": exit_code = 0
            type = "string"
            value = tokenObj.getString()

        return (exit_code, type, value)


class UbuntuBIOSSettingsChecker:
    support = False
    manufacturer = None
    status = 0
    configure = None
    tokenObj = None
    checker = None
    def __init__(self, configFile = "" ):
        try:
            manufacturer = subprocess.Popen("dmidecode -s system-manufacturer".split(),stdout=subprocess.PIPE ).stdout.read().strip()
        except(FileNotFoundError):
            self.status = -1
            return None
    
        logging.debug("The manufacturer is {}.".format(manufacturer))
        self.manufacturer = manufacturer

        if manufacturer == b"Dell Inc." :
            self.checker = DellChecker(configFile)
        elif manufacturer == b"Hewlett-Packard":
            #self.checker = HPChecker()
            logging.debug("This class don't support {} yet.".format(manufacturer))
            return None
        else :
            logging.debug("This class don't support {} yet.".format(manufacturer))
            self.status = -1
            return None
        
        self.support = self.checker.check()


def main():
    ubsc=UbuntuBIOSSettingsChecker("config")
    if ubsc.status == 0:
        if ubsc.support :
            print("Ubuntu can be installed with this BIOS settings.")
        else:
            print("The BIOS settings is not proper.")
    else:
        print("This utility does not support {} yet.".format(ubsc.manufacturer))


    pass

if __name__ == "__main__":
    main()
