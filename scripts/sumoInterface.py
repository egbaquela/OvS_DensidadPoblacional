#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      teabqe
#
# Created:     19/06/2012
# Copyright:   (c) teabqe 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os, sys, subprocess, types

sumoPath = ""
sumoLogPath = ""
duarouterPath = ""
duarouterLogPath = ""
netconvertPath = ""
netconvertLogPath = ""

def setSumoPath(path):
    sumoPath = path

def getSumoPath():
    return sumoPath

def setSumoLogPath(path):
    sumoLogPath = path

def getSumoLogPath():
    return sumoLogPath

def setDuarouterPath(path):
    duarouterPath = path

def getDuarouterPath():
    return duarouterPath

def setDuarouterLogPath(path):
    duarouterLogPath = path

def getDuarouterLogPath():
    return netconvertLogPath

def setNetconvertPath(path):
    netconvertPath = path

def getNetconvertPath():
    return duarouterPath

def setNetconvertLogPath(path):
    netconvertLogPath = path

def getNetconvertLogPath():
    return netconvertLogPath


def runSumoSimulation(sumocfgPath):
    commandSumo = [getSumoPath(), "-c",sumocfgPath]
    log = open(getSumoLogPath, "w+")
    log.flush()
    retCode = subprocess.call(commandSumo, stdout=log, stderr=log)
    log.close

def runDuarouter(duaroutercfgPath):
    commandDuarouter = [getDuarouterPath(), "-c",duaroutercfgPath]
    log = open(getDuarouterLogPath, "w+")
    log.flush()
    retCode = subprocess.call(commandDuarouter, stdout=log, stderr=log)
    log.close

def runNetconvert(netconvertcfgPath):
    commandNetconvert = [getNetconvertPath(), "-c",netconvertcfgPath]
    log = open(getNetconvertLogPath, "w+")
    log.flush()
    retCode = subprocess.call(commandNetconvert, stdout=log, stderr=log)
    log.close

def main():
    pass

if __name__ == '__main__':
    main()
