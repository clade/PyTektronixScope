Overview
========

This package can be used to record data from a Tektronix scope. 


Installation
============

To install PyTektronixScope, download the package and run the command:: 

  python setup.py install

You can also directly move the PyTektronixScope directory to a location
that Python can import from (directory in which scripts 
using PyDAQmx are run, etc.)

Usage
=====

Typical usage::

  from PyTektronixScope import TektronixScope

  scope = TektronixScope(instrument_resource_name)
  X,Y = scope.read_data_one_channel('CH2', t0 = 0, DeltaT = 1E-6, x_axis_out=True)


Version history
===============
Main changes:

* 0.1 Initial relase
* 0.2 Update to new version of visa

