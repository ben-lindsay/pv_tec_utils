# pv_tec_utils

Utilities to facilitate creating 3D images from .tec files in Paraview

### Installation

1. Copy pv_tec_utils.py into a folder in your PYTHONPATH.
2. Install [ParaView](http://www.paraview.org/download/) if you have not already done so.
3. Somewhere in your ParaView application folder is a set of Python modules. On my Mac, the directory is `/Applications/paraview.app/Contents/Python`. On the [Stampede supercomputer](https://www.tacc.utexas.edu/stampede/) the path is `/opt/apps/intel15/mvapich2_2_1/paraview/4.3.1/lib/paraview-4.3/site-packages`. The contents of this directory should look something like this:

```bash
$ ls /Applications/paraview.app/Contents/Python
autobahn/   mpi4py/     paraview/   six.py     six.pyo    vtk/
matplotlib/ numpy/      pygments/   six.pyc    twisted/   zope/
```
