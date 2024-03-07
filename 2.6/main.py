#!/usr/bin/env python3.8
from json import dumps
from getIpsecConf import getIpsecConf
from getSwanConf import getSwanConf
from getFormated import getFormated
from sys import argv

if __name__ == "__main__":
    # xmlFile = '/cf/conf/config.xml'
    # ipsecFile = '/var/etc/ipsec/swanctl.conf'
    xmlFile = '../config.xml'
    ipsecFile = '../swanctl.conf'

    ipsecList = getIpsecConf(xmlFile)
    swanList = getSwanConf(ipsecFile)
    formated = getFormated(ipsecList, swanList)

    print(dumps(formated))
