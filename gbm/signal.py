""" Utilities for processing GBM time series data
"""

def running_norm(times, counts, window):
    nbins = int(window / (times[1] - times[0]))
    csum = counts.cumsum()
    ave = (csum[nbins*2:] - csum[:-nbins*2]) / (nbins * 2.0)

    meansub =  counts[nbins:-nbins] - ave
    normed = meansub / meansub.std()
    return times[nbins:-nbins], normed
