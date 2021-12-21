#!/usr/bin/env python3
import sys
import Scanner
if __name__=="__main__":
    if sys.argv[1] =="1":
        Scanner.ScanWithShowing()
    elif sys.argv[1] =="2":
        Scanner.ScanWithNoShowing()
    elif sys.argv[1] =="3":
        Scanner.ResetSessionPoints()
    elif sys.argv[1] == "4":
        Scanner.AbsencesSetToZero(sys.argv[2])