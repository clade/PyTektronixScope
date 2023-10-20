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

Typical usage when only one supported oscilloscope is connected::

  from PyTektronixScope import TektronixScope

  scope = TektronixScope()
  X, Y = scope.read_data_one_channel('CH2', t0=0, DeltaT=1E-6, x_axis_out=True)

It might be sensible to explicitly define which oscilloscope your instance of
TektronixScope should address, e.g. when multiple devices are connected.
Moreover, this allows using device types for which the automatic detection
fails - the detection algorithm only covers a small selection[1]_ of
all supported Tektronix oscilloscopes. Pass a valid VISA resource name as a
string to TektronixScope to address this particular resource. More information
about VISA resource names can be found in the `PyVISA documentation
<https://pyvisa.readthedocs.io/>`_. You can also pass a PyVISA resource
instead. Provided that you have a DP2024 (this model has the device id
0x0374) with the series number C000683 on USB0, you can use it like this::

  from PyTektronixScope import TektronixScope

  instrument_resource_name = 'USB0::0x0699::0x0374::C000683::INSTR'
  scope = TektronixScope(instrument_resource_name)
  X, Y = scope.read_data_one_channel('CH2', t0=0, DeltaT=1E-6, x_axis_out=True)
  
.. [1] Currently, the automatic detection works with TDS2004B, TDS2024B,
   DPO2024, DPO2024B and DPO4104.

Version history
===============
Main changes:

* 0.1 Initial relase
* 0.2 Update to new version of visa
* 0.3 Introduce automatic device detection
