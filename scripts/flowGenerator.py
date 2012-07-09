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

from xml.dom import minidom
import XMLProcessor
import listMatrix
import random
from consts import *

def cargarOrigenDestino(dataOrigin):
    myList = XMLProcessor.getNodeListFromXML(dataOrigin,"edge")

    oriDests=[]
    for node in myList:
        oriDests.append([node.attributes["id"].value, int(node.attributes["dMin"].value), int(node.attributes["dMax"].value)])
    return oriDests

def normalize(oriDestNotNormalized, targetSize):
#-------------------------------------------------------------------------------
# Devuelve una matriz cuyo primer campo es el ID, el segundo es la densidad
# mínima, el tercero la densidad máxima y el cuarto la densidad ajustada.
#-------------------------------------------------------------------------------
    elementsList = list(oriDestNotNormalized)

    sumElements = listMatrix.sumCols(elementsList, NODE_DENSITY_MIN_INDEX,NODE_DENSITY_MAX_INDEX)
    if (targetSize < int(sumElements[0])):
        for element in elementsList:
            element.append(int(element[NODE_DENSITY_MIN_INDEX]))
    elif (targetSize > int(sumElements[1])):
        for element in elementsList:
            element.append(int(element[NODE_DENSITY_MAX_INDEX]))
    else:
        incTargetSize = targetSize / int(sumElements[0])
        for element in elementsList:
            element.append(round(int(element[NODE_DENSITY_MIN_INDEX])*incTargetSize))
# No es necesario retornar valor, ya que se modifican las sublistas originales
    return elementsList

def shuffleOriDest(oriDestNormalized):
    elementsList = list(oriDestNormalized)
    sumElements = listMatrix.sumCols(elementsList, NODE_DENSITY_MIN_INDEX,NODE_DENSITY_TRG_INDEX)
    targetSize = sumElements[2]

    for oriDest in elementsList:
        if (oriDest[NODE_DENSITY_MIN_INDEX]==oriDest[NODE_DENSITY_MAX_INDEX]):
            oriDest[NODE_DENSITY_TRG_INDEX]= oriDest[NODE_DENSITY_MIN_INDEX]
        else:
            oriDest[NODE_DENSITY_TRG_INDEX]= random.randint(oriDest[NODE_DENSITY_MIN_INDEX], oriDest[NODE_DENSITY_MAX_INDEX])

    newElementList = normalize(elementsList, targetSize)

    return newElementList


def generateInitialFlows(auxFrom, auxTo):
#-------------------------------------------------------------------------------
# Genera una matriz de flujos como el producto cartesiano de los orígenes y
# destinos. El resultado es una lista donde cada campo es otra lista con la
# siguiente estructura:
#   [Id From, Id To, Inicio Ruteo, Fin Ruteo, Cantidad a rutear]
# Este método genera flujos tratando de lograr el objetivo de un solo flujo
# por origen y por destino.
#-------------------------------------------------------------------------------
    myFlows = []

    for origin in auxFrom:
        for destination in auxTo:
            thisFlow = []
            thisFlow.append(origin[NODE_ID_INDEX])
            thisFlow.append(destination[NODE_ID_INDEX])
            thisFlow.append(0)
            thisFlow.append(300)
            if (int(origin[NODE_DENSITY_MIN_INDEX])>=int(destination[NODE_DENSITY_MIN_INDEX])):
                thisFlow.append(destination[NODE_DENSITY_MIN_INDEX])
            else:
                thisFlow.append(origin[NODE_DENSITY_MIN_INDEX])
            origin[NODE_DENSITY_MIN_INDEX] = str(int(origin[NODE_DENSITY_MIN_INDEX]) - int(thisFlow[FLOW_QUANTITY_INDEX]))
            destination[NODE_DENSITY_MIN_INDEX] = str(int(destination[NODE_DENSITY_MIN_INDEX]) - int(thisFlow[FLOW_QUANTITY_INDEX]))
            myFlows.append([thisFlow[FLOW_ID_FROM_INDEX],thisFlow[FLOW_ID_TO_INDEX], \
            thisFlow[FLOW_START_TIME_INDEX],thisFlow[FLOW_END_TIME_INDEX], \
            thisFlow[FLOW_QUANTITY_INDEX]])
    return myFlows

def generateFlows(auxFrom, auxTo):
#-------------------------------------------------------------------------------
# Genera una matriz de flujos como el producto cartesiano de los orígenes y
# destinos. El resultado es una lista donde cada campo es otra lista con la
# siguiente estructura:
#   [Id From, Id To, Inicio Ruteo, Fin Ruteo, Cantidad a rutear]
# Este método genera flujos desde cada origen a todos los destino en la misma
# proporción que se distribuye la demanda.
#-------------------------------------------------------------------------------
    myFlows = []
    sumOfDemand = 0

    for destination in auxTo:
        sumOfDemand= sumOfDemand + destination[NODE_DENSITY_TRG_INDEX]

    for origin in auxFrom:
        for destination in auxTo:
            thisFlow = []
            thisFlow.append(origin[NODE_ID_INDEX])
            thisFlow.append(destination[NODE_ID_INDEX])
            thisFlow.append(0)
            thisFlow.append(300)
            thisFlow.append(round(origin[NODE_DENSITY_TRG_INDEX]*destination[NODE_DENSITY_TRG_INDEX]/sumOfDemand))
            origin[NODE_DENSITY_TRG_INDEX] = origin[NODE_DENSITY_TRG_INDEX] - thisFlow[FLOW_QUANTITY_INDEX]
            destination[NODE_DENSITY_TRG_INDEX] = destination[NODE_DENSITY_TRG_INDEX] - thisFlow[FLOW_QUANTITY_INDEX]
            myFlows.append([thisFlow[FLOW_ID_FROM_INDEX],thisFlow[FLOW_ID_TO_INDEX], \
            thisFlow[FLOW_START_TIME_INDEX],thisFlow[FLOW_END_TIME_INDEX], \
            thisFlow[FLOW_QUANTITY_INDEX]])
    return myFlows

def saveFlowsInXML(auxFlows, auxFilename):
    filename = "%s.flow.xml" % auxFilename
    fd = open(filename, "w")
    print("<?xml version=""1.0"" encoding=""iso-8859-1""?>", file = fd)
    print("<flows>", file = fd)
    i=0
    for flow in auxFlows:
        print("  <flow id = \"%s\" from = \"%s\" to = \"%s\" begin = \"%s\"end = \"%s\" no = \"%s\" />" % (i, flow[0], flow [1] ,flow [2] , flow [3], flow [4]), file = fd)
        i=i+1

    print("</flows>", file = fd)
    fd.close

def generateFlowsInXML(auxFrom, auxTo, auxFilename):
    saveFlowsInXML(generateFlows(auxFrom, auxTo),auxFilename)

def main():
    destinos = cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.ddp.xml")
    origenes = cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.dop.xml")
    poblacionObjetivo = 1248
    destinosNormalizados = normalize(destinos, poblacionObjetivo)
    origenesNormalizados = normalize(origenes, poblacionObjetivo)
    myFlows = generateInitialFlows(origenesNormalizados, destinosNormalizados)
    print(origenes)
    saveFlowsInXML(myFlows, "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido")

    pass

if __name__ == '__main__':
    main()
