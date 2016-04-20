import sys
import vtk
import numpy
import nibabel
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MainWindow import Ui_uMainWindow
import ctypes

class MyMainWindow(QtGui.QMainWindow):
  def __init__(self,parent=None):
    QtGui.QMainWindow.__init__(self)
    self.ui = Ui_uMainWindow()
    self.ui.setupUi(self)  
    
#Buttons to load data
    self.ui.bLoadOriginal.clicked.connect(self.openOriginalBrainFile)
    self.ui.bLoadEnhanced.clicked.connect(self.openEnhancedBrainFile)
    self.ui.bLoadGold.clicked.connect(self.openGoldSegmFile)
    self.ui.bLoadSegmentation.clicked.connect(self.openSegmFile)
    
#Button to compute similarity metrics
    self.ui.bComputeMetrics.clicked.connect(self.computeMetrics)

#Original brain side    
    #Buttons for 3d views
    self.ui.b3dGold.clicked.connect(self.show3dGold)
    
    #Buttons to toggle segmentations
    self.ui.chOriginalGold.stateChanged.connect(self.toggleOriginalGold)
    self.ui.chOriginalSegm.stateChanged.connect(self.toggleOriginalSegm)
    
    #Add the axial view of the original brain to its corresponding widget
    self.originalAxBrainRenderer = vtk.vtkRenderer()
    self.originalAxBrainWidgetWindowInteractor = QVTKRenderWindowInteractor(self.ui.wOriginalAxial)
    self.originalAxBrainWidgetWindowInteractor.GetRenderWindow().AddRenderer(self.originalAxBrainRenderer)        
    self.originalAxBrainInteractor = self.originalAxBrainWidgetWindowInteractor.GetRenderWindow().GetInteractor()      
    
    #Axial view of original brain controls   
    self.ui.vsVerAxOriginal.valueChanged.connect(self.moveHorAxOriginal)
    self.ui.vsHorAxOriginal.valueChanged.connect(self.moveVerAxOriginal)
    self.ui.vsZAxOriginal.valueChanged.connect(self.moveZAxOriginal)  
    
    #Add the coronal view of the original brain to its corresponding widget
    self.originalCorBrainRenderer = vtk.vtkRenderer()
    self.originalCorBrainWidgetWindowInteractor = QVTKRenderWindowInteractor(self.ui.wOriginalCoronal)
    self.originalCorBrainWidgetWindowInteractor.GetRenderWindow().AddRenderer(self.originalCorBrainRenderer)        
    self.originalCorBrainInteractor = self.originalCorBrainWidgetWindowInteractor.GetRenderWindow().GetInteractor()      
    
    #Coronal view of original brain controls   
    self.ui.vsVerCorOriginal.valueChanged.connect(self.moveHorCorOriginal)
    self.ui.vsHorCorOriginal.valueChanged.connect(self.moveVerCorOriginal)
    self.ui.vsZCorOriginal.valueChanged.connect(self.moveZCorOriginal)  

    #Add the sagittal view of the original brain to its corresponding widget
    self.originalSagBrainRenderer = vtk.vtkRenderer()
    self.originalSagBrainWidgetWindowInteractor = QVTKRenderWindowInteractor(self.ui.wOriginalSagital)
    self.originalSagBrainWidgetWindowInteractor.GetRenderWindow().AddRenderer(self.originalSagBrainRenderer)        
    self.originalSagBrainInteractor = self.originalSagBrainWidgetWindowInteractor.GetRenderWindow().GetInteractor()      
    
    #Sagittal view of original brain controls   
    self.ui.vsVerSagOriginal.valueChanged.connect(self.moveHorSagOriginal)
    self.ui.vsHorSagOriginal.valueChanged.connect(self.moveVerSagOriginal)
    self.ui.vsZSagOriginal.valueChanged.connect(self.moveZSagOriginal)        
    
    #Segmentations transparency controls   
    self.ui.vsGoldTransparency.valueChanged.connect(self.moveGoldTransparency)
    self.ui.vsSegTransparency.valueChanged.connect(self.moveSegTransparency)    
    
    #Window and level buttons
    self.ui.vsOriginalWindow.valueChanged.connect(self.moveOriginalWindow)
    self.ui.vsOriginalLevel.valueChanged.connect(self.moveOriginalLevel)    
    
