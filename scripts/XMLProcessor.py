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

def loadNodesFromXML(filePath):
    myXMLObject = minidom.parse(filePath)
    myNodes = myXMLObject.childNodes
    return myNodes

def getNodeList(nodes, nodeLabel):
    myList = nodes[0].getElementsByTagName(nodeLabel)
    return myList

def getNodeListFromXML(filePath, nodeLabel):
    myNodes = loadNodesFromXML(filePath)
    myList = getNodeList(myNodes, nodeLabel)
    return myList

def main():
    myList = getNodeListFromXML("D:\\Compartido\\Proyectos\\SUMO\\OvS_DensidadPoblacional\\models\\nets\\SNResumido.nod.xml", "node")
    print(myList[0].attributes.keys())
    print(myList[0].attributes["x"].value)
    myList[0].attributes["pepe"] = "cualquiera"
    print(myList[0].attributes.keys())
    print(myList[0].attributes["pepe"].value)
    print(myList[0].toxml())
    print(myList[3].toxml())
    pass

if __name__ == '__main__':
    main()
