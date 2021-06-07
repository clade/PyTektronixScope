# -*- coding: utf-8 -*-
import sys

#from distutils.core import setup
from setuptools import setup

long_description='''\
Overview
========

This package can be used to record data from a Tektronix scope. 


Installation
============

You need first to install the `PyVISA`_ package. 
To install PyTektronixScope, download the package and run the command:: 

  python setup.py install

You can also directly move the PyTektronixScope directory to a location
that Python can import from (directory in which scripts 
using PyDAQmx are run, etc.)

Sources can also be download on the `PyTektronixScope github repository`_. 

Usage
=====

Typical usage::

  from PyTektronixScope import PyTektronixScope

  scope = TektronixScope(instrument_resource_name)
  X,Y = scope.read_data_one_channel('CH2', t0 = 0, DeltaT = 1E-6, x_axis_out=True)

Contact
=======

Please send bug reports or feedback to `Pierre Clade`_.

Version history
===============
Main changes:

* 0.1 Initial relase
* 0.2 Update to new version of visa
* 0.2.1 Misc. bugs

.. _Pierre Clade: mailto:pierre.clade@spectro.jussieu.fr
.. _PyTektronixScope github repository: https://github.com/clade/PyTektronixScope
.. _PyVISA: http://pyvisa.sourceforge.net/
'''


# There is a problem with writing unicode to a file on version of python <2.6
# So I remove the accent of the author name in this case
# TODO: find an automatic way of removing accent if version<2.6
if sys.version_info[:2]>=(2,6): # Unicode accent does not work on earlier version
    setup(name="PyTektronixScope", version='0.2.1',
      author=u'Pierre Cladé', author_email="pierre.clade@spectro.jussieu.fr",
      maintainer=u'Pierre Cladé',
      maintainer_email="pierre.clade@spectro.jussieu.fr",
      url='https://github.com/clade/PyTektronixScope',
      license='''\
This software can be used under one of the following two licenses: \
(1) The BSD license. \
(2) Any other license, as long as it is obtained from the original \
author.''',

      description='Interface to Tektronix Scope',
      long_description = long_description,  
      keywords=['Tektronix', 'scope', 'Data Acquisition'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'], 
     requires=['pyvisa'],
     packages=["PyTektronixScope"]

)
else: # version of python <2.6. Remove the unicode  
      setup(name="PyTektronixScope", version='0.2.1',
      author='Pierre Clade', author_email="pierre.clade@spectro.jussieu.fr",
      maintainer='Pierre Clade',
      maintainer_email="pierre.clade@spectro.jussieu.fr",
      url='https://github.com/clade/PyTektronixScope',
      license='''\
This software can be used under one of the following two licenses: \
(1) The BSD license. \
(2) Any other license, as long as it is obtained from the original \
author.''',

      description='Interface to the National Instrument PyDAQmx driver',

      long_description = long_description,

      keywords=['Tektronix', 'scope', 'Data Acquisition'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'], 
     requires=['pyvisa'],
     packages=["PyTektronixScope"]

)
