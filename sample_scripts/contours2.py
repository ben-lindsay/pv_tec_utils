import pv_utils as utils 
import paraview.simple as pv

rdaTec = 'data/rhoda.tec'
rhcTec = 'data/rhohc.tec'
rnpTec = 'data/rho_fld_np.tec'
surfTec = 'data/rho_surf.tec'
white = [1.0, 1.0, 1.0]
red = [0.67, 0.0, 0.0]
green = [0.0, 0.67, 0.0]
gold = [1.0, 0.85, 0.0]
black = [0.0, 0.0, 0.0]

center = utils.GetCenter(tecFile=rdaTec)
renderView = pv.CreateRenderView( ViewSize=[700, 500], Background=white )
utils.ColorSurface( tecFile=rdaTec, opacity=0.5 )
utils.NewContour( tecFile=rdaTec, color=red, opacity=0.5 )
utils.NewContour( tecFile=rhcTec, color=green, opacity=0.5 )
utils.NewContour( tecFile=rnpTec, color=gold, opacity=1.0)
utils.NewContour( tecFile=surfTec, color=black, opacity=0.5 )
utils.SetCameraFocus( tecFile=rdaTec )
utils.SetOrientation( camPosDir=[-1.0, -0.5, 0.3] )
pv.SaveScreenshot('contours2.png')
