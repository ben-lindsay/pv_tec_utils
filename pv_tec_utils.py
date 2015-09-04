from paraview.simple import *
import numpy as np

def InitRenderView(size):
    rv = CreateView('RenderView')
    rv.ViewSize = size
    rv.Background = [1.0, 1.0, 1.0]
    return rv

def ColorSurface(comp, rv, alpha):
    fname = comp + '.tec'
    tecReader = TecplotReader(FileNames=[fname])
    tecReader.DataArrayStatus = ['Real']
    tecDisplay = Show(tecReader, rv)
    tecDisplay.Representation = 'Surface'
    ColorBy(tecDisplay, ('POINTS', 'Real'))
    tecDisplay.RescaleTransferFunctionToDataRange(True)
    tecDisplay.SetScalarBarVisibility(rv, True)
    tecDisplay.Opacity = alpha
    rv.ResetCamera()
    return tecDisplay

def MakeContour(comp, rv, isofrac, alpha, color):
    fname = comp + '.tec'
    tecReader = TecplotReader(FileNames=[fname])
    tecReader.DataArrayStatus = ['Real']
    contour = Contour(Input=tecReader)
    contour.ContourBy = ['POINTS', 'Real']
    f = open(fname)
    X = np.loadtxt(f, skiprows=3) # Load data skipping top 3 lines
    rhomax = X.max(axis=0)[3] # Get maximum rhoda
    rhomin = X.min(axis=0)[3] # Get minimum rhoda
    iso = isofrac * (rhomax + rhomin) # Get rhoda for isosurface
    contour.Isosurfaces = [iso]
    contourDisplay = Show(contour, rv)
    contourDisplay.DiffuseColor = color
    rv.ResetCamera()
    return contourDisplay

def MakeSlice(comp, rv, centerVec, normVec):
    fname = comp + '.tec'
    tecReader = TecplotReader(FileNames=[fname])
    tecReader.DataArrayStatus = ['Real']
    slice = Slice(Input=tecReader)
    slice.SliceType = 'Plane'
    slice.SliceType.Origin = centerVec
    slice.SliceType.Normal = normVec
    sliceDisplay = Show(slice, rv)
    return sliceDisplay

def BlackColorBarText(rv):
    rv.ResetCamera()
    realLUT = GetColorTransferFunction('Real')
    realLUTColorBar = GetScalarBar(realLUT, rv)
    realLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
    realLUTColorBar.TitleColor = [0.0, 0.0, 0.0]

def TurnOffArrows(rv):
    rv.OrientationAxesVisibility = 0

def TurnOffColorbar(tecDisplay, rv):
    tecDisplay.SetScalarBarVisibility(rv, False)

def RescaleColorbar(tecDisplay, rv, low, high):
    # get opacity transfer function/opacity map for 'Real'
    # realPWF = GetOpacityTransferFunction('Real')
    # realPWF.Points = [-73.36000061035156, 0.0, 0.5, 0.0,
    #                    307.6000061035156, 1.0, 0.5, 0.0 ]
    # realPWF.ScalarRangeInitialized = 1
    
    # Rescale transfer function
    # realPWF.RescaleTransferFunction(low, high)
    
    # get color legend/bar for realLUT in view renderView1
    realLUT = GetColorTransferFunction('Real')
    # realLUTColorBar = GetScalarBar(realLUT, rv)
    # realLUTColorBar.Title = 'Real'
    # realLUTColorBar.ComponentTitle = ''
    
    # rescale color and/or opacity maps used to exactly fit the current data range
    tecDisplay.RescaleTransferFunctionToDataRange(False)
    
    # Rescale transfer function
    realLUT.RescaleTransferFunction(low, high)

def SetCameraFocus(comp, rv):
    fname = comp + '.tec'
    f = open( fname )
    X = np.loadtxt(f, skiprows=3) # Load data skipping top 3 lines
    xyz_range = X.max(axis=0)[:3] # Get [max x, max y, max z]
    camFoc = xyz_range / 2 # Get [center x, center y, center z] by div-ing by 2
    f.close()
    rv.CameraFocalPoint = camFoc
    return camFoc

def SetOrientation(camPos, upDir, rv):
    rv.CameraPosition = camPos
    rv.CameraViewUp = upDir
    # rv.CameraParallelScale = 0
