import sys
import os
pvpath = '/opt/apps/intel15/mvapich2_2_1/paraview/4.3.1/lib/paraview-4.3/'
sys.path.append(os.path.abspath(pvpath + 'site-packages'))
sys.path.append(os.path.abspath(pvpath + 'site-packages/vtk'))
import pv_tec_utils as utils 
import paraview.simple as pv
import numpy as np

center = utils.GetCenter(tecFile='data/rhoda.tec')
renderView = pv.CreateRenderView( ViewSize=[700, 500],
                                  Background=[1.0, 1.0, 1.0] )
utils.ColorSurface( tecFile='data/rhoda.tec', view=renderView, opacity=0.5 )
utils.SetCameraFocus( tecFile='data/rhoda.tec', view=renderView, camFoc=center )
utils.SetOrientation( view=renderView, camPosDir=[-1.0, -0.5, 0.3] )
pv.SaveScreenshot('surface.png', magnification=1, quality=100, view=renderView)
