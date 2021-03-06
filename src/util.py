#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
'''
Created on Jun 28, 2011

@author: wired
'''
import traceback
import logging
import logging.handlers
import configobj
import validate

def load_conf(conf_file):
    try:
        config = configobj.ConfigObj(conf_file, configspec=spec)
    except:
        traceback.print_exc()
        exit('Error parsing the ' + conf_file + ' please check it out.')
    validator = validate.Validator()
    if config.validate(validator) is not True:#), copy=True)
        exit(CONF_FILE + ' file has problems...please check.')    
    return config

#Loading config files
CONF_PREFIX = '/usr/local/etc/usbuirtd'
CONF_FILE = CONF_PREFIX + '/usbuirtd.conf'
REMOTE_CONF_FILE = CONF_PREFIX + '/remotes.conf'


default_config = """
[CONF_VAR]
APP_NAME = string(default='UsbUIRTd')
APP_USER = string(default='root')
DEV_FILE = string(default='/dev/ttyUSB0')
SO_FILE = string(default='/lib/uuirtdrv.so')
LOG_FILENAME = string(default='/tmp/usbuirtd.log')
LOG_LEVEL = integer(default=10)
TCP_CLIENT_LISTEN = integer(default=15)
TCP_PORT = integer(min=1025, max=50000, default=8765)

[TV]
POWER_DELAY = float(default=10.3)
"""
spec = default_config.split("\n")

CONF_VAR = load_conf(CONF_FILE)['CONF_VAR']
TV_VAR = load_conf(CONF_FILE)['TV']


log = logging.getLogger(CONF_VAR['APP_NAME'])
log.setLevel(CONF_VAR['LOG_LEVEL'])

# create file handler which logs even debug messages
fh = logging.handlers.RotatingFileHandler(CONF_VAR['LOG_FILENAME'], maxBytes=2000000, backupCount=5, encoding = 'UTF-8')
fh.setLevel(CONF_VAR['LOG_LEVEL'])
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(CONF_VAR['LOG_LEVEL'])
            
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s -\t%(levelname)s\t- %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
log.addHandler(fh)
log.addHandler(ch)

###################################
#REMOTES section
###################################
REMOTE = {} #main dictionary
config = load_conf(REMOTE_CONF_FILE)
REMOTE_NAMES = config['REMOTES']['REMOTE_NAMES']

#When we add debug capabilities...this will be printed out
if CONF_VAR['LOG_LEVEL'] == 10:
            log.info('*********************************************************')
            log.info('*                        NEW LOG                        *')
            log.info('*********************************************************')
for i in REMOTE_NAMES:
    try:
        REMOTE[i] =  config['REMOTES'][i]
        log.debug('\''+ i + '\' remote control added succesfully')
    except:
        log.error('\'' + i + '\' remote control is *NOT* in config file!!')



if __name__ == '__main__':
    #log.debug(REMOTE_NAMES[0])
    print REMOTE['foxtel']
    for i in REMOTE:
        log.debug('--> ' +i)
