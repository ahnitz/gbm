""" Utilities for processing GBM time series data
"""
import numpy

def running_norm(times, counts, window):
    t = times.copy()
    t.sort()

    l = times - window
    r = times + window

    csum = counts.cumsum()
    ave = (csum[nbins*2:] - csum[:-nbins*2]) / (nbins * 2.0)

    meansub =  counts[nbins:-nbins] - ave
    normed = meansub / meansub.std()
    return times[nbins:-nbins], normed

def cluster_detectors(counts, num_detectors=4):
    counts = numpy.array(counts)
    counts = numpy.sort(counts, axis=0)

    st = counts[-num_detectors:,:]
    return numpy.sum(st, axis=0)

def trigger_integrate(times, counts, threshold, window):
    peaks = numpy.where(counts > threshold)[0]
    wbins = int(window / (times[1] - times[0]))
    stats = []
    for p in peaks:
        l = p-wbins if p-wbins >=0 else 0
        r = p+wbins if p+wbins <=len(counts) else len(counts)
        s = counts[l:r]
        stat = s.sum()
        stats.append(stat)
    return times[peaks], numpy.array(stats)

def running_window(times, window):
    t = times.copy()
    t.sort()
    l = t - window
    r = t + window
    sl = numpy.searchsorted(t, l)
    sr = numpy.searchsorted(t, r)
    bins = sr - sl
    return t, bins

def running_norm(times, values, window, blind):
    times = times.copy()
    s = times.argsort()
    times = times[s]
    values = values[s]

    sl = numpy.searchsorted(times, times-window)
    sr = numpy.searchsorted(times, times+window) - 1

    bsl = numpy.searchsorted(times, times-blind)
    bsr = numpy.searchsorted(times, times+blind) - 1

    csum = values.cumsum()
    csum2 = (values**2.0).cumsum()

    dx = (sr - sl).astype(numpy.float64)
    dx -= (bsr - bsl).astype(numpy.float64)

    mean = (csum[sr] - csum[sl] - (csum[bsr]- csum[bsl])) / dx
    meansq = (csum2[sr] - csum2[sl] - (csum2[bsr] - csum2[bsl])) / dx

    std = (meansq - mean**2.0)**0.5
    values = (values - mean) / std
    return times, values

