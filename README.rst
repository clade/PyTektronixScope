Overview
========

This package can be used to record data from a Tektronix scope. 


Installation
============

To install PyTektronixScope, download the package, navigate to the directory in
which you downloaded the repository, and run the command:: 

  pip install .

You can also directly move the PyTektronixScope directory to a location
that Python can import from.

This package has been tested with ``pyvisa``.

Usage
=====

Typical usage : 

  from PyTektronixScope import TektronixScope

  scope = TektronixScope(instrument_resource_name)
  X, Y = scope.read_data_one_channel('CH2', t0=0, DeltaT=1E-6, x_axis_out=True)

where ``instrument_resource_name`` is the resource name of your device. You can get
the resource name of all connected devices using the following::

    import pyvisa
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

If only one supported oscilloscope is connected, you can simplify use::

  scope = TektronixScope()

The detection algorithm only covers a small selection [1]_ of
all supported Tektronix oscilloscopes. 

You can also pass any object that implements a ``write`` and ``query`` method.
  
.. [1] Currently, the automatic detection works with TDS2004B, TDS2024B,
   DPO2024, DPO2024B and DPO4104.

Version history
===============
Main changes:

* 0.1 Initial relase
* 0.2 Update to new version of visa
* 0.3 Introduce automatic device detection
