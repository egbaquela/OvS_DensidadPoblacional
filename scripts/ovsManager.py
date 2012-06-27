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
import outputAnalysis

def main():
    origen = cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.dop.xml")
    destino = cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.ddp.xml")
    routeFilePath= "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido"
    sumocfgPath = "D:\Compartido\Proyectos\SUMO\OvS_DensidadPoblacional\models\\SNResumido.sumo.cfg"
    duaroutercfgPath = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido.ruoc.cfg"

    sumoInterface.setSumoPath("D:\\Appls\\SUMO\\sumo-0.13.1\\bin\\sumo-gui.exe")
    sumoInterface.setSumoLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\sumo.log")
    sumoInterface.setDuarouterPath("D:\\Appls\\SUMO\\sumo-0.13.1\\bin\\duarouter.exe")
    sumoInterface.setDuarouterLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\duatouter.log")


    flowGenerator.generateFlowsInXML(origen, destino, routeFilePath)
    sumoInterface.runDuarouter(duaroutercfgPath)

    i=0
    optimalSolution = FALSE
    while not(optimalSolution):
        sumoInterface.runSumoSimulation(sumocfgPath)
        if outputAnalysis.evaluateSolution():
            optimalSolution = TRUE
        else:
            i=i+1
            if (i==5):
                break
            #generateNewSolutions()

    print("SoluciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n Encontrada")
    pass

if __name__ == '__main__':
    main()
