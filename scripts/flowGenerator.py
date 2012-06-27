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

    sumElements = listMatrix.sumCols(elementsList, 1,3)
    incTargetSize = targetSize / int(sumElements[1])

    for element in elementsList:
        element.append(round(int(element[1])*incTargetSize))
# No es necesario retornar valor, ya que se modifican las sublistas originales
    return elementsList

def generateInitialFlows(auxFrom, auxTo):
#-------------------------------------------------------------------------------
# Genera una matriz de flujos como el producto cartesiano de los orÃƒÆ’Ã‚Â­genes y
# destinos. El resultado es una lista donde cada campo es otra lista con la
# siguiente estructura:
#   [Id From, Id To, Inicio Ruteo, Fin Ruteo, Cantidad a rutear]
# Este mÃƒÆ’Ã‚Â©todo genera flujos tratando de lograr el objetivo de un solo flujo
# por origen y por destino.
#-------------------------------------------------------------------------------
    myFlows = []

    for origin in auxFrom:
        for destination in auxTo:
            thisFlow = []
            thisFlow.append(origin[0])
            thisFlow.append(destination[0])
            thisFlow.append(0)
            thisFlow.append(300)
            if (int(origin[1])>=int(destination[1])):
                thisFlow.append(destination[1])
            else:
                thisFlow.append(origin[1])
            origin[1] = str(int(origin[1]) - int(thisFlow[4]))
            destination[1] = str(int(destination[1]) - int(thisFlow[4]))
            myFlows.append([thisFlow[0],thisFlow[1],thisFlow[2],thisFlow[3], \
            thisFlow[4]])
    return myFlows

def generateFlows(auxFrom, auxTo):
#-------------------------------------------------------------------------------
# Genera una matriz de flujos como el producto cartesiano de los orÃƒÆ’Ã‚Â­genes y
# destinos. El resultado es una lista donde cada campo es otra lista con la
# siguiente estructura:
#   [Id From, Id To, Inicio Ruteo, Fin Ruteo, Cantidad a rutear]
# Este mÃ©todo genera flujos desde cada origen a todos los destino en la misma
# proporciÃ³n que se distribuye la demanda.
#-------------------------------------------------------------------------------
    myFlows = []
    sumOfDemand = 0

    for destination in auxTo:
        sumOfDemand= sumOfDemand + destination[1]

    for origin in auxFrom:
        for destination in auxTo:
            thisFlow = []
            thisFlow.append(origin[0])
            thisFlow.append(destination[0])
            thisFlow.append(0)
            thisFlow.append(300)
            thisFlow.append(round(origin[1]*destination[1]/sumOfDemand))
            origin[1] = origin[1] - thisFlow[4]
            destination[1] = destination[1] - thisFlow[4]
            myFlows.append([thisFlow[0],thisFlow[1],thisFlow[2],thisFlow[3], \
            thisFlow[4]])
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
    poblacionObjetivo = 2000
    destinosNormalizados = normalize(destinos, poblacionObjetivo)
    origenesNormalizados = normalize(origenes, poblacionObjetivo)
    myFlows = generateInitialFlows(origenesNormalizados, destinosNormalizados)
    print(myFlows)
    saveFlowsInXML(myFlows, "D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\routes\\SNResumido")

    pass

if __name__ == '__main__':
    main()
