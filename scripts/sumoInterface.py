#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      teabqe
#
# Created:     19/06/2012
# Copyright:   (c) teabqe 2012
# Licence:     <your licence>
#
# TO DO: encapsular el acceso a SUMO en un objeto
#
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
    global sumoPath
    sumoPath = path

def getSumoPath():
    global sumoPath
    return sumoPath

def setSumoLogPath(path):
    global sumoLogPath
    sumoLogPath = path

def getSumoLogPath():
    global sumoLogPath
    return sumoLogPath

def setDuarouterPath(path):
    global duarouterPath
    duarouterPath = path

def getDuarouterPath():
    global duarouterPath
    return duarouterPath

def setDuarouterLogPath(path):
    global duarouterLogPath
    duarouterLogPath = path

def getDuarouterLogPath():
    global duarouterLogPath
    return duarouterLogPath

def setNetconvertPath(path):
    global netconvertPath
    netconvertPath = path

def getNetconvertPath():
    global netconvertPath
    return duarouterPath

def setNetconvertLogPath(path):
    global netconvertLogPath
    netconvertLogPath = path

def getNetconvertLogPath():
    global netconvertLogPath
    return netconvertLogPath


def runSumoSimulation(sumocfgPath):
    commandSumo = ["D:\\Appls\\SUMO\\sumo-0.15.0\\bin\\sumo.exe", "-c",sumocfgPath]
    log = open("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\sumo.log", "w+")
    #commandSumo = [getSumoPath(), "-c",sumocfgPath]
    #log = open(getSumoLogPath(), "w+")
    log.flush()
    retCode = subprocess.call(commandSumo, stdout=log, stderr=log)
    log.close

def runDuarouter(duaroutercfgPath):
    commandDuarouter = ["D:\\Appls\\SUMO\\sumo-0.15.0\\bin\\duarouter.exe", "-c",duaroutercfgPath]
    log = open("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\duatouter.log", "w+")
    #commandDuarouter = [getDuarouterPath(), "-c",duaroutercfgPath]
    #log = open(getDuarouterLogPath(), "w+")
    log.flush()
    retCode = subprocess.call(commandDuarouter, stdout=log, stderr=log)
    log.close

def runNetconvert(netconvertcfgPath):
    commandNetconvert = [getNetconvertPath(), "-c",netconvertcfgPath]
    log = open(getNetconvertLogPath(), "w+")
    log.flush()
    retCode = subprocess.call(commandNetconvert, stdout=log, stderr=log)
    log.close

def main():
    pass

if __name__ == '__main__':
    main()
