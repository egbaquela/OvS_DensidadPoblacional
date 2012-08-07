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
from math import floor

def cargarOrigenDestino(dataOrigin):
    myList = XMLProcessor.getNodeListFromXML(dataOrigin,"edge")

    oriDests=[]
    for node in myList:
        oriDests.append([node.attributes["id"].value, int(node.attributes["dMin"].value), int(node.attributes["dMax"].value)])
    return oriDests

def normalize(oriDestNotNormalized, targetSize):
#-------------------------------------------------------------------------------
# Devuelve una matriz cuyo primer campo es el ID, el segundo es la densidad
# mínima, el tercero la densidad máxima, el cuarto la densidad ajustada
# y el quinto el campo auxiliar
#-------------------------------------------------------------------------------
    elementsList = list(oriDestNotNormalized)

    sumElements = listMatrix.sumCols(elementsList, NODE_DENSITY_MIN_INDEX,NODE_DENSITY_MAX_INDEX)
    if (targetSize < int(sumElements[0])):
        for element in elementsList:
            element.append(int(element[NODE_DENSITY_MIN_INDEX]))
            element.append(int(element[NODE_DENSITY_MIN_INDEX]))
    elif (targetSize > int(sumElements[1])):
        for element in elementsList:
            element.append(int(element[NODE_DENSITY_MAX_INDEX]))
            element.append(int(element[NODE_DENSITY_MAX_INDEX]))
    else:
        incTargetSize = targetSize / int(sumElements[0])
        for element in elementsList:
            element.append(round(int(element[NODE_DENSITY_MIN_INDEX])*incTargetSize))
            element.append(round(int(element[NODE_DENSITY_MIN_INDEX])*incTargetSize))
# No es necesario retornar valor, ya que se modifican las sublistas originales
    return elementsList

def shuffleOriDest(oriDestNormalized, targetSize):
#-------------------------------------------------------------------------------
# Toma una lista de nodos orignenes/destinos normalizada y le asigna
# aleatoriamente su capacidad objetivo.
# Para ellos, recorre la lista asignando aleatoriamente el incremento
# en valores entre la capacidad mínima (objetivo después de la primer
# pasada) y máxima, repitiendo el proceso si sobra capacidad para asignar.
#-------------------------------------------------------------------------------
    elementsList = list(oriDestNormalized)
    sumElements = listMatrix.sumCols(elementsList, NODE_DENSITY_MIN_INDEX,NODE_DENSITY_TRG_INDEX)
    incCapacity = targetSize - sumElements[0]
    proposalCapacity = 0
    varCapacity = 0


    random.seed()
    random.shuffle(elementsList,random.random)


    for oriDest in elementsList:
        oriDest[NODE_DENSITY_TRG_INDEX]= oriDest[NODE_DENSITY_MIN_INDEX]

    bSaturedCapacity = False
    while ((incCapacity>0) and (bSaturedCapacity==False)):
        bSaturedCapacity = True
        for oriDest in elementsList:
            if (oriDest[NODE_DENSITY_TRG_INDEX]<oriDest[NODE_DENSITY_MAX_INDEX]):
                bSaturedCapacity = False
                proposalCapacity = random.randint(oriDest[NODE_DENSITY_TRG_INDEX], oriDest[NODE_DENSITY_MAX_INDEX])
                varCapacity = proposalCapacity - oriDest[NODE_DENSITY_TRG_INDEX]
                if (incCapacity < varCapacity):
                    varCapacity = incCapacity
                oriDest[NODE_DENSITY_TRG_INDEX]= varCapacity + oriDest[NODE_DENSITY_TRG_INDEX]
                incCapacity= incCapacity - varCapacity



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
    sumOfOffer = 0

    for destination in auxTo:
        sumOfDemand= sumOfDemand + destination[NODE_DENSITY_TRG_INDEX]
        destination[NODE_DENSITY_AUX_INDEX] = destination[NODE_DENSITY_TRG_INDEX]

    for origin in auxFrom:
        sumOfOffer= sumOfOffer + origin[NODE_DENSITY_TRG_INDEX]
        origin[NODE_DENSITY_AUX_INDEX] = origin[NODE_DENSITY_TRG_INDEX]

    for origin in auxFrom:
        for destination in auxTo:
            #quantityToRoute = round(sumOfDemand * (origin[NODE_DENSITY_TRG_INDEX]/sumOfOffer)*(destination[NODE_DENSITY_TRG_INDEX]/sumOfDemand))
            quantityToRoute = floor(origin[NODE_DENSITY_AUX_INDEX]*(destination[NODE_DENSITY_AUX_INDEX]/sumOfDemand))
            if (quantityToRoute>0):
                thisFlow = []
                thisFlow.append(origin[NODE_ID_INDEX])
                thisFlow.append(destination[NODE_ID_INDEX])
                thisFlow.append(0)
                thisFlow.append(1)
                thisFlow.append(quantityToRoute)
                origin[NODE_DENSITY_TRG_INDEX] = origin[NODE_DENSITY_TRG_INDEX] - quantityToRoute
                destination[NODE_DENSITY_TRG_INDEX] = destination[NODE_DENSITY_TRG_INDEX] - quantityToRoute
                myFlows.append([thisFlow[FLOW_ID_FROM_INDEX],thisFlow[FLOW_ID_TO_INDEX], \
                thisFlow[FLOW_START_TIME_INDEX],thisFlow[FLOW_END_TIME_INDEX], \
                thisFlow[FLOW_QUANTITY_INDEX]])
    return myFlows

def saveFlowsInXML(auxFlows, auxFilename):
    filename = "%s.flow.xml" % auxFilename
    fd = open(filename, "w")
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", file = fd)
    print("<flows>", file = fd)
    i=0
    for flow in auxFlows:
        print("  <flow id = \"%s\" from = \"%s\" to = \"%s\" begin = \"%s\" end = \"%s\" no = \"%s\" />" % (i, flow[0], flow [1] ,flow [2] , flow [3], flow [4]), file = fd)
        i=i+1

    print("</flows>", file = fd)
    fd.close

def generateFlowsInXML(auxFrom, auxTo, auxFilename):
    saveFlowsInXML(generateFlows(auxFrom, auxTo),auxFilename)

def main():
#    destinos = cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.ddp.xml")
#    origenes = cargarOrigenDestino("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\data\\SNResumido.dop.xml")
#    poblacionObjetivo = 1248
#    destinosNormalizados = normalize(destinos, poblacionObjetivo)
#    origenesNormalizados = normalize(origenes, poblacionObjetivo)
#    myFlows = generateInitialFlows(origenesNormalizados, destinosNormalizados)
#    print(origenes)
#    saveFlowsInXML(myFlows, "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido")

    a = [['fsalidacruce-01-01', 0, 100,0], ['fentradacruce-01-01', 50, 100, 0], ['fsalidacruce-01-02', 25, 150, 0]]
    shuffleOriDest(a,100)
    print(a)
    pass

if __name__ == '__main__':
    main()
