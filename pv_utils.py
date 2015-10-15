r"""pv_utils is a module that facilitates creating 3D images of data from
.tec files using ParaView's server manager in Python.

"""
#==============================================================================
#
#   Module:     pv_utils.py
#   Author:     Ben Lindsay
#   Date:       October 2015
#
#==============================================================================


from paraview.simple import *
import numpy as np
from os.path import isfile

def InitView(viewSize=[700, 500], color=[1.0, 1.0, 1.0], noAxisArrows=True,
             offScreenRender=True):
    view = CreateRenderView(ViewSize=viewSize, Background=color)
    if noAxisArrows:
        view.OrientationAxesVisibility = 0
    #if offScreenRender:
    #    view.UseOffscreenRendering = 1
    return view

def GetCenter(tecFile=None):
    if not tecFile:
        raise ValueError, "No .tec file name was provided to GetCenter()"
    if not isfile(tecFile):
        raise IOError, "%s does not exist" % tecFile
    # Load data skipping top 3 lines (.tec files have a 3-line header)
    file = open(tecFile)
    data = np.loadtxt(file, skiprows=3)
    file.close()
    # Get arrays of max and min x,y,z values
    xyz_max = data.max(axis=0)[:3]
    xyz_min = data.min(axis=0)[:3]
    # Return [x_center, y_center, z_center] array
    center = (xyz_min + xyz_max) / 2.0
    return list(center)

# -----------------------------------------------------------------------------

def ColorSurface(tecFile=None, view=None, opacity=1.0, showColorBar=False):
    if not tecFile:
        raise ValueError, "No .tec file name was provided to ColorSurface()"
    if not isfile(tecFile):
        raise IOError, "%s does not exist" % tecFile
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to ColorSurface()"
    # Create a TecplotReader for the input .tec file name
    tecReader = TecplotReader(FileNames=[tecFile])
    tecReader.DataArrayStatus = ['Real']
    # Turn on visibility of tecReader object in view
    tecDisplay = Show(tecReader, view)
    # Color surface of object by the values of 'Real' column in .tec file
    tecDisplay.Representation = 'Surface'
    ColorBy(tecDisplay, ('POINTS', 'Real'))
    tecDisplay.Opacity = opacity
    tecDisplay.RescaleTransferFunctionToDataRange(True)
    if showColorBar:
        # Turn on color bar as is done by default in Paraview
        tecDisplay.SetScalarBarVisibility(view, True)
        # Set color bar text color to black using internal function
        SetColorBarTextColor([0.0, 0.0, 0.0], view)
    # Reset the camera so the object fits nicely on the canvas
    view.ResetCamera()
    return tecDisplay

# -----------------------------------------------------------------------------

def NewContour(tecFile=None, view=None, isoFrac=0.5,
               opacity=1.0, color=[0.0, 0.0, 0.0]):
    if not tecFile:
        raise ValueError, "No .tec file name was provided to NewContour()"
    if not isfile(tecFile):
        raise IOError, "%s does not exist" % tecFile
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to NewContour()"
    # Create a TecplotReader for the input .tec file name
    tecReader = TecplotReader(FileNames=[tecFile])
    tecReader.DataArrayStatus = ['Real']
    # Create a contour from the TecplotReader object
    contour = Contour(Input=tecReader)
    contour.ContourBy = ['POINTS', 'Real']
    # Open .tec file
    file = open(tecFile)
    # Read in data from .tec file skipping the 3-line header
    # This data can have as many columns as you want, but the first 4 must be
    # x, y, z, and f(x, y, z) in that order. Currently the 4th column must be
    # labeled as 'Real'
    data = np.loadtxt(file, skiprows=3)
    # Get max and min f values from 4th column
    fMax = data.max(axis=0)[3]
    fMin = data.min(axis=0)[3]
    # Get the f value at which the iso-surface will be drawn based on a
    # fraction (isoFrac) between the max and min f values
    fIso = isoFrac * (fMax + fMin) # Get rhoda for isosurface
    # Create the isosurface and set its color
    contour.Isosurfaces = [fIso]
    contourDisplay = Show(contour, view)
    contourDisplay.DiffuseColor = color
    contourDisplay.Opacity = opacity
    # Reset the camera to so the object fits nicely in the canvas, just for
    # good measure
    view.ResetCamera()
    return contourDisplay

# -----------------------------------------------------------------------------

