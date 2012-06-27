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

def extractEdgeFromLane(lane):
    return lane[0:(lane.rindex("_"))]

def extractTripTypeFromIDTripinfo(idTripInfo):
    return idTripInfo[0:(idTripInfo.rindex("_"))]

def main():
    print(extractEdgeFromLane("123456_12"))
    print(extractTripTypeFromIDTripinfo("0_0"))

if __name__ == '__main__':
    main()
