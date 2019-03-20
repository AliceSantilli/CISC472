import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import numpy as np

class helperFunctions(ScriptedLoadableModuleLogic):

  def radialDoseCalc(word):
    print word
    print "help"
    return word

  def wordPrinter(self,word):
    print word
    return word



    
    for m in range(num):
      x = int(fiducials[m,0])
      y = int(fiducials[m,1])
      z = int(fiducials[m,2])
     
      vol[z,y,x] = time
      xstart = x - (time - 1)
      xend = x + time
      ystart = y - (time - 1)
      yend = y + time 
      zstart = z - (time-1)
      zend = z + time

      amt = [0,0,0]
      
      for i in range(xstart,xend):
        amt[0] = time - abs(x -i)
        for j in range(ystart, yend):
          amt[1] = time - abs(y -j)
          for k in range(zstart, zend):
            amt[2] = time - abs(z -k)
            #vol[i,j,k] = min(amt)
            vol[k,j,i] = -1000