#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      teabqe
#
# Created:     20/06/2012
# Copyright:   (c) teabqe 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sumoXMLProcessor
import XMLProcessor
from consts import *

def loadTrips(tripsPath):
#-------------------------------------------------------------------------------
# TO-DO: Hacer que el parser XML pueda leer la salida como la genera el SUMO
# (es decir, con el primer nodo que sea de comentarios).
# Ideas: 1) hacer que detecte si el primer nodo es de comentario y avanzar al
# siguiente, 2)hacer que le tenga que pasar como pará¡metro el nombre del nodo
# del cual quiero obtener sus hijos
#-------------------------------------------------------------------------------
    myTrips = XMLProcessor.getNodeListFromXML(tripsPath, "tripinfo")
    return myTrips

def processTrips(trips):
#-------------------------------------------------------------------------------
# Genera una lista en la cual cada elemento es una lista conteniendo el ID del
# viaje, la hora de partida, la hora de arribo, el edge de partida, el
# edge de arribo y el tipo de viaje.
#-------------------------------------------------------------------------------
    myTrips = []

    for trip in trips:
        myTrip = []
        myTrip.append(trip.attributes["id"].value)
        myTrip.append(trip.attributes["depart"].value)
        myTrip.append(trip.attributes["arrival"].value)
        myTrip.append(sumoXMLProcessor.extractEdgeFromLane((trip.attributes["departLane"].value)))
        myTrip.append(sumoXMLProcessor.extractEdgeFromLane(trip.attributes["arrivalLane"].value))
        myTrip.append(sumoXMLProcessor.extractTripTypeFromIDTripinfo(trip.attributes["id"].value))
        myTrips.append(myTrip)

    return myTrips

def generateTripsStats(trips):
#-------------------------------------------------------------------------------
# Consolida estadísticas de cada viaje.
# Actualmente, solo devuelve el tiempo promedio de cada viaje.
#-------------------------------------------------------------------------------
    sumOfTripTime = 0

    for trip in trips:
        sumOfTripTime = float(trip[2])-float(trip[1])

    return sumOfTripTime / len(trip)

def evaluateSolution(tripsPath):
#-------------------------------------------------------------------------------
# Calcula el valor de la función FITNESS
#-------------------------------------------------------------------------------
    return generateTripsStats(processTrips(loadTrips(tripsPath)))

def compareSolutions(solutionOne, solutionTwo, indiferenceFactor):
#-------------------------------------------------------------------------------
# Determinada cual de las dos soluciones es la mejor
#-------------------------------------------------------------------------------
    varSolutions = solutionOne-solutionTwo
    varSolutions = varSolutions/solutionTwo
    varSolutions = abs(varSolutions)
    if (varSolutions<indiferenceFactor):
        return BOTH_SOLUTIONS_ARE_EQUALS
    elif ((solutionOne-solutionTwo)>0):
        return SECOND_SOLUTION_IS_BETTER
    else:
        return FIRST_SOLUTION_IS_BETTER

def main():
    myTrips = loadTrips("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\output\\SNResumido2.trip.xml")
    #print(myTrips)
    myTripsInfo = processTrips(myTrips)
    print(myTripsInfo)
    myTripsStats = generateTripsStats(myTripsInfo)
    print(myTripsStats)

    pass

if __name__ == '__main__':
    main()
