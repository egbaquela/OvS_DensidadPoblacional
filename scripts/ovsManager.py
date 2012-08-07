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
from consts import *
import listMatrix
import time

def main():

    print(time.time())
    #Cargo las listas de nodos orígenes y destinos y los normalizo
    origen = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.dop.xml")
    destino = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.ddp.xml")
    #origen = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\spider15x15x100.dop.xml")
    #destino = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\spider15x15x100.ddp.xml")
    origenNormalizado= flowGenerator.normalize(origen, 10000)
    destinoNormalizado = flowGenerator.normalize(destino, 10000)

    #Definos las variables de Paths
    routeFilePath= "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido"
    sumocfgPath = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\SNResumido.sumo.cfg"
    duaroutercfgPath = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido.ruoc.cfg"
    #duaroutercfgPath = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\spider15x15x100.ruoc.cfg"
    outputTrips = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\output\\SNResumido.trip.xml"

    sumoInterface.setSumoPath("D:\\Appls\\SUMO\\sumo-0.15.0\\bin\\sumo-gui.exe")
    sumoInterface.setSumoLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\ulogs\\sumo.log")
    sumoInterface.setDuarouterPath("D:\\Appls\\SUMO\\sumo-0.15.0\\bin\\duarouter.exe")
    sumoInterface.setDuarouterLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\duatouter.log")

    #Creo/abro el archivo para grabar las soluciones encontradas
    fd = open("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\output\\output.log", "w")
    #myLog2 = open("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\MyLog2.log", "a")

    #Genero la población inicial de soluciones
    bestSolutions=[]
    thisSolution=[]
    optimalSolution = False
    factor = 0.01
    for n in range(1):
        #genero una solución en forma aleatoria
        flowGenerator.shuffleOriDest(origenNormalizado,10000)
        flowGenerator.shuffleOriDest(destinoNormalizado,10000)
        flowGenerator.generateFlowsInXML(origenNormalizado, destinoNormalizado, routeFilePath)
        #print("DUAROUTER iniciada", file=myLog2)
        sumoInterface.runDuarouter(duaroutercfgPath)
        #print("DUAROUTER finalizada", file=myLog2)

        #Evalúo la solución y, si es buena, la agrego a la lista de buenas soluciones
        #print("Simulación iniciada", file=myLog2)
        sumoInterface.runSumoSimulation(sumocfgPath)
        #print("Simulación terminada", file=myLog2)
        thisSolution = [origenNormalizado, destinoNormalizado, outputAnalysis.evaluateSolution(outputTrips)]
        #print("Analizando solución", file=myLog2)
        print(("Solución nro: " + str(n) + ";Fitness: " + str(thisSolution[SOLUTION_FITNESS_VALUE_INDEX])), file = fd)
        if len(bestSolutions)==0:
            bestSolutions.append([thisSolution[SOLUTION_ORIGIN_INDEX], thisSolution[SOLUTION_DESTINATION_INDEX], thisSolution[SOLUTION_FITNESS_VALUE_INDEX]])
        elif len(bestSolutions)<5:
            #bestSolutions.append([thisSolution[SOLUTION_ORIGIN_INDEX], thisSolution[SOLUTION_DESTINATION_INDEX], thisSolution[SOLUTION_FITNESS_VALUE_INDEX]])
            for i in range(len(bestSolutions)-1):
                if (outputAnalysis.compareSolutions(thisSolution[SOLUTION_FITNESS_VALUE_INDEX], solutionToCompare[SOLUTION_FITNESS_VALUE_INDEX], factor)==SECOND_SOLUTION_IS_BETTER):
                    bestSolutions.insert(i,[thisSolution[SOLUTION_ORIGIN_INDEX], thisSolution[SOLUTION_DESTINATION_INDEX], thisSolution[SOLUTION_FITNESS_VALUE_INDEX]])
            #print("If<10", file=myLog2)
        else:
            #print("IF>=10", file=myLog2)
            for i in range(5):
                #print("Prueba", file=myLog2)
                solutionToCompare = bestSolutions[i]
                if (outputAnalysis.compareSolutions(thisSolution[SOLUTION_FITNESS_VALUE_INDEX], solutionToCompare[SOLUTION_FITNESS_VALUE_INDEX], factor)==SECOND_SOLUTION_IS_BETTER):
                    if not(i==0):
                        #print(len(bestSolutions))
                        bestSolutions.remove(len(bestSolutions)-1)
                        bestSolutions.insert(i,[thisSolution[SOLUTION_ORIGIN_INDEX], thisSolution[SOLUTION_DESTINATION_INDEX], thisSolution[SOLUTION_FITNESS_VALUE_INDEX]])


    print("*********************************************************", file=fd)
    print("******************Detalle Mejor Solucion*****************", file=fd)
    print (bestSolutions[0], file=fd)
    fd.close
    #myLog2.close
    print(time.time())
    print ("Optimización Terminada")

if __name__ == '__main__':
    main()
