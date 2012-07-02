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
    origen = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.dop.xml")
    destino = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.ddp.xml")
    origenNormalizado= flowGenerator.normalize(origen, 2000)
    destinoNormalizado = flowGenerator.normalize(destino, 2000)

    routeFilePath= "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido"
    sumocfgPath = "D:\Compartido\Proyectos\SUMO\OvS_DensidadPoblacional\models\\SNResumido.sumo.cfg"
    duaroutercfgPath = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido.ruoc.cfg"

    sumoInterface.setSumoPath("D:\\Appls\\SUMO\\sumo-0.13.1\\bin\\sumo-gui.exe")
    sumoInterface.setSumoLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\sumo.log")
    sumoInterface.setDuarouterPath("D:\\Appls\\SUMO\\sumo-0.13.1\\bin\\duarouter.exe")
    sumoInterface.setDuarouterLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\duatouter.log")


    flowGenerator.generateFlowsInXML(origenNormalizado, destinoNormalizado, routeFilePath)
    sumoInterface.runDuarouter(duaroutercfgPath)

    i=0
    optimalSolution = False
    while not(optimalSolution):
        sumoInterface.runSumoSimulation(sumocfgPath)
        if outputAnalysis.evaluateSolution():
            optimalSolution = True
        else:
            i=i+1
            if (i==5):
                break
            origenNormalizado = flowGenerator.shuffleOriDest(origenNormalizado)
            destinoNormalizado = flowGenerator.shuffleOriDest(destinoNormalizado)
            flowGenerator.generateFlowsInXML(origenNormalizado, destinoNormalizado, routeFilePath)
            sumoInterface.runDuarouter(duaroutercfgPath)


    print("Solución Encontrada")
    pass

if __name__ == '__main__':
    main()
