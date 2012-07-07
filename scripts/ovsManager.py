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

    #Cargo las listas de nodos orígenes y destinos y los normalizo
    origen = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.dop.xml")
    destino = flowGenerator.cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.ddp.xml")
    origenNormalizado= flowGenerator.normalize(origen, 2000)
    destinoNormalizado = flowGenerator.normalize(destino, 2000)

    #Definos las variables de Paths
    routeFilePath= "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido"
    sumocfgPath = "D:\Compartido\Proyectos\SUMO\OvS_DensidadPoblacional\models\\SNResumido.sumo.cfg"
    duaroutercfgPath = "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido.ruoc.cfg"

    sumoInterface.setSumoPath("D:\\Appls\\SUMO\\sumo-0.13.1\\bin\\sumo-gui.exe")
    sumoInterface.setSumoLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\sumo.log")
    sumoInterface.setDuarouterPath("D:\\Appls\\SUMO\\sumo-0.13.1\\bin\\duarouter.exe")
    sumoInterface.setDuarouterLogPath("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\logs\\duatouter.log")

    #Genero la población inicial de soluciones
    bestSolutions=[]
    thisSolution=[]
    optimalSolution = False
    factor = 0.01
    for n in range(100):
        #genero una solución en forma aleatoria
        origenNormalizado = flowGenerator.shuffleOriDest(origenNormalizado)
        destinoNormalizado = flowGenerator.shuffleOriDest(destinoNormalizado)
        flowGenerator.generateFlowsInXML(origenNormalizado, destinoNormalizado, routeFilePath)
        sumoInterface.runDuarouter(duaroutercfgPath)

        #Evalúo la solución y, si es buena, la agrego a la lista de buenas soluciones
        sumoInterface.runSumoSimulation(sumocfgPath)
        thisSolution = [origenNormalizado, destinoNormalizado, outputAnalysis.evaluateSolution()]
        if len(bestSolution)<10:
            bestSolutions.append(thisSolution[SOLUTION_ORIGIN_INDEX], thisSolution[SOLUTION_DESTINATION_INDEX], thisSolution[SOLUTION_FITNESS_VALUE])
        else:
            for i in range(10):
                solutionToCompare = bestSolutions[i]
                if (outputAnalysis.compareSolutions(thisSolution[SOLUTION_FITNESS_VALUE], solutionToCompare[SOLUTION_FITNESS_VALUE], factor)==SECOND_SOLUTION_IS_BETTER):
                    if not(i==0):
                        bestSolutions.remove(len(bestSolutions)-1)
                        bestSolutions.insert(i,[thisSolution[SOLUTION_ORIGIN_INDEX], thisSolution[SOLUTION_DESTINATION_INDEX], thisSolution[SOLUTION_FITNESS_VALUE]])


    #Aplico convolución sobre las soluciones de la lista de buenas soluciones,
    #y me quedo con la mejor.





        if outputAnalysis.isBestSolution(solutions[i]):
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
