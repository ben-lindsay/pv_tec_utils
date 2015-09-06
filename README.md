# pv_tec_utils

Utilities to facilitate creating 3D images from .tec files in Paraview

### Installation

1. Copy pv_tec_utils.py into a folder in your PYTHONPATH.
2. Install [ParaView](http://www.paraview.org/download/) if you have not already done so.
3. Make sure the `paraview` module and the `vtk` submodules are in your `PYTHONPATH`. This can be done two different ways:
   1. **If you plan to use your usual Python executable:**
   Look in your ParaView application folder for a set of Python modules. On my Mac, the directory is `/Applications/paraview.app/Contents/Python`. On the [Stampede supercomputer](https://www.tacc.utexas.edu/stampede/) the path is `/opt/apps/intel15/mvapich2_2_1/paraview/4.3.1/lib/paraview-4.3/site-packages`. The contents of this directory should look something like this:
   ```bash
   $ ls /Applications/paraview.app/Contents/Python
   autobahn/   mpi4py/     paraview/   six.py     six.pyo    vtk/
   matplotlib/ numpy/      pygments/   six.pyc    twisted/   zope/
   ```
   Include the following line in your `~/.bashrc` file, replacing `$MODULEDIR` with this directory:
   ```bash
   export PYTHONPATH=$PYTHONPATH:$MODULEDIR:$MODULEDIR/vtk
   ```
   2. **If you're OK with using a different Python executable:**
   Find the `pvpython` executable in the `bin` directory with your ParaView tree. Use this executable every time you use a script that does anything with ParaView. For example, create an alias like
   ```bash
   alias pvpython='/Applications/paraview.app/Contents/bin/pvpython'
   ```
   in your `~/.bashrc` file and use that instead of `python` to call your ParaView scripts. This executable already has everything ParaView needs set up in its path.
