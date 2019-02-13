from astropy.io import fits
from astropy.time import Time
from astropy.coordinates import cartesian_to_spherical
from astropy.constants import R_earth
from gbm import TIME_OFFSET
import numpy


PATHS = ['/atlas/recent/fermi/gbm/daily/',
         'https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/daily/']

pattern = "20{0:02d}/{1:02d}/{2:02d}/current/glg_poshist_all_{0:02d}{1:02d}{2:02d}_v00.fit"

def xyzposition(time):
    dt = Time(time, format='gps', scale='utc').datetime
    for path in PATHS:
        try:
            name = path + pattern.format(dt.year-2000, dt.month, dt.day)
            d = fits.open(name)
            break
        except:
            pass

    xv = d[1].data['POS_X']
    yv = d[1].data['POS_Y']
    zv = d[1].data['POS_Z']
    tv = d[1].data['SCLK_UTC'] + TIME_OFFSET
    x = numpy.interp(time, tv, xv)
    y = numpy.interp(time, tv, yv)
    z = numpy.interp(time, tv, zv)
    return x, y, z

def earth_xyzposition(time):
    return tuple(numpy.array(xyzposition(time))*-1)

def earth_position(time):
    x, y, z = earth_xyzposition(time)
    d, dec, ra = cartesian_to_spherical(x, y, z)
    return ra.value, dec.value
