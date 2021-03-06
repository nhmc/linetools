# Module to run tests on spectra.io
from __future__ import print_function, absolute_import, \
     division, unicode_literals
import os
import pytest
import astropy.io.ascii as ascii
from astropy import units as u
import numpy as np
from astropy.io import fits

from linetools.spectra import io
from linetools.spectra.xspectrum1d import XSpectrum1D


def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'files')
    return os.path.join(data_dir, filename)

# From arrays
def test_from_tuple():
    idl = ascii.read(data_path('UM184.dat.gz'), names=['wave', 'flux', 'sig'])
    spec = XSpectrum1D.from_tuple((idl['wave'],idl['flux'],idl['sig']))
    #
    np.testing.assert_allclose(spec.dispersion.value, idl['wave'])
    np.testing.assert_allclose(spec.sig, idl['sig'], atol=2e-3, rtol=0)

    assert spec.dispersion.unit == u.Unit('AA')

# From Table
#def test_from_table():

# From file
def test_from_file():
    spec = XSpectrum1D.from_file(data_path('UM184_nF.fits'))
    idl = ascii.read(data_path('UM184.dat.gz'), names=['wave', 'flux', 'sig'])

    np.testing.assert_allclose(spec.dispersion.value, idl['wave'])
    np.testing.assert_allclose(spec.sig, idl['sig'], atol=2e-3, rtol=0)

    assert spec.dispersion.unit == u.Unit('AA')

# Attributes
def test_attrib():
    spec = io.readspec(data_path('UM184_nF.fits'))
    # 
    np.testing.assert_allclose(spec.wvmin.value, 3056.6673905210096)
    #np.testing.assert_allclose(spec.median_s2n,18.383451461791992)