def NewSlice(tecFile=None, view=None, originVec=None,
             normVec=[1.0, 0.0, 0.0], opacity=1.0, showColorBar=False):
    if not tecFile:
        raise ValueError, "No .tec file name was provided to NewSlice()"
    if not isfile(tecFile):
        raise IOError, "%s does not exist" % tecFile
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to NewSlice()"
    if type(originVec)==type(None):
        # If originVec wasn't provided, use the center
        originVec = GetCenter(tecFile)
    # Create a TecplotReader for the input .tec file name
    tecReader = TecplotReader(FileNames=[tecFile])
    tecReader.DataArrayStatus = ['Real']
    # Create a slice from the TecplotReader object
    slice = Slice(Input=tecReader)
    slice.SliceType = 'Plane'
    # Set the origin about which the slice can pivot
    slice.SliceType.Origin = originVec
    # Rotate the slice by setting the normal vector to the plane
    slice.SliceType.Normal = normVec
    # Turn on visibility of slice, color, and set opacity
    sliceDisplay = Show(slice, view)
    ColorBy(sliceDisplay, ('POINTS', 'Real'))
    sliceDisplay.Opacity = opacity
    # Rescale color bar to fit data range
    sliceDisplay.RescaleTransferFunctionToDataRange(True)
    if showColorBar:
        # Turn on color bar as is done by default in Paraview
        sliceDisplay.SetScalarBarVisibility(view, True)
        # Set color bar text color to black using internal function
        SetColorBarTextColor([0.0, 0.0, 0.0], view)
    # Reset the camera so the object fits nicely on the canvas
    view.ResetCamera()
    return sliceDisplay

# -----------------------------------------------------------------------------

def SetColorBarTextColor(color=[0.0, 0.0, 0.0], view=None):
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to " + \
                          "SetColorBarTextColor()"
    realLUT = GetColorTransferFunction('Real')
    realLUTColorBar = GetScalarBar(realLUT, view)
    realLUTColorBar.LabelColor = color
    realLUTColorBar.TitleColor = color

# -----------------------------------------------------------------------------

def TurnOffColorBar(tecDisplay=None, view=None):
    if not tecDisplay:
        raise ValueError, "No tecDisplay object was provided to " + \
                          "TurnOffColorBar()"
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to TurnOffColorBar()"
    tecDisplay.SetScalarBarVisibility(view, False)

# -----------------------------------------------------------------------------

def TurnOnColorBar(tecDisplay=None, view=None):
    if not tecDisplay:
        raise ValueError, "No tecDisplay object was provided to " + \
                          "TurnOnColorBar()"
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to TurnOnColorBar()"
    tecDisplay.SetScalarBarVisibility(view, True)

# -----------------------------------------------------------------------------

def TurnOffAxisArrows(view=None):
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to TurnOffAxisArrows()"
    view.OrientationAxesVisibility = 0

# -----------------------------------------------------------------------------

def TurnOnAxisArrows(view=None):
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to TurnOnAxisArrows()"
    view.OrientationAxesVisibility = 1

# -----------------------------------------------------------------------------

def RescaleColorBar(tecDisplay=None, view=None, low=0.0, high=1.0):
    if not tecDisplay:
        raise ValueError, "No tecDisplay object was provided to " + \
                          "RescaleColorBar()"
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to RescaleColorBar()"
    # get color legend/bar for realLUT in view
    realLUT = GetColorTransferFunction('Real')
    # Tell ParaView not to rescale color maps to exactly fit the data range
    tecDisplay.RescaleTransferFunctionToDataRange(False)
    # Rescale transfer function
    realLUT.RescaleTransferFunction(low, high)

# -----------------------------------------------------------------------------

def AutoscaleColorBar(tecDisplay=None):
    if not tecDisplay:
        raise ValueError, "No tecDisplay object was provided to " + \
                          "AutoscaleColorBar()"
    # Tell ParaView to rescale color maps to exactly fit the data range
    tecDisplay.RescaleTransferFunctionToDataRange(True)

# -----------------------------------------------------------------------------

def SetCameraFocus(tecFile=None, view=None, camFoc=None):
    if not tecFile:
        raise ValueError, "No .tec file name was provided to SetCameraFocus()"
    if not isfile(tecFile):
        raise IOError, "%s does not exist" % tecFile
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to SetCameraFocus()"
    if not camFoc:
        # If camera focal point [x_foc, y_foc, z_foc] is not provided, set
        # camFoc to the center point of the data in the provided .tec file
        camFoc = GetCenter(tecFile)
    # Set camera focal point
    view.CameraFocalPoint = camFoc

# -----------------------------------------------------------------------------

def SetOrientation(view=None, camPosDir=[-1.0, 0.0, 0.0],
                   upDir=[0.0, 0.0, 1.0], resetCamera=True):
    if not view:
        # If view wasn't provided, get view from server manager
        # or create new one if one hasn't been created
        view = GetRenderView()
    if not view:
        raise ValueError, "No view was provided to SetOrientation()"
    # Get the camera focal point (should have already set this using
    # SetCameraFocus)
    camFoc = view.CameraFocalPoint
    # Set the camera position to the focal point vector + the vector
    # representing the arrow pointing from the focal point to the camera.
    # The magnitude of the vector doesn't matter if we're resetting the camera
    view.CameraPosition = np.array(camFoc) + np.array(camPosDir)
    # Set the direction that points directly up, i.e. if you want the
    # z-direction to point up, use upDir = [0.0, 0.0, 1.0]
    view.CameraViewUp = upDir
    if resetCamera:
        view.ResetCamera()
