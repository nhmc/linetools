# Module to run tests on spectra.io
from __future__ import print_function, absolute_import, \
     division, unicode_literals
import os
import pytest
import pdb
from astropy import units as u
import numpy as np
from astropy.io import fits, ascii
from astropy.table import QTable, Table, Column

from linetools.spectra import io
from linetools.spectra.xspectrum1d import XSpectrum1D

def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'files')
    return os.path.join(data_dir, filename)

# Rel vel
def test_addnoise():
    spec = io.readspec(data_path('UM184_nF.fits'))
    #
    spec.add_noise(seed=12)
    np.testing.assert_allclose(spec.flux[1000], 0.44806158542633057)

    # With S/N input
    spec.add_noise(seed=19,s2n=10.)
    np.testing.assert_allclose(spec.flux[1000], 0.24104823059199412)

# Box car smooth
def test_box_smooth():
    spec = io.readspec(data_path('UM184_nF.fits'))

    # Smooth
    newspec3 = spec.box_smooth(3)
    np.testing.assert_allclose(newspec3.flux[4000], 0.9967582821846008)
    assert newspec3.flux.unit == u.dimensionless_unscaled

    newspec5 = spec.box_smooth(5)
    np.testing.assert_allclose(newspec5.flux[3000], 1.086308240890503)

# Gaussian smooth
def test_gauss_smooth():
    spec = io.readspec(data_path('UM184_nF.fits'))

    # Smooth
    smth_spec = spec.gauss_smooth(4.)
    # Test
    np.testing.assert_allclose(smth_spec.flux[3000].value, 0.8288110494613)
    assert smth_spec.flux.unit == spec.flux.unit

# Rebin
def test_rebin():
    spec = io.readspec(data_path('UM184_nF.fits'))
    # Rebin
    new_wv = np.arange(3000., 9000., 5) * u.AA
    newspec = spec.rebin(new_wv)
    # Test

    np.testing.assert_allclose(newspec.flux[1000], 0.9999280967617779)
    assert newspec.flux.unit == u.dimensionless_unscaled

# Rel vel
def test_relvel():
    spec = io.readspec(data_path('UM184_nF.fits'))

    # Velocity
    velo = spec.relative_vel(5000.*u.AA)
    # Test
    np.testing.assert_allclose(velo[6600].value, -3716.441360213781)
    assert velo.unit == (u.km/u.s)

# Repr
def test_repr():
    spec = io.readspec(data_path('UM184_nF.fits'))
    print(spec)

# Write FITS
def test_write_ascii():
    spec = io.readspec(data_path('UM184_nF.fits'))
    # Write. Should be replaced with tempfile.TemporaryFile
    spec.write_to_ascii(data_path('tmp.ascii'))
    # 
    spec2 = io.readspec(data_path('tmp.ascii'))
    # check a round trip works
    np.testing.assert_allclose(spec.dispersion, spec2.dispersion)

# Write FITS
def test_write_fits():
    spec = io.readspec(data_path('UM184_nF.fits'))

    # Write. Should be replaced with tempfile.TemporaryFile
    spec.write_to_fits(data_path('tmp.fits'))
    spec2 = io.readspec(data_path('tmp.fits'))
    # check a round trip works
    np.testing.assert_allclose(spec.dispersion, spec2.dispersion)

def test_readwrite_without_sig():
    sp = XSpectrum1D.from_tuple(([5,6,7], np.ones(3)))
    sp.write_to_fits(data_path('tmp.fits'))
    sp1 = io.readspec(data_path('tmp.fits'))
    np.testing.assert_allclose(sp1.dispersion.value, sp.dispersion.value)
    np.testing.assert_allclose(sp1.flux.value, sp.flux.value)

def test_readwrite_metadata():
    spec = io.readspec(data_path('UM184_nF.fits'))
    d = {'a':1, 'b':'abc', 'c':3.2, 'd':np.array([1,2,3]),
         'e':dict(a=1,b=2)}
    spec.meta.update(d)
    spec.write_to_fits(data_path('tmp.fits'))
    spec2 = io.readspec(data_path('tmp.fits'))
    assert spec2.meta['a'] == d['a']
    assert spec2.meta['b'] == d['b']
    np.testing.assert_allclose(spec2.meta['c'], d['c'])
    np.testing.assert_allclose(spec2.meta['d'], d['d'])
    assert spec2.meta['e'] == d['e']

def test_copy():
    spec = io.readspec(data_path('UM184_nF.fits'))
    spec2 = spec.copy()
    assert spec.wavelength[0] == spec2.wavelength[0]
    assert spec.flux[-1] == spec2.flux[-1]
