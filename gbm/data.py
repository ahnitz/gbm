""" Qeury GBM data
"""
import os, numpy
import astropy.io.fits as fits
from astropy.utils.data import download_file
from astropy.time import Time
from urllib2 import HTTPError
from gbm import TIME_OFFSET

nfiles = 24

PATHS = ['/home/ahnitz/projects/gwgrb/fermi/heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/daily/{}/{:02d}/{:02d}/current',
         '/atlas/recent/fermi/gbm/daily/{}/{:02d}/{:02d}/current',
         'https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/daily/{}/{:02d}/{:02d}/current']

CHANNELS = [4.525152, 5.44399, 6.3488774, 7.242544, 8.127722, 9.00714, 9.88353, 10.759623, 11.814384, 12.87737, 13.953295, 15.046664, 16.158535, 17.287188, 18.430826, 19.781616, 21.148579, 22.537933, 23.959501, 25.423134, 26.93867, 28.746897, 30.65047, 32.664085, 34.506603, 35.901306, 37.49628, 39.12609, 40.78905, 42.483486, 44.40107, 46.353138, 48.337387, 50.35152, 52.59883, 54.876453, 57.181316, 59.51036, 62.07511, 64.66102, 67.2641, 70.09887, 72.94407, 75.79465, 78.86471, 81.928825, 84.98232, 88.24256, 91.49262, 94.73412, 98.1841, 101.62812, 105.068146, 108.720985, 112.37386, 116.24428, 120.120155, 124.220215, 128.33057, 132.6683, 137.01732, 141.37752, 145.9677, 150.57002, 155.40446, 160.47269, 165.55516, 170.87367, 176.20741, 181.77946, 187.36775, 193.19664, 199.26793, 205.3576, 211.69203, 218.27307, 224.87463, 231.72516, 238.82654, 246.18068, 253.55856, 261.19153, 269.08148, 277.23032, 285.40594, 293.84265, 302.5423, 311.5067, 320.73773, 330.2371, 340.0066, 350.0479, 360.36273, 370.95267, 381.8193, 392.96414, 404.38858, 416.09396, 428.3267, 440.84436, 453.64807, 466.7388, 480.11728, 494.03314, 508.2395, 522.73676, 537.776, 553.1077, 568.984, 585.1533, 601.8686, 618.8764, 636.4302, 654.52997, 672.9196, 691.85297, 711.3284, 731.34406, 751.89716, 772.72705, 794.08655, 815.97095, 838.3748, 861.2916, 884.97144, 909.1482, 945.6184, 983.2799, 2000.0]
CHANNELS = numpy.array(CHANNELS)

def get_path(year, month, day, hour, detector_num):
    for path in PATHS:
        pattern = 'glg_tte_n{:X}_{:02d}{:02d}{:02d}_{:02d}z_v00.fit.gz'
        pname = path.format(year, month, day)
        fname = pattern.format(detector_num, int(str(year)[-2:]), month, day, hour)
        full_path = os.path.join(pname, fname.lower())
        if os.path.isfile(full_path):
            return full_path
        elif 'http' in full_path:
            return full_path

def get_paths_covering(start_time, end_time, detector_num):
    t = Time(start_time, format='gps', scale='utc')

    rounded = t.datetime.replace(minute=0, second=0)
    ftime = Time(rounded)
    fnames = []

    while ftime.gps < end_time:
        fnames.append(get_path(ftime.datetime.year, ftime.datetime.month,
                               ftime.datetime.day, ftime.datetime.hour,
                               detector_num))

        ftime = Time(ftime.gps + 3600, format='gps', scale='utc')
    return fnames

def get_data(start_time, end_time, detector_num, fault_tolerant=False):
    fnames = get_paths_covering(start_time, end_time, detector_num)
    times = [[],]
    channels = [[],]
    for fname in fnames:

        if fname[0:4] == 'http':
            try:
                fname = download_file(fname, cache=True)
            except HTTPError as e:
                if fault_tolerant:
                    continue
                else:
                    raise e


        f = fits.open(fname)
        time = f[2].data['TIME'] + TIME_OFFSET
        l = (time < end_time) & (time >= start_time)
        time = time[l]
        channel = f[2].data['PHA'][l]

        times.append(time)
        channels.append(channel)

    t, c = numpy.concatenate(times), numpy.concatenate(channels)
    t, i = numpy.unique(t, return_index=True)
    c = c[i]
    return t, c

def get_triggers(start_time, end_time, detector_num,
                 energy=(CHANNELS.min(), CHANNELS.max()), fault_tolerant=False):
    times, channels = get_data(start_time, end_time, detector_num, fault_tolerant=fault_tolerant)

    l = numpy.searchsorted(CHANNELS, energy[0]) - 1
    r = numpy.searchsorted(CHANNELS, energy[1])

    keep = (channels >= l) & (channels < r)
    return times[keep]

def get_binned_triggers(start_time, end_time, detector_num, delta_t,
                        energy=(CHANNELS.min(), CHANNELS.max()), fault_tolerant=False):
    times = get_triggers(start_time, end_time, detector_num,
                         energy=energy, fault_tolerant=fault_tolerant)
    bin_edges = numpy.arange(start_time, end_time, delta_t)

    left = numpy.searchsorted(times, bin_edges)
    right = numpy.concatenate([left[1:], [len(times)]])
    bcount = right - left
    return bin_edges, bcount
