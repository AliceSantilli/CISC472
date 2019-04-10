import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import numpy as np
#import helperFunctions as hF 

#
# LinearDistribution
     
    

class LinearDistribution(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "LinearDistribution" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It performs a simple thresholding on the input volume and optionally captures a screenshot.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# LinearDistributionWidget
#

class LinearDistributionWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  def onCalcButtonClicked(self):
    logic = LinearDistributionLogic()
    Image = self.inputSelector.currentNode()
    cloneVolume = self.outputSelector.currentNode()
    result = logic.calcDoseRadius(Image, cloneVolume)
    #qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result2)

  def onNeedlePlanButtonClicked(self):
    logic = LinearDistributionLogic()
    entryFiducial = self.entry.value
    endFiducial = self.end.value
    result = logic.setNeedlePlan(entryFiducial, endFiducial)
    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #Print something to parameter screen 

    #INTRO 
    intro = qt.QLabel("Place Fiducials as the Ablation points \nonto the segmented Tumour (red) \n ")
    parametersFormLayout.addWidget(intro)

    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.outputSelector.selectNodeUponCreation = True
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)


    # connections
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)


    # Add vertical spacer
    self.layout.addStretch(1)

    #CALC BUTTON
    calcButton = qt.QPushButton("Calculate Ablation")
    calcButton.toolTip = "Print 'Hello World' in standard output"
    parametersFormLayout.addWidget(calcButton)
    calcButton.connect('clicked(bool)', self.onCalcButtonClicked)
    self.layout.addStretch(1)
    self.calcButton = calcButton

    #SET UP NEEDLE PLAN 
    entryText = qt.QLabel("\n Once you are happy with the ablation of the tumor, \nset new fiducials as entry points.\n")
    parametersFormLayout.addWidget(entryText)


    #needleBox1 = qt.QHBoxLayout()
    entryLabel= qt.QLabel("Entry Point = Fiducial ")
    entry = qt.QSpinBox()
    entry.setMinimum(1)
    parametersFormLayout.addRow(entryLabel, entry)
    self.entry = entry
    end = qt.QSpinBox()
    endLabel = qt.QLabel("Needle Tip = Fiducial ")
    end.setMinimum(1)
    parametersFormLayout.addRow(endLabel, end)
    self.end = end


    #NEEDLE PLAN BUTTON
    needleButton = qt.QPushButton("Set a new Needle Plan")
    needleButton.toolTip = "Print 'Hello World' in standard output"
    parametersFormLayout.addWidget(needleButton)
    needleButton.connect('clicked(bool)', self.onNeedlePlanButtonClicked)
    self.layout.addStretch(1)
    self.needleButton = needleButton


  def cleanup(self):
    pass


  def onSelect(self):
    pass
 

#
# LinearDistributionLogic
#

class LinearDistributionLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def getNeedlePlan(self,entry, end):

    f = slicer.util.getNode("F")
    entryPoint1 = [0,0,0]
    f.GetNthFiducialPosition(entry-1, entryPoint1)
    endPoint1 = [0,0,0]
    f.GetNthFiducialPosition(end-1, endPoint1)
    
    lineSource = vtk.vtkLineSource()
    lineSource.SetPoint1(entryPoint1[0],entryPoint1[1],entryPoint1[2])
    lineSource.SetPoint2(endPoint1[0],endPoint1[1],endPoint1[2])
    lineSource.Update()
    tubeFilter = vtk.vtkTubeFilter()
    tubeFilter.SetInputConnection(lineSource.GetOutputPort())
    tubeFilter.SetRadius(0.5) #Default is 0.5
    tubeFilter.SetNumberOfSides(100)
    tubeFilter.Update()

    #try:
     # model = slicer.util.getNode('Model')
      #model.SetAndObservePolyData(tubeFilter.GetOutput())
    #except:
    modelsLogic = slicer.modules.models.logic()
    model = modelsLogic.AddModel(tubeFilter.GetOutput())
    modelDisplayNode = model.GetDisplayNode()
    modelDisplayNode.SetSliceIntersectionVisibility(True)
    modelDisplayNode.SetSliceIntersectionThickness(3)
    modelDisplayNode.SetColor(1,1,0)
    modelDisplayNode.SetOpacity(1)


  def setNeedlePlan(self, entry, end):

    self.getNeedlePlan(entry, end)

    return "done"


  def checkinSphere(self, pt,radius,center):
      x=pt[0]
      y=pt[1]
      z=pt[2]
      cx=center[0]
      cy=center[1]
      cz=center[2]
      if (pow(( x-cx ),2) + pow((y-cy),2) + pow((z-cz),2)) <= pow(radius,2):
          return True
      else:
          return False

  def radialDose(self,fid, doseMap, vol, IjktoRasMatrix,originalPointinRAS):

    rad = max(doseMap[0])
    for i in range(-rad, rad + 1):
      for j in range(-rad, rad + 1):
        for k in range(-rad, rad + 1):
          pos = np.array([i, j, k])
          pt = pos + np.array(fid)  # point in ijk
          for sphereradindex in range(len(doseMap[0])):
            appended_pt = np.append(pt, 1)
            pt_RAS = IjktoRasMatrix.MultiplyDoublePoint(appended_pt)
            euclDist = np.linalg.norm(np.array(pt_RAS[0:3]) - np.array(originalPointinRAS))
            if euclDist <= sphereradindex:
              if vol[int(pt[2]), int(pt[1]), int(pt[0])] == -1000:
                vol[int(pt[2]), int(pt[1]), int(pt[0])] = doseMap[1][int(sphereradindex)]
              else:
                vol[int(pt[2]), int(pt[1]), int(pt[0])] += doseMap[1][int(sphereradindex)]



  def calcDoseRadius(self, Image, cloneVolume):
    #Image = '03'
    time = 5 # burning time 
    doseMap=[[2, 4, 6, 8, 10], [5, 4, 3, 2, 1]]

    #Image = self.inputSelector.currentNode()
    #vol = self.outputSelector.currentNode()
    #print(cloneVolume)
    vol = slicer.util.array(cloneVolume.GetID())
    vol.fill(-1000)

    f = slicer.util.getNode("F")
    num = f.GetNumberOfFiducials()

    fiducials = np.zeros((num, 3)) 
    RastoIjkMatrix = vtk.vtkMatrix4x4()
    Image.GetRASToIJKMatrix(RastoIjkMatrix)
    IjktoRasMatrix = vtk.vtkMatrix4x4()
    Image.GetIJKToRASMatrix(IjktoRasMatrix)

    for i in range(num):
      pos = [0, 0, 0]
      f.GetNthFiducialPosition(i, pos)
      originalPointinRAS=pos
      pos = np.append(pos, 1)

      p_IJK = RastoIjkMatrix.MultiplyDoublePoint(pos)
      print p_IJK
      self.radialDose(p_IJK[0:3], doseMap, vol, IjktoRasMatrix,originalPointinRAS)

    cloneVolume.Modified()



  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('LinearDistributionTest-Start','MyScreenshot',-1)

    logging.info('Processing completed')

    return True


class LinearDistributionTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_LinearDistribution1()

  def test_LinearDistribution1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = LinearDistributionLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
