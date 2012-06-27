#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      teabqe
#
# Created:     15/06/2012
# Copyright:   (c) teabqe 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sumoInterface
import flowGenerator

def main():
    origen = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.dop.xml"
    destino = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.ddp.xml"
    routeFilePath= "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido"
    sumocfgPath = "D:\Compartido\Proyectos\SUMO\OvS_DensidadPoblacional\models\\SNResumido.sumo.cfg"
    duaroutercfgPath = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido.ruoc.cfg"

    setSumoPath("D:\\Appls\\SUMO\\sumo-0.13.1\\bin\\sumo.exe")
    setSumoLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\sumo.log")
    setDuarouterPath("D:\\Appls\\SUMO\\sumo-0.13.1\\bin\\duarouter.exe")
    setDuarouterPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\duatouter.log")


    generateFlowsInXML(origen, destino, routeFilePath)
    runDuarouter(duaroutercfgPath)

    optimalSolution = FALSE
    while not(optimalSolution):
        runSumoSimulation(sumocfgPath)
        if evaluateSolution():
            optimalSolution = TRUE
        else:
            generateNewSolutions()

    print("SoluciÃƒÆ’Ã‚Â³n Encontrada")
    pass

if __name__ == '__main__':
    main()
