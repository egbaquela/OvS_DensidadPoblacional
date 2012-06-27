#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      teabqe
#
# Created:     12/06/2012
# Copyright:   (c) teabqe 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os, sys, subprocess, types

def main():
    commandDuarouter = ['D:\\Appls\\SUMO\sumo-0.13.1\\bin\\duarouter', '-c', 'D:\\Compartido\\Proyectos\\SUMO\\SNResumido\\models\\routes\\SNResumido.ruoc.cfg']
    commandSumo = ['D:\\Appls\\SUMO\sumo-0.13.1\\bin\\sumo-gui', '-c', 'D:\\Compartido\\Proyectos\\SUMO\\SNResumido\\models\\SNResumido.sumo.cfg']
    log = open("D:\\Compartido\\Proyectos\\SUMO\\SNResumido\\logs\\mylog.txt", "w+")
    log.flush()
    retCode = subprocess.call(commandDuarouter, stdout=log, stderr=log)
    retCode = subprocess.call(commandSumo, stdout=log, stderr=log)
    print(log)
    log.close
    pass

if __name__ == '__main__':
    main()
