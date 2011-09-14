#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
'''
Created on Sep 14, 2011

@author: raul
'''
import util

###################################
#REMOTES section
###################################
REMOTE = {} #main dictionary
config = util.load_conf(util.REMOTE_CONF_FILE)
REMOTE_NAMES = config['REMOTES']['REMOTE_NAMES']
for i in REMOTE_NAMES:
    try:
        REMOTE[i] =  config['REMOTES'][i]
        util.log.debug('\''+ i + '\' remote control added succesfully')
    except:
        util.log.error('\'' + i + '\' remote control is *NOT* in config file!!')



if __name__ == '__main__':
    #log.debug(REMOTE_NAMES[0])
    print REMOTE['foxtel']
    for i in REMOTE:
        util.log.debug('--> ' +i)