#Enhanced brain side       
    #Buttons for 3d view with intersections
    self.ui.b3dColored.clicked.connect(self.show3dColored)

    #Buttons to toggle segmentations
    self.ui.chEnhancedGold.stateChanged.connect(self.toggleEnhancedGold)
    self.ui.chEnhancedSegm.stateChanged.connect(self.toggleEnhancedSegm)

    #Add the axial view of the enhanced brain to its corresponding widget
    self.enhancedAxBrainRenderer = vtk.vtkRenderer()
    self.enhancedAxBrainWidgetWindowInteractor = QVTKRenderWindowInteractor(self.ui.wEnhancedAxial)
    self.enhancedAxBrainWidgetWindowInteractor.GetRenderWindow().AddRenderer(self.enhancedAxBrainRenderer)        
    self.enhancedAxBrainInteractor = self.enhancedAxBrainWidgetWindowInteractor.GetRenderWindow().GetInteractor()      
    
    #Axial view of enhanced brain controls   
    self.ui.vsVerAxEnhanced.valueChanged.connect(self.moveHorAxEnhanced)
    self.ui.vsHorAxEnhanced.valueChanged.connect(self.moveVerAxEnhanced)
    self.ui.vsZAxEnhanced.valueChanged.connect(self.moveZAxEnhanced)  
    
    #Add the coronal view of the enhanced brain to its corresponding widget
    self.enhancedCorBrainRenderer = vtk.vtkRenderer()
    self.enhancedCorBrainWidgetWindowInteractor = QVTKRenderWindowInteractor(self.ui.wEnhancedCoronal)
    self.enhancedCorBrainWidgetWindowInteractor.GetRenderWindow().AddRenderer(self.enhancedCorBrainRenderer)        
    self.enhancedCorBrainInteractor = self.enhancedCorBrainWidgetWindowInteractor.GetRenderWindow().GetInteractor()      
    
    #Coronal view of enhanced brain controls   
    self.ui.vsVerCorEnhanced.valueChanged.connect(self.moveHorCorEnhanced)
    self.ui.vsHorCorEnhanced.valueChanged.connect(self.moveVerCorEnhanced)
    self.ui.vsZCorEnhanced.valueChanged.connect(self.moveZCorEnhanced)  

    #Add the sagittal view of the enhanced brain to its corresponding widget
    self.enhancedSagBrainRenderer = vtk.vtkRenderer()
    self.enhancedSagBrainWidgetWindowInteractor = QVTKRenderWindowInteractor(self.ui.wEnhancedSagital)
    self.enhancedSagBrainWidgetWindowInteractor.GetRenderWindow().AddRenderer(self.enhancedSagBrainRenderer)        
    self.enhancedSagBrainInteractor = self.enhancedSagBrainWidgetWindowInteractor.GetRenderWindow().GetInteractor()      
    
    #Sagittal view of enhanced brain controls   
    self.ui.vsVerSagEnhanced.valueChanged.connect(self.moveHorSagEnhanced)
    self.ui.vsHorSagEnhanced.valueChanged.connect(self.moveVerSagEnhanced)
    self.ui.vsZSagEnhanced.valueChanged.connect(self.moveZSagEnhanced)      
    
    #Segmentations transparency controls   
    self.ui.vsGoldTransparencyEnc.valueChanged.connect(self.moveGoldTransparencyEnc)
    self.ui.vsSegTransparencyEnc.valueChanged.connect(self.moveSegTransparencyEnc)    
    
    #Window and level buttons
    self.ui.vsEnhancedWindow.valueChanged.connect(self.moveEnhancedWindow)
    self.ui.vsEnhancedLevel.valueChanged.connect(self.moveEnhancedLevel)        
    
  #Read a niftii image  
  def openNiftiiImage (self, fileName):    
    img = nibabel.load(str(fileName))
    imgData = img.get_data()
    imgDataType = imgData.dtype
    imgDataShape = imgData.shape
    
    dataImporter = vtk.vtkImageImport()
    dataImporter.SetDataScalarTypeToShort()    
    if imgDataType is None:
        imgDataType = imgData.type
    if imgDataType == numpy.float64:
        dataImporter.SetDataScalarTypeToDouble()
    elif imgDataType == numpy.float32:
        dataImporter.SetDataScalarTypeToFloat()
    elif imgDataType == numpy.int32:
        dataImporter.SetDataScalarTypeToInt()
    elif imgDataType == numpy.int16:
        dataImporter.SetDataScalarTypeToShort()
    elif imgDataType == numpy.uint8:
        dataImporter.SetDataScalarTypeToUnsignedChar()
    else:
        dataImporter.SetDataScalarTypeToDouble()
        imgData = imgData.astype(numpy.float64)

    dataString = imgData.flatten(order='F').tostring()
    if imgDataType.byteorder == '>':
        # Fix byte order
        dflat_l = imgData.flatten(order='F').tolist()
        format_string = '<%id' % len(dflat_l)
        dataString = struct.pack(format_string, *dflat_l)            
    
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.CopyImportVoidPointer(dataString, len(dataString))    
           
    dataImporter.SetDataExtent(0, imgDataShape[0] - 1, 0, imgDataShape[1] - 1, 0, imgDataShape[2] - 1)
    dataImporter.SetWholeExtent(0, imgDataShape[0] - 1, 0, imgDataShape[1] - 1, 0, imgDataShape[2] - 1)
    dataImporter.SetDataSpacing(img.get_header().get_zooms()[0], img.get_header().get_zooms()[1], img.get_header().get_zooms()[2])    
    dataImporter.Update()
    tempData = dataImporter.GetOutput()
    newData = vtk.vtkImageData()
    newData.DeepCopy(tempData)    
    
    return newData
  
  def orientImage (self, newData, orientation):
    (xMin, xMax, yMin, yMax, zMin, zMax) = newData.GetWholeExtent()
    (xSpacing, ySpacing, zSpacing) = newData.GetSpacing()
    (x0, y0, z0) = newData.GetOrigin()
  
    center = [x0 + xSpacing * 0.5 * (xMin + xMax),
                      y0 + ySpacing * 0.5 * (yMin + yMax),
                      z0 + zSpacing * 0.5 * (zMin + zMax)]
    
    axial = vtk.vtkMatrix4x4()
    axial.DeepCopy((1, 0, 0,center[0] ,
                    0, -1, 0,center[1] ,
                    0, 0, 1,center[2],
                    0, 0, 0, 1))
    
    coronal = vtk.vtkMatrix4x4()
    coronal.DeepCopy((1, 0, 0, center[0],
                      0, 0, 1, center[1],
                      0, 1, 0, center[2],
                      0, 0, 0, 1))
    
    sagittal = vtk.vtkMatrix4x4()
    sagittal.DeepCopy((0, 0,-1, center[0],
                       1, 0, 0, center[1],
                       0, 1, 0,center[2] ,
                       0, 0, 0, 1))

    
    reslice = vtk.vtkImageReslice()
    reslice.SetInput(newData)
    reslice.SetOutputDimensionality(3)
    reslice.SetResliceAxesOrigin(0,0,0)
    if orientation=='axial':
      reslice.SetResliceAxes(axial)
    elif orientation=='sagittal':
      reslice.SetResliceAxes(sagittal)
    elif orientation=='coronal':
      reslice.SetResliceAxes(coronal)
    reslice.SetInterpolationModeToCubic()
    reslice.Update()
    return reslice.GetOutput()
    
  def openOriginalBrainFile (self):
    fileName = QtGui.QFileDialog.getOpenFileName(self,'Open file','/home/rphellan/UofC/Datasets/OriginalBrainsAndGT')          
    newData = self.openNiftiiImage(fileName)
    
    #Set window and level max and min
    self.ui.vsOriginalWindow.setMinimum(0)
    self.ui.vsOriginalWindow.setMaximum(newData.GetScalarRange()[1])
    
    self.ui.vsOriginalLevel.setMinimum(0)
    self.ui.vsOriginalLevel.setMaximum(newData.GetScalarRange()[1])    
    
    #Set the axial original view
    self.ui.vsHorAxOriginal.setMinimum(0 - newData.GetDimensions()[0] / 2)
    self.ui.vsHorAxOriginal.setMaximum(newData.GetDimensions()[0] / 2)
    self.ui.vsVerAxOriginal.setMinimum(0 - newData.GetDimensions()[1] / 2)
    self.ui.vsVerAxOriginal.setMaximum(newData.GetDimensions()[1] / 2)
    self.ui.vsZAxOriginal.setMinimum(0)
    self.ui.vsZAxOriginal.setMaximum(newData.GetDimensions()[2] - 1)    
  
    mapperAxial = vtk.vtkImageMapper()
    mapperAxial.SetInput(self.orientImage(newData, 'axial'))
    mapperAxial.SetZSlice(0)
    mapperAxial.SetColorWindow(self.ui.vsOriginalWindow.value())
    mapperAxial.SetColorLevel(self.ui.vsOriginalLevel.value())   
    self.axOriginalMapper = mapperAxial 
    
    actorAxial = vtk.vtkActor2D()
    actorAxial.SetMapper(mapperAxial)     
    actorAxial.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())         
    actorAxial.SetLayerNumber(0)
    
    self.originalAxBrainRenderer.RemoveAllViewProps()
    self.axOriginalActor = actorAxial    
    self.originalAxBrainRenderer.AddActor(actorAxial)        
    self.originalAxBrainRenderer.Render()
    
    #Set the coronal original view
    self.ui.vsHorCorOriginal.setMinimum(0 - newData.GetDimensions()[0] / 2)
    self.ui.vsHorCorOriginal.setMaximum(newData.GetDimensions()[0] / 2)
    self.ui.vsVerCorOriginal.setMinimum(0 - newData.GetDimensions()[2] / 2)
    self.ui.vsVerCorOriginal.setMaximum(newData.GetDimensions()[2] / 2)
    self.ui.vsZCorOriginal.setMinimum(0)
    self.ui.vsZCorOriginal.setMaximum(newData.GetDimensions()[1] - 1)            
    
    mapperCoronal = vtk.vtkImageMapper()
    mapperCoronal.SetInput(self.orientImage(newData, 'coronal'))
    mapperCoronal.SetZSlice(0)
    mapperCoronal.SetColorWindow(self.ui.vsOriginalWindow.value())
    mapperCoronal.SetColorLevel(self.ui.vsOriginalLevel.value())   
    self.corOriginalMapper = mapperCoronal
    
    actorCoronal = vtk.vtkActor2D()
    actorCoronal.SetMapper(mapperCoronal)     
    actorCoronal.SetPosition(self.ui.vsHorCorOriginal.value() - 100, self.ui.vsVerCorOriginal.value() + 150)         
    
    self.originalCorBrainRenderer.RemoveAllViewProps()
    self.corOriginalActor = actorCoronal    
    self.originalCorBrainRenderer.AddActor(actorCoronal)        
    self.originalCorBrainRenderer.Render()
    
    #Set the sagittal original view
    self.ui.vsHorSagOriginal.setMinimum(0 - newData.GetDimensions()[1] / 2)
    self.ui.vsHorSagOriginal.setMaximum(newData.GetDimensions()[1] / 2)
    self.ui.vsVerSagOriginal.setMinimum(0 - newData.GetDimensions()[2] / 2)
    self.ui.vsVerSagOriginal.setMaximum(newData.GetDimensions()[2] / 2)
    self.ui.vsZSagOriginal.setMinimum(0)
    self.ui.vsZSagOriginal.setMaximum(newData.GetDimensions()[0] - 1)            
    
    mapperSagittal = vtk.vtkImageMapper()
    mapperSagittal.SetInput(self.orientImage(newData, 'sagittal'))
    mapperSagittal.SetZSlice(0)
    mapperSagittal.SetColorWindow(self.ui.vsOriginalWindow.value())
    mapperSagittal.SetColorLevel(self.ui.vsOriginalLevel.value())   
    self.sagOriginalMapper = mapperSagittal
    
    actorSagittal = vtk.vtkActor2D()
    actorSagittal.SetMapper(mapperSagittal)     
    actorSagittal.SetPosition(self.ui.vsHorSagOriginal.value() - 100, self.ui.vsVerSagOriginal.value() + 150)         
    
    self.originalSagBrainRenderer.RemoveAllViewProps()
    self.sagOriginalActor = actorSagittal    
    self.originalSagBrainRenderer.AddActor(actorSagittal)        
    self.originalSagBrainRenderer.Render()
    
  def moveHorAxOriginal (self):
    if hasattr(self, 'axOriginalActor'):
      self.axOriginalActor.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())          
    if hasattr(self, 'axOriginalGoldActor'):
      self.axOriginalGoldActor.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())    
    if hasattr(self, 'axOriginalSegmActor'):
      self.axOriginalSegmActor.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())
    self.originalAxBrainWidgetWindowInteractor.Render()    
    
  def moveVerAxOriginal (self):
    if hasattr(self, 'axOriginalActor'):
       self.axOriginalActor.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())
    if hasattr(self, 'axOriginalGoldActor'):
      self.axOriginalGoldActor.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())
    if hasattr(self, 'axOriginalSegmActor'):
      self.axOriginalSegmActor.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())      
    self.originalAxBrainWidgetWindowInteractor.Render()   
    
  def moveZAxOriginal (self):
    if hasattr(self, 'axOriginalMapper'):
      self.axOriginalMapper.SetZSlice(self.ui.vsZAxOriginal.value())
    if hasattr(self, 'axOriginalGoldMapper'):
      self.axOriginalGoldMapper.SetZSlice(self.ui.vsZAxOriginal.value())
    if hasattr(self, 'axOriginalSegmMapper'):
      self.axOriginalSegmMapper.SetZSlice(self.ui.vsZAxOriginal.value())     
    if (self.ui.chSyncDisp.isChecked()):
      self.ui.vsZAxEnhanced.setValue(self.ui.vsZAxOriginal.value())              
    self.originalAxBrainWidgetWindowInteractor.Render()
    
  def moveHorCorOriginal (self):
    if hasattr(self, 'corOriginalActor'):
      self.corOriginalActor.SetPosition(self.ui.vsHorCorOriginal.value() - 100, self.ui.vsVerCorOriginal.value() + 150)
    if hasattr(self, 'corOriginalGoldActor'):
      self.corOriginalGoldActor.SetPosition(self.ui.vsHorCorOriginal.value() - 100, self.ui.vsVerCorOriginal.value() + 150)
    if hasattr(self, 'corOriginalSegmActor'):
      self.corOriginalSegmActor.SetPosition(self.ui.vsHorCorOriginal.value() - 100, self.ui.vsVerCorOriginal.value() + 150)      
    self.originalCorBrainWidgetWindowInteractor.Render()    
    
  def moveVerCorOriginal (self):
    if hasattr(self, 'corOriginalActor'):
      self.corOriginalActor.SetPosition(self.ui.vsHorCorOriginal.value() - 100, self.ui.vsVerCorOriginal.value() + 150)
    if hasattr(self, 'corOriginalGoldActor'):
      self.corOriginalGoldActor.SetPosition(self.ui.vsHorCorOriginal.value() - 100, self.ui.vsVerCorOriginal.value() + 150)
    if hasattr(self, 'corOriginalSegmActor'):
      self.corOriginalSegmActor.SetPosition(self.ui.vsHorCorOriginal.value() - 100, self.ui.vsVerCorOriginal.value() + 150)        
    self.originalCorBrainWidgetWindowInteractor.Render()   
    
  def moveZCorOriginal (self):
    if hasattr(self, 'corOriginalActor'):
      self.corOriginalMapper.SetZSlice(self.ui.vsZCorOriginal.value())
    if hasattr(self, 'corOriginalGoldMapper'):
      self.corOriginalGoldMapper.SetZSlice(self.ui.vsZCorOriginal.value())
    if hasattr(self, 'corOriginalSegmMapper'):
      self.corOriginalSegmMapper.SetZSlice(self.ui.vsZCorOriginal.value())      
    if (self.ui.chSyncDisp.isChecked()):
      self.ui.vsZCorEnhanced.setValue(self.ui.vsZCorOriginal.value())                    
    self.originalCorBrainWidgetWindowInteractor.Render() 
    
  def moveHorSagOriginal (self):
    if hasattr(self, 'sagOriginalActor'):
      self.sagOriginalActor.SetPosition(self.ui.vsHorSagOriginal.value() - 100, self.ui.vsVerSagOriginal.value() + 150)
    if hasattr(self, 'sagOriginalGoldActor'):
      self.sagOriginalGoldActor.SetPosition(self.ui.vsHorSagOriginal.value() - 100, self.ui.vsVerSagOriginal.value() + 150)    
    if hasattr(self, 'sagOriginalSegmActor'):
      self.sagOriginalSegmActor.SetPosition(self.ui.vsHorSagOriginal.value() - 100, self.ui.vsVerSagOriginal.value() + 150)          
    self.originalSagBrainWidgetWindowInteractor.Render()    
    
  def moveVerSagOriginal (self):
    if hasattr(self, 'sagOriginalActor'):
      self.sagOriginalActor.SetPosition(self.ui.vsHorSagOriginal.value() - 100, self.ui.vsVerSagOriginal.value() + 150)
    if hasattr(self, 'sagOriginalGoldActor'):
      self.sagOriginalGoldActor.SetPosition(self.ui.vsHorSagOriginal.value() - 100, self.ui.vsVerSagOriginal.value() + 150)     
    if hasattr(self, 'sagOriginalSegmActor'):
      self.sagOriginalSegmActor.SetPosition(self.ui.vsHorSagOriginal.value() - 100, self.ui.vsVerSagOriginal.value() + 150)      
    self.originalSagBrainWidgetWindowInteractor.Render()   
    
  def moveZSagOriginal (self):
    if hasattr(self, 'sagOriginalMapper'):
      self.sagOriginalMapper.SetZSlice(self.ui.vsZSagOriginal.value())
    if hasattr(self, 'sagOriginalGoldMapper'):
      self.sagOriginalGoldMapper.SetZSlice(self.ui.vsZSagOriginal.value())  
    if hasattr(self, 'sagOriginalSegmMapper'):
      self.sagOriginalSegmMapper.SetZSlice(self.ui.vsZSagOriginal.value())      
    if (self.ui.chSyncDisp.isChecked()):
      self.ui.vsZSagEnhanced.setValue(self.ui.vsZSagOriginal.value())                    
    self.originalSagBrainWidgetWindowInteractor.Render()     
    
  def openGoldSegmFile (self):
    fileName = QtGui.QFileDialog.getOpenFileName(self,'Open file','/home/rphellan/UofC/Datasets/VesselGroundTruthMasks')          
    segmGoldData = self.openNiftiiImage(fileName)
        
    self.segmGoldData = segmGoldData    
        
    lookupTableGoldSegOrig = vtk.vtkLookupTable()    
    self.lookupTableGoldSegOrig = lookupTableGoldSegOrig
    lookupTableGoldSegOrig.SetNumberOfTableValues(2)
    lookupTableGoldSegOrig.SetRange(0.0,1.0)
    lookupTableGoldSegOrig.SetTableValue( 0, 1.0, 0.0, 0.0, 0.0 ) #label 0 is transparent
    lookupTableGoldSegOrig.SetTableValue( 1, 0.0, 1.0, 0.0, self.ui.vsGoldTransparency.value() * 1.0 / 100 )  #label 1 is opaque and green
    lookupTableGoldSegOrig.Build()
    
    lookupTableGoldSegEnc = vtk.vtkLookupTable()    
    self.lookupTableGoldSegEnc = lookupTableGoldSegEnc
    lookupTableGoldSegEnc.SetNumberOfTableValues(2)
    lookupTableGoldSegEnc.SetRange(0.0,1.0)
    lookupTableGoldSegEnc.SetTableValue( 0, 1.0, 0.0, 0.0, 0.0 ) #label 0 is transparent
    lookupTableGoldSegEnc.SetTableValue( 1, 0.0, 1.0, 0.0, self.ui.vsGoldTransparencyEnc.value() * 1.0 / 100 )  #label 1 is opaque and green
    lookupTableGoldSegEnc.Build()
    
    # Overlay axial gold segmentation over original image
    mapAxialTransparency = vtk.vtkImageMapToColors()    
    mapAxialTransparency.SetLookupTable(lookupTableGoldSegOrig)
    mapAxialTransparency.PassAlphaToOutputOn()
    mapAxialTransparency.SetInput(self.orientImage(segmGoldData, 'axial'))    

    mapperAxialOriginalGold = vtk.vtkImageMapper()
    mapperAxialOriginalGold.SetInputConnection(mapAxialTransparency.GetOutputPort())    
    mapperAxialOriginalGold.SetZSlice(self.ui.vsZAxOriginal.value())
    mapperAxialOriginalGold.SetColorWindow(300)
    mapperAxialOriginalGold.SetColorLevel(140)   
    self.axOriginalGoldMapper = mapperAxialOriginalGold

    actorAxialOriginalGold = vtk.vtkActor2D()
    actorAxialOriginalGold.SetMapper(mapperAxialOriginalGold)
    actorAxialOriginalGold.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())   
    if hasattr(self, 'axOriginalGoldActor'):
      self.originalAxBrainRenderer.RemoveActor(self.axOriginalGoldActor)
    self.axOriginalGoldActor = actorAxialOriginalGold
    
    self.originalAxBrainRenderer.AddActor(actorAxialOriginalGold)
    self.originalAxBrainWidgetWindowInteractor.Render()           
    
    # Overlay axial gold segmentation over enhanced image    
    mapAxialTransparencyEnc = vtk.vtkImageMapToColors()    
    mapAxialTransparencyEnc.SetLookupTable(lookupTableGoldSegEnc)
    mapAxialTransparencyEnc.PassAlphaToOutputOn()
    mapAxialTransparencyEnc.SetInput(self.orientImage(segmGoldData, 'axial'))        
    
    mapperAxialEnhancedGold = vtk.vtkImageMapper()
    mapperAxialEnhancedGold.SetInputConnection(mapAxialTransparencyEnc.GetOutputPort())    
    mapperAxialEnhancedGold.SetZSlice(self.ui.vsZAxEnhanced.value())
    mapperAxialEnhancedGold.SetColorWindow(300)
    mapperAxialEnhancedGold.SetColorLevel(140)   
    self.axEnhancedGoldMapper = mapperAxialEnhancedGold

    actorAxialEnhancedGold = vtk.vtkActor2D()
    actorAxialEnhancedGold.SetMapper(mapperAxialEnhancedGold)
    actorAxialEnhancedGold.SetPosition(self.ui.vsHorAxEnhanced.value() - 100, self.ui.vsVerAxEnhanced.value())   
    if hasattr(self, 'axEnhancedGoldActor'):
      self.enhancedAxBrainRenderer.RemoveActor(self.axEnhancedGoldActor)
    self.axEnhancedGoldActor = actorAxialEnhancedGold
    
    self.enhancedAxBrainRenderer.AddActor(actorAxialEnhancedGold)
    self.enhancedAxBrainWidgetWindowInteractor.Render()      
    
    # Overlay coronal gold segmentation over original image
    mapCoronalTransparency = vtk.vtkImageMapToColors()    
    mapCoronalTransparency.SetLookupTable(lookupTableGoldSegOrig)
    mapCoronalTransparency.PassAlphaToOutputOn()
    mapCoronalTransparency.SetInput(self.orientImage(segmGoldData, 'coronal'))    

    mapperCoronalOriginalGold = vtk.vtkImageMapper()
    mapperCoronalOriginalGold.SetInputConnection(mapCoronalTransparency.GetOutputPort())    
    mapperCoronalOriginalGold.SetZSlice(self.ui.vsZCorOriginal.value())
    mapperCoronalOriginalGold.SetColorWindow(300)
    mapperCoronalOriginalGold.SetColorLevel(140)   
    self.corOriginalGoldMapper = mapperCoronalOriginalGold

    actorCoronalOriginalGold = vtk.vtkActor2D()
    actorCoronalOriginalGold.SetMapper(mapperCoronalOriginalGold)
    actorCoronalOriginalGold.SetPosition(self.ui.vsHorCorOriginal.value() - 100, self.ui.vsVerCorOriginal.value() + 150)   
    if hasattr(self, 'corOriginalGoldActor'):
      self.originalCorBrainRenderer.RemoveActor(self.corOriginalGoldActor)
    self.corOriginalGoldActor = actorCoronalOriginalGold
    
    self.originalCorBrainRenderer.AddActor(actorCoronalOriginalGold)
    self.originalCorBrainWidgetWindowInteractor.Render()
    
    # Overlay coronal gold segmentation over enhanced image    
    mapCoronalTransparencyEnc = vtk.vtkImageMapToColors()    
    mapCoronalTransparencyEnc.SetLookupTable(lookupTableGoldSegEnc)
    mapCoronalTransparencyEnc.PassAlphaToOutputOn()
    mapCoronalTransparencyEnc.SetInput(self.orientImage(segmGoldData, 'coronal'))    
    
    mapperCoronalEnhancedGold = vtk.vtkImageMapper()
    mapperCoronalEnhancedGold.SetInputConnection(mapCoronalTransparencyEnc.GetOutputPort())    
    mapperCoronalEnhancedGold.SetZSlice(self.ui.vsZCorEnhanced.value())
    mapperCoronalEnhancedGold.SetColorWindow(self.ui.vsOriginalWindow.value())
    mapperCoronalEnhancedGold.SetColorLevel(self.ui.vsOriginalLevel.value())   
    self.corEnhancedGoldMapper = mapperCoronalEnhancedGold

    actorCoronalEnhancedGold = vtk.vtkActor2D()
    actorCoronalEnhancedGold.SetMapper(mapperCoronalEnhancedGold)
    actorCoronalEnhancedGold.SetPosition(self.ui.vsHorCorEnhanced.value() - 100, self.ui.vsVerCorEnhanced.value() + 150)   
    if hasattr(self, 'corEnhancedGoldActor'):
      self.enhancedCorBrainRenderer.RemoveActor(self.corEnhancedGoldActor)
    self.corEnhancedGoldActor = actorCoronalEnhancedGold
    
    self.enhancedCorBrainRenderer.AddActor(actorCoronalEnhancedGold)
    self.enhancedCorBrainWidgetWindowInteractor.Render()  
    
    # Overlay sagittal gold segmentation over original image
    mapSagittalTransparency = vtk.vtkImageMapToColors()    
    mapSagittalTransparency.SetLookupTable(lookupTableGoldSegOrig)
    mapSagittalTransparency.PassAlphaToOutputOn()
    mapSagittalTransparency.SetInput(self.orientImage(segmGoldData, 'sagittal'))    

    mapperSagittalOriginalGold = vtk.vtkImageMapper()
    mapperSagittalOriginalGold.SetInputConnection(mapSagittalTransparency.GetOutputPort())    
    mapperSagittalOriginalGold.SetZSlice(self.ui.vsZSagOriginal.value())
    mapperSagittalOriginalGold.SetColorWindow(300)
    mapperSagittalOriginalGold.SetColorLevel(140)   
    self.sagOriginalGoldMapper = mapperSagittalOriginalGold

    actorSagittalOriginalGold = vtk.vtkActor2D()
    actorSagittalOriginalGold.SetMapper(mapperSagittalOriginalGold)
    actorSagittalOriginalGold.SetPosition(self.ui.vsHorSagOriginal.value() - 100, self.ui.vsVerSagOriginal.value() + 150)   
    if hasattr(self, 'sagOriginalGoldActor'):
      self.originalSagBrainRenderer.RemoveActor(self.sagOriginalGoldActor)
    self.sagOriginalGoldActor = actorSagittalOriginalGold
    
    self.originalSagBrainRenderer.AddActor(actorSagittalOriginalGold)
    self.originalSagBrainWidgetWindowInteractor.Render()    
  
    # Overlay sagittal gold segmentation over enhanced image
    mapSagittalTransparencyEnc = vtk.vtkImageMapToColors()    
    mapSagittalTransparencyEnc.SetLookupTable(lookupTableGoldSegEnc)
    mapSagittalTransparencyEnc.PassAlphaToOutputOn()
    mapSagittalTransparencyEnc.SetInput(self.orientImage(segmGoldData, 'sagittal'))  
    
    mapperSagittalEnhancedGold = vtk.vtkImageMapper()
    mapperSagittalEnhancedGold.SetInputConnection(mapSagittalTransparencyEnc.GetOutputPort())    
    mapperSagittalEnhancedGold.SetZSlice(self.ui.vsZSagEnhanced.value())
    mapperSagittalEnhancedGold.SetColorWindow(300)
    mapperSagittalEnhancedGold.SetColorLevel(140)   
    self.sagEnhancedGoldMapper = mapperSagittalEnhancedGold

    actorSagittalEnhancedGold = vtk.vtkActor2D()
    actorSagittalEnhancedGold.SetMapper(mapperSagittalEnhancedGold)
    actorSagittalEnhancedGold.SetPosition(self.ui.vsHorSagEnhanced.value() - 100, self.ui.vsVerSagEnhanced.value() + 150)   
    if hasattr(self, 'sagEnhancedGoldActor'):
      self.enhancedSagBrainRenderer.RemoveActor(self.sagEnhancedGoldActor)
    self.sagEnhancedGoldActor = actorSagittalEnhancedGold
    
    self.enhancedSagBrainRenderer.AddActor(actorSagittalEnhancedGold)
    self.enhancedSagBrainWidgetWindowInteractor.Render()
  
    self.ui.chOriginalGold.setChecked(True)
    self.ui.chEnhancedGold.setChecked(True)    
    
  def toggleOriginalGold (self):
    if hasattr(self, 'axOriginalGoldActor'):
      if self.ui.chOriginalGold.isChecked():
        self.axOriginalGoldActor.SetVisibility(True)        
        self.originalAxBrainWidgetWindowInteractor.Render()
        
        self.corOriginalGoldActor.SetVisibility(True)
        self.originalCorBrainWidgetWindowInteractor.Render()
        
        self.sagOriginalGoldActor.SetVisibility(True)
        self.originalSagBrainWidgetWindowInteractor.Render()
        
      else:
        self.axOriginalGoldActor.SetVisibility(False)
        self.originalAxBrainWidgetWindowInteractor.Render()
        
        self.corOriginalGoldActor.SetVisibility(False)
        self.originalCorBrainWidgetWindowInteractor.Render()
        
        self.sagOriginalGoldActor.SetVisibility(False)
        self.originalSagBrainWidgetWindowInteractor.Render()   
        
  def toggleEnhancedGold (self):
    if hasattr(self, 'axEnhancedGoldActor'):
      if self.ui.chEnhancedGold.isChecked():
        self.axEnhancedGoldActor.SetVisibility(True)        
        self.enhancedAxBrainWidgetWindowInteractor.Render()
        
        self.corEnhancedGoldActor.SetVisibility(True)
        self.enhancedCorBrainWidgetWindowInteractor.Render()
        
        self.sagEnhancedGoldActor.SetVisibility(True)
        self.enhancedSagBrainWidgetWindowInteractor.Render()
        
      else:
        self.axEnhancedGoldActor.SetVisibility(False)
        self.enhancedAxBrainWidgetWindowInteractor.Render()
        
        self.corEnhancedGoldActor.SetVisibility(False)
        self.enhancedCorBrainWidgetWindowInteractor.Render()
        
        self.sagEnhancedGoldActor.SetVisibility(False)
        self.enhancedSagBrainWidgetWindowInteractor.Render()         
        
  def show3dGold (self):
    
    ren = vtk.vtkRenderer()
    
        #Show 3d view of the gold segmentation
    if self.ui.chOriginalGold.isChecked():
      voiGoldOrig = vtk.vtkExtractVOI()
      voiGoldOrig.SetInput(self.segmGoldData)
      voiGoldOrig.SetVOI(self.segmGoldData.GetExtent())    
      voiGoldOrig.Update()
      self.voiGoldOrig = voiGoldOrig           
        
      isoGold = vtk.vtkMarchingCubes()
      isoGold.SetInput(voiGoldOrig.GetOutput())
      isoGold.SetValue(0, 1)
      isoGold.Update()
      self.isoGold = isoGold    
    
      decimatorGold = vtk.vtkDecimatePro()
      decimatorGold.SetInputConnection(isoGold.GetOutputPort())
      decimatorGold.SetTargetReduction(0.20)
      decimatorGold.Update()
        
      mapperGold = vtk.vtkPolyDataMapper()
      mapperGold.SetInputConnection(decimatorGold.GetOutputPort())      
      mapperGold.ScalarVisibilityOff()
      mapperGold.ImmediateModeRenderingOn()    

      actorGold = vtk.vtkActor()
      actorGold.SetMapper(mapperGold)  
      actorGold.GetProperty().SetColor([0.0, 1.0, 0.0])  
      
      ren.AddActor(actorGold)
    
        #Show 3d view of the segmentation
    if self.ui.chOriginalSegm.isChecked():
      
      voiSegOrig = vtk.vtkExtractVOI()
      voiSegOrig.SetInput(self.segmData)
      voiSegOrig.SetVOI(self.segmData.GetExtent())    
      voiSegOrig.Update()    
      self.voiSegOrig = voiSegOrig      
      
      isoSeg = vtk.vtkMarchingCubes()
      isoSeg.SetInput(voiSegOrig.GetOutput())
      isoSeg.SetValue(0, 1)
      isoSeg.Update()
    
      decimatorSeg = vtk.vtkDecimatePro()
      decimatorSeg.SetInputConnection(isoSeg.GetOutputPort())
      decimatorSeg.SetTargetReduction(0.20)
      decimatorSeg.Update()
        
      mapperSeg = vtk.vtkPolyDataMapper()
      mapperSeg.SetInputConnection(decimatorSeg.GetOutputPort())      
      mapperSeg.ScalarVisibilityOff()
      mapperSeg.ImmediateModeRenderingOn()    

      actorSeg = vtk.vtkActor()
      actorSeg.SetMapper(mapperSeg)  
      actorSeg.GetProperty().SetColor([1.0, 0.0, 0.0])    

      ren.AddActor(actorSeg)

    renWin = vtk.vtkRenderWindow()      
    
    renWin.AddRenderer(ren)
    
    renWin.SetSize(500, 500)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)    
    
    # Create a box widget
    
    #Extract selected region    
    
    if (self.ui.chOriginalGold.isChecked() or self.ui.chOriginalSegm.isChecked()):
      if self.ui.chOriginalGold.isChecked():
        voiOrig = self.segmGoldData
      if self.ui.chOriginalSegm.isChecked():
        voiOrig = self.segmData       
      boxWidget3d = vtk.vtkBoxWidget()
      boxWidget3d.SetInteractor(iren)
      boxWidget3d.SetPlaceFactor(1.0)
      boxWidget3d.SetInput(voiOrig)
      boxWidget3d.PlaceWidget()
      boxWidget3d.RotationEnabledOff()
      boxWidget3d.On()
      self.voiOrig = voiOrig
      
      def myCallback(widget, event_string):
        pd = vtk.vtkPolyData()
        boxWidget3d.GetPolyData(pd)
        pointBegin = [0.1, 0.1, 0.1]   
        pointEnd = [0.1, 0.1, 0.1]
        pd.GetPoint(0,pointBegin)   
        pd.GetPoint(6,pointEnd)           
        spac = self.segmData.GetSpacing()
        
        if self.ui.chOriginalGold.isChecked():  	  	  	  
          self.voiGoldOrig.SetVOI(int(pointBegin[0] / spac[0]), int(pointEnd[0] / spac[0]), int(pointBegin[1] / spac[1]), int(pointEnd[1] / spac[1]), int(pointBegin[2] / spac[2]), int(pointEnd[2]/ spac[2]))                        
        
        if self.ui.chOriginalSegm.isChecked():  	  	  	  
          self.voiSegOrig.SetVOI(int(pointBegin[0] / spac[0]), int(pointEnd[0] / spac[0]), int(pointBegin[1] / spac[1]), int(pointEnd[1] / spac[1]), int(pointBegin[2] / spac[2]), int(pointEnd[2]/ spac[2]))                        
          
        ren.Render()
        
      boxWidget3d.AddObserver("EndInteractionEvent", myCallback) 
    
    iren.Initialize()
    renWin.Render()
    iren.Start()

  def openSegmFile (self):
    fileName = QtGui.QFileDialog.getOpenFileName(self,'Open file','/home/rphellan/UofC/Datasets/VesselGroundTruthMasks')          
    segmData = self.openNiftiiImage(fileName)
    
    cast = vtk.vtkImageCast()
    cast.SetInput(segmData)
    cast.SetOutputScalarType(self.segmGoldData.GetScalarType())
    cast.Update()
        
    self.segmData = cast.GetOutput()    
        
    lookupTableSeg = vtk.vtkLookupTable()    
    self.lookupTableSeg = lookupTableSeg
    lookupTableSeg.SetNumberOfTableValues(2)
    lookupTableSeg.SetRange(0.0,1.0)
    lookupTableSeg.SetTableValue( 0, 1.0, 0.0, 0.0, 0.0 ) #label 0 is transparent
    lookupTableSeg.SetTableValue( 1, 1.0, 0.0, 0.0,  self.ui.vsSegTransparency.value() * 1.0 / 100  )  #label 1 is opaque and red
    lookupTableSeg.Build()
    
    lookupTableSegEnc = vtk.vtkLookupTable()    
    self.lookupTableSegEnc = lookupTableSegEnc
    lookupTableSegEnc.SetNumberOfTableValues(2)
    lookupTableSegEnc.SetRange(0.0,1.0)
    lookupTableSegEnc.SetTableValue( 0, 1.0, 0.0, 0.0, 0.0 ) #label 0 is transparent
    lookupTableSegEnc.SetTableValue( 1, 1.0, 0.0, 0.0,  self.ui.vsSegTransparencyEnc.value() * 1.0 / 100  )  #label 1 is opaque and red
    lookupTableSegEnc.Build()
    
    # Overlay axial segmentation over original image
    mapAxialTransparency = vtk.vtkImageMapToColors()    
    mapAxialTransparency.SetLookupTable(lookupTableSeg)
    mapAxialTransparency.PassAlphaToOutputOn()
    mapAxialTransparency.SetInput(self.orientImage(segmData, 'axial'))    

    mapperAxialOriginalSegm = vtk.vtkImageMapper()
    mapperAxialOriginalSegm.SetInputConnection(mapAxialTransparency.GetOutputPort())    
    mapperAxialOriginalSegm.SetZSlice(self.ui.vsZAxOriginal.value())
    mapperAxialOriginalSegm.SetColorWindow(300)
    mapperAxialOriginalSegm.SetColorLevel(140)   
    self.axOriginalSegmMapper = mapperAxialOriginalSegm

    actorAxialOriginalSegm = vtk.vtkActor2D()
    actorAxialOriginalSegm.SetMapper(mapperAxialOriginalSegm)
    actorAxialOriginalSegm.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())   
    if hasattr(self, 'axOriginalSegmActor'):
      self.originalAxBrainRenderer.RemoveActor(self.axOriginalSegmActor)
    self.axOriginalSegmActor = actorAxialOriginalSegm
    
    self.originalAxBrainRenderer.AddActor(actorAxialOriginalSegm)
    self.originalAxBrainWidgetWindowInteractor.Render()           
    
    # Overlay axial segmentation over enhanced image    
    mapAxialTransparencyEnc = vtk.vtkImageMapToColors()    
    mapAxialTransparencyEnc.SetLookupTable(lookupTableSegEnc)
    mapAxialTransparencyEnc.PassAlphaToOutputOn()
    mapAxialTransparencyEnc.SetInput(self.orientImage(segmData, 'axial'))        
    
    mapperAxialEnhancedSegm = vtk.vtkImageMapper()
    mapperAxialEnhancedSegm.SetInputConnection(mapAxialTransparencyEnc.GetOutputPort())    
    mapperAxialEnhancedSegm.SetZSlice(self.ui.vsZAxEnhanced.value())
    mapperAxialEnhancedSegm.SetColorWindow(300)
    mapperAxialEnhancedSegm.SetColorLevel(140)   
    self.axEnhancedSegmMapper = mapperAxialEnhancedSegm

    actorAxialEnhancedSegm = vtk.vtkActor2D()
    actorAxialEnhancedSegm.SetMapper(mapperAxialEnhancedSegm)
    actorAxialEnhancedSegm.SetPosition(self.ui.vsHorAxEnhanced.value() - 100, self.ui.vsVerAxEnhanced.value())   
    if hasattr(self, 'axEnhancedSegmActor'):
      self.enhancedAxBrainRenderer.RemoveActor(self.axEnhancedSegmActor)
    self.axEnhancedSegmActor = actorAxialEnhancedSegm
    
    self.enhancedAxBrainRenderer.AddActor(actorAxialEnhancedSegm)
    self.enhancedAxBrainWidgetWindowInteractor.Render()  
    
    # Overlay coronal segmentation over original image
    mapCoronalTransparency = vtk.vtkImageMapToColors()    
    mapCoronalTransparency.SetLookupTable(lookupTableSeg)
    mapCoronalTransparency.PassAlphaToOutputOn()
    mapCoronalTransparency.SetInput(self.orientImage(segmData, 'coronal'))    

    mapperCoronalOriginalSegm = vtk.vtkImageMapper()
    mapperCoronalOriginalSegm.SetInputConnection(mapCoronalTransparency.GetOutputPort())    
    mapperCoronalOriginalSegm.SetZSlice(self.ui.vsZCorOriginal.value())
    mapperCoronalOriginalSegm.SetColorWindow(300)
    mapperCoronalOriginalSegm.SetColorLevel(140)   
    self.corOriginalSegmMapper = mapperCoronalOriginalSegm

    actorCoronalOriginalSegm = vtk.vtkActor2D()
    actorCoronalOriginalSegm.SetMapper(mapperCoronalOriginalSegm)
    actorCoronalOriginalSegm.SetPosition(self.ui.vsHorCorOriginal.value() - 100, self.ui.vsVerCorOriginal.value() + 150)   
    if hasattr(self, 'corOriginalSegmActor'):
      self.originalCorBrainRenderer.RemoveActor(self.corOriginalSegmActor)
    self.corOriginalSegmActor = actorCoronalOriginalSegm
    
    self.originalCorBrainRenderer.AddActor(actorCoronalOriginalSegm)
    self.originalCorBrainWidgetWindowInteractor.Render()

    # Overlay coronal segmentation over enhanced image   
    mapCoronalTransparencyEnc = vtk.vtkImageMapToColors()    
    mapCoronalTransparencyEnc.SetLookupTable(lookupTableSegEnc)
    mapCoronalTransparencyEnc.PassAlphaToOutputOn()
    mapCoronalTransparencyEnc.SetInput(self.orientImage(segmData, 'coronal'))   
    
    mapperCoronalEnhancedSegm = vtk.vtkImageMapper()
    mapperCoronalEnhancedSegm.SetInputConnection(mapCoronalTransparencyEnc.GetOutputPort())    
    mapperCoronalEnhancedSegm.SetZSlice(self.ui.vsZCorEnhanced.value())
    mapperCoronalEnhancedSegm.SetColorWindow(300)
    mapperCoronalEnhancedSegm.SetColorLevel(140)   
    self.corEnhancedSegmMapper = mapperCoronalEnhancedSegm

    actorCoronalEnhancedSegm = vtk.vtkActor2D()
    actorCoronalEnhancedSegm.SetMapper(mapperCoronalEnhancedSegm)
    actorCoronalEnhancedSegm.SetPosition(self.ui.vsHorCorEnhanced.value() - 100, self.ui.vsVerCorEnhanced.value() + 150)   
    if hasattr(self, 'corEnhancedSegmActor'):
      self.enhancedCorBrainRenderer.RemoveActor(self.corEnhancedSegmActor)
    self.corEnhancedSegmActor = actorCoronalEnhancedSegm
    
    self.enhancedCorBrainRenderer.AddActor(actorCoronalEnhancedSegm)
    self.enhancedCorBrainWidgetWindowInteractor.Render()  
    
    # Overlay sagittal segmentation over original image
    mapSagittalTransparency = vtk.vtkImageMapToColors()    
    mapSagittalTransparency.SetLookupTable(lookupTableSeg)
    mapSagittalTransparency.PassAlphaToOutputOn()
    mapSagittalTransparency.SetInput(self.orientImage(segmData, 'sagittal'))    

    mapperSagittalOriginalSegm = vtk.vtkImageMapper()
    mapperSagittalOriginalSegm.SetInputConnection(mapSagittalTransparency.GetOutputPort())    
    mapperSagittalOriginalSegm.SetZSlice(self.ui.vsZSagOriginal.value())
    mapperSagittalOriginalSegm.SetColorWindow(300)
    mapperSagittalOriginalSegm.SetColorLevel(140)   
    self.sagOriginalSegmMapper = mapperSagittalOriginalSegm

    actorSagittalOriginalSegm = vtk.vtkActor2D()
    actorSagittalOriginalSegm.SetMapper(mapperSagittalOriginalSegm)
    actorSagittalOriginalSegm.SetPosition(self.ui.vsHorSagOriginal.value() - 100, self.ui.vsVerSagOriginal.value() + 150)   
    if hasattr(self, 'sagOriginalSegmActor'):
      self.originalSagBrainRenderer.RemoveActor(self.sagOriginalSegmActor)
    self.sagOriginalSegmActor = actorSagittalOriginalSegm
    
    self.originalSagBrainRenderer.AddActor(actorSagittalOriginalSegm)
    self.originalSagBrainWidgetWindowInteractor.Render()   
    
    # Overlay sagittal segmentation over enhanced image    
    mapSagittalTransparencyEnc = vtk.vtkImageMapToColors()    
    mapSagittalTransparencyEnc.SetLookupTable(lookupTableSegEnc)
    mapSagittalTransparencyEnc.PassAlphaToOutputOn()
    mapSagittalTransparencyEnc.SetInput(self.orientImage(segmData, 'sagittal'))   
    
    mapperSagittalEnhancedSegm = vtk.vtkImageMapper()
    mapperSagittalEnhancedSegm.SetInputConnection(mapSagittalTransparencyEnc.GetOutputPort())    
    mapperSagittalEnhancedSegm.SetZSlice(self.ui.vsZSagEnhanced.value())
    mapperSagittalEnhancedSegm.SetColorWindow(300)
    mapperSagittalEnhancedSegm.SetColorLevel(140)   
    self.sagEnhancedSegmMapper = mapperSagittalEnhancedSegm

    actorSagittalEnhancedSegm = vtk.vtkActor2D()
    actorSagittalEnhancedSegm.SetMapper(mapperSagittalEnhancedSegm)
    actorSagittalEnhancedSegm.SetPosition(self.ui.vsHorSagEnhanced.value() - 100, self.ui.vsVerSagEnhanced.value() + 150)   
    if hasattr(self, 'sagEnhancedSegmActor'):
      self.enhancedSagBrainRenderer.RemoveActor(self.sagEnhancedSegmActor)
    self.sagEnhancedSegmActor = actorSagittalEnhancedSegm
    
    self.enhancedSagBrainRenderer.AddActor(actorSagittalEnhancedSegm)
    self.enhancedSagBrainWidgetWindowInteractor.Render()
  
    self.ui.chOriginalSegm.setChecked(True)
    self.ui.chEnhancedSegm.setChecked(True)
    
  def toggleOriginalSegm (self):
    if hasattr(self, 'axOriginalSegmActor'):
      if self.ui.chOriginalSegm.isChecked():
        self.axOriginalSegmActor.SetVisibility(True)        
        self.originalAxBrainWidgetWindowInteractor.Render()
        
        self.corOriginalSegmActor.SetVisibility(True)
        self.originalCorBrainWidgetWindowInteractor.Render()
        
        self.sagOriginalSegmActor.SetVisibility(True)
        self.originalSagBrainWidgetWindowInteractor.Render()
        
      else:
        self.axOriginalSegmActor.SetVisibility(False)
        self.originalAxBrainWidgetWindowInteractor.Render()
        
        self.corOriginalSegmActor.SetVisibility(False)
        self.originalCorBrainWidgetWindowInteractor.Render()
        
        self.sagOriginalSegmActor.SetVisibility(False)
        self.originalSagBrainWidgetWindowInteractor.Render()        
        
  def toggleEnhancedSegm (self):
    if hasattr(self, 'axEnhancedSegmActor'):
      if self.ui.chEnhancedSegm.isChecked():
        self.axEnhancedSegmActor.SetVisibility(True)        
        self.enhancedAxBrainWidgetWindowInteractor.Render()
        
        self.corEnhancedSegmActor.SetVisibility(True)
        self.enhancedCorBrainWidgetWindowInteractor.Render()
        
        self.sagEnhancedSegmActor.SetVisibility(True)
        self.enhancedSagBrainWidgetWindowInteractor.Render()
        
      else:
        self.axEnhancedSegmActor.SetVisibility(False)
        self.enhancedAxBrainWidgetWindowInteractor.Render()
        
        self.corEnhancedSegmActor.SetVisibility(False)
        self.enhancedCorBrainWidgetWindowInteractor.Render()
        
        self.sagEnhancedSegmActor.SetVisibility(False)
        self.enhancedSagBrainWidgetWindowInteractor.Render()                 
        
  def openEnhancedBrainFile (self):
    fileName = QtGui.QFileDialog.getOpenFileName(self,'Open file','/home/rphellan/UofC/Datasets/OriginalBrainsAndGT')          
    newData = self.openNiftiiImage(fileName)
    
        #Set window and level max and min
    self.ui.vsEnhancedWindow.setMinimum(0)
    self.ui.vsEnhancedWindow.setMaximum(newData.GetScalarRange()[1])
    
    self.ui.vsEnhancedLevel.setMinimum(0)
    self.ui.vsEnhancedLevel.setMaximum(newData.GetScalarRange()[1])    
    
    #Set the axial enhanced view
    self.ui.vsHorAxEnhanced.setMinimum(0 - newData.GetDimensions()[0] / 2)
    self.ui.vsHorAxEnhanced.setMaximum(newData.GetDimensions()[0] / 2)
    self.ui.vsVerAxEnhanced.setMinimum(0 - newData.GetDimensions()[1] / 2)
    self.ui.vsVerAxEnhanced.setMaximum(newData.GetDimensions()[1] / 2)
    self.ui.vsZAxEnhanced.setMinimum(0)
    self.ui.vsZAxEnhanced.setMaximum(newData.GetDimensions()[2] - 1)    
  
    mapperAxial = vtk.vtkImageMapper()
    mapperAxial.SetInput(self.orientImage(newData, 'axial'))
    mapperAxial.SetZSlice(0)
    mapperAxial.SetColorWindow(self.ui.vsEnhancedWindow.value())
    mapperAxial.SetColorLevel(self.ui.vsEnhancedLevel.value())   
    self.axEnhancedMapper = mapperAxial
    
    actorAxial = vtk.vtkActor2D()
    actorAxial.SetMapper(mapperAxial)     
    actorAxial.SetPosition(self.ui.vsHorAxOriginal.value() - 100, self.ui.vsVerAxOriginal.value())         
    actorAxial.SetLayerNumber(0)
    
    self.enhancedAxBrainRenderer.RemoveAllViewProps()
    self.axEnhancedActor = actorAxial    
    self.enhancedAxBrainRenderer.AddActor(actorAxial)        
    self.enhancedAxBrainRenderer.Render()
    
    #Set the coronal enhanced view
    self.ui.vsHorCorEnhanced.setMinimum(0 - newData.GetDimensions()[0] / 2)
    self.ui.vsHorCorEnhanced.setMaximum(newData.GetDimensions()[0] / 2)
    self.ui.vsVerCorEnhanced.setMinimum(0 - newData.GetDimensions()[2] / 2)
    self.ui.vsVerCorEnhanced.setMaximum(newData.GetDimensions()[2] / 2)
    self.ui.vsZCorEnhanced.setMinimum(0)
    self.ui.vsZCorEnhanced.setMaximum(newData.GetDimensions()[1] - 1)            
    
    mapperCoronal = vtk.vtkImageMapper()
    mapperCoronal.SetInput(self.orientImage(newData, 'coronal'))
    mapperCoronal.SetZSlice(0)
    mapperCoronal.SetColorWindow(self.ui.vsEnhancedWindow.value())
    mapperCoronal.SetColorLevel(self.ui.vsEnhancedLevel.value())   
    self.corEnhancedMapper = mapperCoronal
    
    actorCoronal = vtk.vtkActor2D()
    actorCoronal.SetMapper(mapperCoronal)     
    actorCoronal.SetPosition(self.ui.vsHorCorEnhanced.value() - 100, self.ui.vsVerCorEnhanced.value() + 150)         
    
    self.enhancedCorBrainRenderer.RemoveAllViewProps()
    self.corEnhancedActor = actorCoronal    
    self.enhancedCorBrainRenderer.AddActor(actorCoronal)        
    self.enhancedCorBrainRenderer.Render()
    
    #Set the sagittal enhanced view
    self.ui.vsHorSagEnhanced.setMinimum(0 - newData.GetDimensions()[1] / 2)
    self.ui.vsHorSagEnhanced.setMaximum(newData.GetDimensions()[1] / 2)
    self.ui.vsVerSagEnhanced.setMinimum(0 - newData.GetDimensions()[2] / 2)
    self.ui.vsVerSagEnhanced.setMaximum(newData.GetDimensions()[2] / 2)
    self.ui.vsZSagEnhanced.setMinimum(0)
    self.ui.vsZSagEnhanced.setMaximum(newData.GetDimensions()[0] - 1)            
    
    mapperSagittal = vtk.vtkImageMapper()
    mapperSagittal.SetInput(self.orientImage(newData, 'sagittal'))
    mapperSagittal.SetZSlice(0)
    mapperSagittal.SetColorWindow(self.ui.vsEnhancedWindow.value())
    mapperSagittal.SetColorLevel(self.ui.vsEnhancedLevel.value())   
    self.sagEnhancedMapper = mapperSagittal
    
    actorSagittal = vtk.vtkActor2D()
    actorSagittal.SetMapper(mapperSagittal)     
    actorSagittal.SetPosition(self.ui.vsHorSagEnhanced.value() - 100, self.ui.vsVerSagEnhanced.value() + 150)         
    
    self.enhancedSagBrainRenderer.RemoveAllViewProps()
    self.sagEnhancedActor = actorSagittal    
    self.enhancedSagBrainRenderer.AddActor(actorSagittal)        
    self.enhancedSagBrainRenderer.Render()        
    
  def moveHorAxEnhanced (self):
    if hasattr(self, 'axEnhancedActor'):
      self.axEnhancedActor.SetPosition(self.ui.vsHorAxEnhanced.value() - 100, self.ui.vsVerAxEnhanced.value())    
    if hasattr(self, 'axEnhancedGoldActor'):
      self.axEnhancedGoldActor.SetPosition(self.ui.vsHorAxEnhanced.value() - 100, self.ui.vsVerAxEnhanced.value())    
    if hasattr(self, 'axEnhancedSegmActor'):
      self.axEnhancedSegmActor.SetPosition(self.ui.vsHorAxEnhanced.value() - 100, self.ui.vsVerAxEnhanced.value())          
    self.enhancedAxBrainWidgetWindowInteractor.Render()    
    
  def moveVerAxEnhanced (self):
    if hasattr(self, 'axEnhancedActor'):
       self.axEnhancedActor.SetPosition(self.ui.vsHorAxEnhanced.value() - 100, self.ui.vsVerAxEnhanced.value())
    if hasattr(self, 'axEnhancedGoldActor'):
      self.axEnhancedGoldActor.SetPosition(self.ui.vsHorAxEnhanced.value() - 100, self.ui.vsVerAxEnhanced.value())
    if hasattr(self, 'axEnhancedSegmActor'):
      self.axEnhancedSegmActor.SetPosition(self.ui.vsHorAxEnhanced.value() - 100, self.ui.vsVerAxEnhanced.value())      
    self.enhancedAxBrainWidgetWindowInteractor.Render()   
    
  def moveZAxEnhanced (self):
    if hasattr(self, 'axEnhancedMapper'):
      self.axEnhancedMapper.SetZSlice(self.ui.vsZAxEnhanced.value())
    if hasattr(self, 'axEnhancedGoldMapper'):
      self.axEnhancedGoldMapper.SetZSlice(self.ui.vsZAxEnhanced.value())
    if hasattr(self, 'axEnhancedSegmMapper'):
      self.axEnhancedSegmMapper.SetZSlice(self.ui.vsZAxEnhanced.value())      
    self.enhancedAxBrainWidgetWindowInteractor.Render()
    
  def moveHorCorEnhanced (self):
    if hasattr(self, 'corEnhancedActor'):
      self.corEnhancedActor.SetPosition(self.ui.vsHorCorEnhanced.value() - 100, self.ui.vsVerCorEnhanced.value() + 150)
    if hasattr(self, 'corEnhancedGoldActor'):
      self.corEnhancedGoldActor.SetPosition(self.ui.vsHorCorEnhanced.value() - 100, self.ui.vsVerCorEnhanced.value() + 150)
    if hasattr(self, 'corEnhancedSegmActor'):
      self.corEnhancedSegmActor.SetPosition(self.ui.vsHorCorEnhanced.value() - 100, self.ui.vsVerCorEnhanced.value() + 150)      
    self.enhancedCorBrainWidgetWindowInteractor.Render()    
    
  def moveVerCorEnhanced (self):
    if hasattr(self, 'corEnhancedActor'):
      self.corEnhancedActor.SetPosition(self.ui.vsHorCorEnhanced.value() - 100, self.ui.vsVerCorEnhanced.value() + 150)
    if hasattr(self, 'corEnhancedGoldActor'):
      self.corEnhancedGoldActor.SetPosition(self.ui.vsHorCorEnhanced.value() - 100, self.ui.vsVerCorEnhanced.value() + 150)
    if hasattr(self, 'corEnhancedSegmActor'):
      self.corEnhancedSegmActor.SetPosition(self.ui.vsHorCorEnhanced.value() - 100, self.ui.vsVerCorEnhanced.value() + 150)        
    self.enhancedCorBrainWidgetWindowInteractor.Render()   
    
  def moveZCorEnhanced (self):
    if hasattr(self, 'corEnhancedMapper'):
      self.corEnhancedMapper.SetZSlice(self.ui.vsZCorEnhanced.value())
    if hasattr(self, 'corEnhancedGoldMapper'):
      self.corEnhancedGoldMapper.SetZSlice(self.ui.vsZCorEnhanced.value())
    if hasattr(self, 'corEnhancedSegmMapper'):
      self.corEnhancedSegmMapper.SetZSlice(self.ui.vsZCorEnhanced.value())      
    self.enhancedCorBrainWidgetWindowInteractor.Render() 
    
  def moveHorSagEnhanced (self):
    if hasattr(self, 'sagEnhancedActor'):
      self.sagEnhancedActor.SetPosition(self.ui.vsHorSagEnhanced.value() - 100, self.ui.vsVerSagEnhanced.value() + 150)
    if hasattr(self, 'sagEnhancedGoldActor'):
      self.sagEnhancedGoldActor.SetPosition(self.ui.vsHorSagEnhanced.value() - 100, self.ui.vsVerSagEnhanced.value() + 150)    
    if hasattr(self, 'sagEnhancedSegmActor'):
      self.sagEnhancedSegmActor.SetPosition(self.ui.vsHorSagEnhanced.value() - 100, self.ui.vsVerSagEnhanced.value() + 150)          
    self.enhancedSagBrainWidgetWindowInteractor.Render()    
    
  def moveVerSagEnhanced (self):
    if hasattr(self, 'sagEnhancedActor'):
      self.sagEnhancedActor.SetPosition(self.ui.vsHorSagEnhanced.value() - 100, self.ui.vsVerSagEnhanced.value() + 150)
    if hasattr(self, 'sagEnhancedGoldActor'):
      self.sagEnhancedGoldActor.SetPosition(self.ui.vsHorSagEnhanced.value() - 100, self.ui.vsVerSagEnhanced.value() + 150)     
    if hasattr(self, 'sagEnhancedSegmActor'):
      self.sagEnhancedSegmActor.SetPosition(self.ui.vsHorSagEnhanced.value() - 100, self.ui.vsVerSagEnhanced.value() + 150)      
    self.enhancedSagBrainWidgetWindowInteractor.Render()   
    
  def moveZSagEnhanced (self):
    if hasattr(self, 'sagEnhancedMapper'):
      self.sagEnhancedMapper.SetZSlice(self.ui.vsZSagEnhanced.value())
    if hasattr(self, 'sagEnhancedGoldMapper'):
      self.sagEnhancedGoldMapper.SetZSlice(self.ui.vsZSagEnhanced.value())  
    if hasattr(self, 'sagEnhancedSegmMapper'):
      self.sagEnhancedSegmMapper.SetZSlice(self.ui.vsZSagEnhanced.value())        
    self.enhancedSagBrainWidgetWindowInteractor.Render()      
    
  def moveGoldTransparency (self):
    if hasattr(self, 'lookupTableGoldSegOrig'):      
      self.lookupTableGoldSegOrig.SetTableValue( 1, 0.0, 1.0, 0.0, self.ui.vsGoldTransparency.value() * 1.0 / 100 )      
      self.originalAxBrainWidgetWindowInteractor.Render()
      self.originalCorBrainWidgetWindowInteractor.Render()
      self.originalSagBrainWidgetWindowInteractor.Render()
      
  def moveGoldTransparencyEnc (self):
    if hasattr(self, 'lookupTableGoldSegEnc'):      
      self.lookupTableGoldSegEnc.SetTableValue( 1, 0.0, 1.0, 0.0, self.ui.vsGoldTransparencyEnc.value() * 1.0 / 100 )      
      self.enhancedAxBrainWidgetWindowInteractor.Render()
      self.enhancedCorBrainWidgetWindowInteractor.Render()
      self.enhancedSagBrainWidgetWindowInteractor.Render()

  def moveSegTransparency (self):
    if hasattr(self, 'lookupTableSeg'):      
      self.lookupTableSeg.SetTableValue( 1, 1.0, 0.0, 0.0, self.ui.vsSegTransparency.value() * 1.0 / 100 )      
      self.originalAxBrainWidgetWindowInteractor.Render()
      self.originalCorBrainWidgetWindowInteractor.Render()
      self.originalSagBrainWidgetWindowInteractor.Render()
      
  def moveSegTransparencyEnc (self):
    if hasattr(self, 'lookupTableSegEnc'):      
      self.lookupTableSegEnc.SetTableValue( 1, 1.0, 0.0, 0.0, self.ui.vsSegTransparencyEnc.value() * 1.0 / 100 )            
      self.enhancedAxBrainWidgetWindowInteractor.Render()
      self.enhancedCorBrainWidgetWindowInteractor.Render()
      self.enhancedSagBrainWidgetWindowInteractor.Render()
      
  def moveOriginalWindow (self):
    if hasattr(self, 'axOriginalMapper'):      
      self.axOriginalMapper.SetColorWindow( self.ui.vsOriginalWindow.value())
      self.corOriginalMapper.SetColorWindow( self.ui.vsOriginalWindow.value())
      self.sagOriginalMapper.SetColorWindow( self.ui.vsOriginalWindow.value())    
      # Re-render every original view
      self.originalAxBrainWidgetWindowInteractor.Render()
      self.originalCorBrainWidgetWindowInteractor.Render()
      self.originalSagBrainWidgetWindowInteractor.Render()

  def moveOriginalLevel (self):
    if hasattr(self, 'axOriginalMapper'):      
      self.axOriginalMapper.SetColorLevel( self.ui.vsOriginalLevel.value())
      self.corOriginalMapper.SetColorLevel( self.ui.vsOriginalLevel.value())
      self.sagOriginalMapper.SetColorLevel( self.ui.vsOriginalLevel.value())
      # Re-render every original view
      self.originalAxBrainWidgetWindowInteractor.Render()
      self.originalCorBrainWidgetWindowInteractor.Render()
      self.originalSagBrainWidgetWindowInteractor.Render()
      
  def moveEnhancedWindow (self):
    if hasattr(self, 'axEnhancedMapper'):      
      self.axEnhancedMapper.SetColorWindow( self.ui.vsEnhancedWindow.value())
      self.corEnhancedMapper.SetColorWindow( self.ui.vsEnhancedWindow.value())
      self.sagEnhancedMapper.SetColorWindow( self.ui.vsEnhancedWindow.value())    
      # Re-render every original view
      self.enhancedAxBrainWidgetWindowInteractor.Render()
      self.enhancedCorBrainWidgetWindowInteractor.Render()
      self.enhancedSagBrainWidgetWindowInteractor.Render()

  def moveEnhancedLevel (self):
    if hasattr(self, 'axEnhancedMapper'):      
      self.axEnhancedMapper.SetColorLevel( self.ui.vsEnhancedLevel.value())
      self.corEnhancedMapper.SetColorLevel( self.ui.vsEnhancedLevel.value())
      self.sagEnhancedMapper.SetColorLevel( self.ui.vsEnhancedLevel.value())
      # Re-render every original view
      self.enhancedAxBrainWidgetWindowInteractor.Render()
      self.enhancedCorBrainWidgetWindowInteractor.Render()
      self.enhancedSagBrainWidgetWindowInteractor.Render()
         
  def computeMetrics (self):
    if hasattr(self, 'segmGoldData') and hasattr(self, 'segmData'):      
      originalSeg = self.segmGoldData
      newSeg = self.segmData
      intersection = 0.0
      total = 0.0
      c_double_p = ctypes.POINTER(ctypes.c_ubyte)
      totalIter = originalSeg.GetDimensions()[0] * originalSeg.GetDimensions()[1] * originalSeg.GetDimensions()[2]         
      count = 0
      
      for x in range(0, originalSeg.GetDimensions()[0]):
        for y in range(0, originalSeg.GetDimensions()[1]):
          for z in range(0, originalSeg.GetDimensions()[2]):
	    count = count + 1
	    if ( (originalSeg.GetScalarComponentAsFloat(x,y,z,0) != 0.0) and (newSeg.GetScalarComponentAsFloat(x,y,z,0) != 0.0) ):	      
	      intersection = intersection + 1
	      total = total + 2 
      	    if ( (originalSeg.GetScalarComponentAsFloat(x,y,z,0) == 0.0) and (newSeg.GetScalarComponentAsFloat(x,y,z,0) != 0.0) ):	      
	      total = total + 1          	      
      	    if ( (originalSeg.GetScalarComponentAsFloat(x,y,z,0) != 0.0) and (newSeg.GetScalarComponentAsFloat(x,y,z,0) == 0.0) ):	      
	      total = total + 1
	    self.ui.pbMetrics.setValue( int(count*100 / totalIter) )

      self.ui.pbMetrics.setValue(0)
      self.ui.lDiceCoefficient.setText(str(round(200 * intersection / total, 2)))     
      
  def show3dColored (self):
    
    ren = vtk.vtkRenderer()
    
        #Show 3d view of the gold segmentation
    if self.ui.chOriginalGold.isChecked() and self.ui.chOriginalSegm.isChecked():
      #Intersection
      if self.ui.chEnhancedIntersect.isChecked():
        intersection = vtk.vtkImageLogic()
        intersection.SetInput1(self.segmGoldData)
        intersection.SetInput2(self.segmData)
        intersection.SetOperationToAnd()
        intersection.Update()     
      
        isoIntersection = vtk.vtkMarchingCubes()
        isoIntersection.SetInput(intersection.GetOutput())
        isoIntersection.SetValue(0, 1)
        isoIntersection.Update()    
    
        decimatorIntersection = vtk.vtkDecimatePro()
        decimatorIntersection.SetInputConnection(isoIntersection.GetOutputPort())
        decimatorIntersection.SetTargetReduction(0.20)
        decimatorIntersection.Update()
        
        mapperIntersection = vtk.vtkPolyDataMapper()
        mapperIntersection.SetInputConnection(decimatorIntersection.GetOutputPort())      
        mapperIntersection.ScalarVisibilityOff()
        mapperIntersection.ImmediateModeRenderingOn()    

        actorIntersection = vtk.vtkActor()
        actorIntersection.SetMapper(mapperIntersection)  
        actorIntersection.GetProperty().SetColor([0.0, 0.0, 1.0])  
      
        ren.AddActor(actorIntersection)          
      
      #Only gold segmentation
      if self.ui.chEnhancedOnlyGold.isChecked():
        xorFilter1 = vtk.vtkImageLogic()
        xorFilter1.SetInput1(self.segmGoldData)
        xorFilter1.SetInput2(self.segmData)
        xorFilter1.SetOperationToXor()
        xorFilter1.Update()     
      
        onlyGold = vtk.vtkImageLogic()
        onlyGold.SetInput1(xorFilter1.GetOutput())
        onlyGold.SetInput2(self.segmGoldData)
        onlyGold.SetOperationToAnd()
        onlyGold.Update() 
      
        isoOnlyGold = vtk.vtkMarchingCubes()
        isoOnlyGold.SetInput(onlyGold.GetOutput())
        isoOnlyGold.SetValue(0, 1)
        isoOnlyGold.Update()    
    
        decimatorOnlyGold = vtk.vtkDecimatePro()
        decimatorOnlyGold.SetInputConnection(isoOnlyGold.GetOutputPort())
        decimatorOnlyGold.SetTargetReduction(0.20)
        decimatorOnlyGold.Update()
        
        mapperOnlyGold = vtk.vtkPolyDataMapper()
        mapperOnlyGold.SetInputConnection(decimatorOnlyGold.GetOutputPort())      
        mapperOnlyGold.ScalarVisibilityOff()
        mapperOnlyGold.ImmediateModeRenderingOn()    

        actorOnlyGold = vtk.vtkActor()
        actorOnlyGold.SetMapper(mapperOnlyGold)  
        actorOnlyGold.GetProperty().SetColor([0.0, 1.0, 0.0])  
      
        ren.AddActor(actorOnlyGold)   

      #Only segmentation
      if self.ui.chEnhancedOnlySeg.isChecked():
        xorFilter2 = vtk.vtkImageLogic()
        xorFilter2.SetInput1(self.segmGoldData)
        xorFilter2.SetInput2(self.segmData)
        xorFilter2.SetOperationToXor()
        xorFilter2.Update()     
      
        onlySeg = vtk.vtkImageLogic()
        onlySeg.SetInput1(xorFilter2.GetOutput())
        onlySeg.SetInput2(self.segmData)
        onlySeg.SetOperationToAnd()
        onlySeg.Update() 
      
        isoOnlySeg = vtk.vtkMarchingCubes()
        isoOnlySeg.SetInput(onlySeg.GetOutput())
        isoOnlySeg.SetValue(0, 1)
        isoOnlySeg.Update()    
    
        decimatorOnlySeg = vtk.vtkDecimatePro()
        decimatorOnlySeg.SetInputConnection(isoOnlySeg.GetOutputPort())
        decimatorOnlySeg.SetTargetReduction(0.20)
        decimatorOnlySeg.Update()
        
        mapperOnlySeg = vtk.vtkPolyDataMapper()
        mapperOnlySeg.SetInputConnection(decimatorOnlySeg.GetOutputPort())      
        mapperOnlySeg.ScalarVisibilityOff()
        mapperOnlySeg.ImmediateModeRenderingOn()    

        actorOnlySeg = vtk.vtkActor()
        actorOnlySeg.SetMapper(mapperOnlySeg)  
        actorOnlySeg.GetProperty().SetColor([1.0, 0.0, 0.0])  
      
        ren.AddActor(actorOnlySeg)   

    renWin = vtk.vtkRenderWindow()      
    
    renWin.AddRenderer(ren)
    
    renWin.SetSize(500, 500)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)          
    
    iren.Initialize()
    renWin.Render()
    iren.Start()      

#The python interpreter assigns the name main to this module when this program is being executed, 
#but not included into another one
if __name__ == "__main__":
 
#These are basic Qt commands
  #Define an application object
  app = QtGui.QApplication(['Vessel enhancement visualizer']) 
  #Instantiate an object  
  window = MyMainWindow() 
  window.show()
  window.originalAxBrainInteractor.Initialize()
  window.originalCorBrainInteractor.Initialize()
  window.originalSagBrainInteractor.Initialize()  
  window.enhancedAxBrainInteractor.Initialize()
  window.enhancedCorBrainInteractor.Initialize()
  window.enhancedSagBrainInteractor.Initialize()
  #Start the main loop of the application
  sys.exit(app.exec_())
  