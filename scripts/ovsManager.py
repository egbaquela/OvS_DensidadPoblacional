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

def main():

    #Cargo las listas de nodos orígenes y destinos y los normalizo
    origen = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.dop.xml")
    destino = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.ddp.xml")
    origenNormalizado= flowGenerator.normalize(origen, 10000)
    destinoNormalizado = flowGenerator.normalize(destino, 10000)

    #Definos las variables de Paths
    routeFilePath= "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido"
    sumocfgPath = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\SNResumido.sumo.cfg"
    duaroutercfgPath = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido.ruoc.cfg"
    outputTrips = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\output\\SNResumido.trip.xml"

    sumoInterface.setSumoPath("D:\\Appls\\SUMO\\sumo-0.15.0\\bin\\sumo-gui.exe")
    sumoInterface.setSumoLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\ulogs\\sumo.log")
    sumoInterface.setDuarouterPath("D:\\Appls\\SUMO\\sumo-0.15.0\\bin\\duarouter.exe")
    sumoInterface.setDuarouterLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\duatouter.log")

    #Creo/abro el archivo para grabar las soluciones encontradas
    fd = open("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\output\\output.log", "w")
    myLog2 = open("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\MyLog2.log", "a")

    #Genero la población inicial de soluciones
    bestSolutions=[]
    thisSolution=[]
    optimalSolution = False
    factor = 0.01
    for n in range(1):
        #genero una solución en forma aleatoria
        flowGenerator.shuffleOriDest(origenNormalizado,10000)
        print(listMatrix.sumCols(origenNormalizado, NODE_DENSITY_MIN_INDEX,NODE_DENSITY_TRG_INDEX))
        flowGenerator.shuffleOriDest(destinoNormalizado,10000)
        print("Shuffle Destino Finalizado")
        print(listMatrix.sumCols(origenNormalizado, NODE_DENSITY_MIN_INDEX,NODE_DENSITY_TRG_INDEX))
        flowGenerator.generateFlowsInXML(origenNormalizado, destinoNormalizado, routeFilePath)
        print(listMatrix.sumCols(origenNormalizado, NODE_DENSITY_MIN_INDEX,NODE_DENSITY_TRG_INDEX))
        print("DUAROUTER iniciada", file=myLog2)
        sumoInterface.runDuarouter(duaroutercfgPath)
        print("DUAROUTER finalizada", file=myLog2)
        print(listMatrix.sumCols(origenNormalizado, NODE_DENSITY_MIN_INDEX,NODE_DENSITY_TRG_INDEX))

        #Evalúo la solución y, si es buena, la agrego a la lista de buenas soluciones
        print("Simulación iniciada", file=myLog2)
        sumoInterface.runSumoSimulation(sumocfgPath)
        print("Simulación terminada", file=myLog2)
        thisSolution = [origenNormalizado, destinoNormalizado, outputAnalysis.evaluateSolution(outputTrips)]
        print("Analizando solución", file=myLog2)
        print(str(thisSolution[SOLUTION_FITNESS_VALUE_INDEX]), file = fd)
        if len(bestSolutions)<10:
            bestSolutions.append([thisSolution[SOLUTION_ORIGIN_INDEX], thisSolution[SOLUTION_DESTINATION_INDEX], thisSolution[SOLUTION_FITNESS_VALUE_INDEX]])
            print("If<10", file=myLog2)
        else:
            print("IF>=10", file=myLog2)
            for i in range(10):
                print("Prueba", file=myLog2)
                solutionToCompare = bestSolutions[i]
                if (outputAnalysis.compareSolutions(thisSolution[SOLUTION_FITNESS_VALUE_INDEX], solutionToCompare[SOLUTION_FITNESS_VALUE_INDEX], factor)==SECOND_SOLUTION_IS_BETTER):
                    if not(i==0):
                        bestSolutions.remove(len(bestSolutions)-1)
                        bestSolutions.insert(i,[thisSolution[SOLUTION_ORIGIN_INDEX], thisSolution[SOLUTION_DESTINATION_INDEX], thisSolution[SOLUTION_FITNESS_VALUE_INDEX]])


    print("Solución Encontrada")
    fd.close
    myLog2.close

#    a = [['fsalidacruce-01-01', 0, 100,0], ['fentradacruce-01-01', 50, 100, 0], ['fsalidacruce-01-02', 25, 150, 0]]
#    flowGenerator.shuffleOriDest(a,100)
#    print(a)
#    flowGenerator.shuffleOriDest(a,100)
#    print(a)
#    flowGenerator.shuffleOriDest(a,100)
#    print(a)
#    pass

if __name__ == '__main__':
    main()
