.. highlight:: rest

****************
linetool Scripts
****************


Quick Plots
===========

lt_absline
----------

Simple script to plot a single absorption line.
Requires the rest wavelength (Ang), log10 column density, and 
Doppler parameter (km/s). 

Here is a simple example::

	lt_absline 1215.6701 14.0 30

A plot will appear and the line info and EW as well, i.e. ::

	[AbsLine: HI 1215, wrest=1215.6700 Angstrom]
	EW = 0.268851 Angstrom

Try:: 

	lt_absline -h

for the full set of options.
