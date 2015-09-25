import pv_utils as utils 
import paraview.simple as pv

center = utils.GetCenter(tecFile='data/rhoda.tec')
renderView = pv.CreateRenderView( ViewSize=[700, 500],
                                  Background=[1.0, 1.0, 1.0] )
utils.ColorSurface( tecFile='data/rhoda.tec', view=renderView, opacity=1.0 )
utils.SetCameraFocus( tecFile='data/rhoda.tec', view=renderView, camFoc=center )
utils.SetOrientation( view=renderView, camPosDir=[-1.0, -0.5, 0.3] )
pv.SaveScreenshot('surface.png', magnification=1, quality=100, view=renderView)
