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
