#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      teabqe
#
# Created:     18/06/2012
# Copyright:   (c) teabqe 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# MÃƒÆ’Ã‚Â³dulo para procesar matrices formadas por listas incluidas en listas.
# Una lista-matriz es una lista incluida como campo en otra lista.
# El ÃƒÆ’Ã‚Â­ndice de la lista externa representa a las filas (los registros) y
# los de las listas anidades a las columnas (campos). Los valores de la lista
# interna son los datos almacenados para ese registro y campo.
# Las matrices difinidas de esta forma no tienen que ser rectangulares
#-------------------------------------------------------------------------------

def isNumber(x):
    try:
        float(x)
    except ValueError:
        return False
    return True

def sumCols(auxListMatrix, auxRowFrom, auxRowTo):
    sumOfTheCols= [0]*(auxRowTo-auxRowFrom)

    for myRow in auxListMatrix:
        i=0
        for myData in myRow[auxRowFrom:auxRowTo]:
            sumOfTheCols[i] = int(sumOfTheCols[i]) + int(myData)
            i=i+1

    return sumOfTheCols



def sumRows(auxListMatrix):
    sumOfTheRows=[]
    myList=[]
    i=0
    for myColsList in auxListMatrix:
        sumOfTheRows.append(0)
        for myValue in myColsList:
            sumOfTheRows[i] = int(sumOfTheRows[i]) + int(myValue)
        i= i+1
    return sumOfTheRows


def main():
    row1 = [1,2,3]
    row2 = [4,5,6]
    row3 = [7,8,9]
    row4 = [10,11,12]
    listMatrix=[]
    listMatrix.append(row1)
    listMatrix.append(row2)
    listMatrix.append(row3)
    listMatrix.append(row4)

    print("Matriz")
    print(listMatrix)
    print("Suma de filas")
    print(sumRows(listMatrix))
    print("Suma de columnas")
    print(sumCols(listMatrix, 0, (len(listMatrix)-1)))
    pass

if __name__ == '__main__':
    main()