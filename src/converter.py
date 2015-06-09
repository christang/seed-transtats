# See references for a nice extraction of the necessary logic from nctoasc
#
# References:
#
# http://jjhelmus.github.io/blog/2013/09/17/plotting-nsw-precipitation-data/


import numpy as np

HRAP_XOR = 14
HRAP_YOR = 10


def lat_lon_from_hrap(hrap_x, hrap_y):

    raddeg = 57.29577951
    earthrad = 6371.2
    stdlon = 105.
    mesh_len = 4.7625

    tlat = 60. / raddeg

    x = hrap_x - 401.
    y = hrap_y - 1601.
    rr = x * x + y * y
    gi = ((earthrad * (1 + np.sin(tlat))) / mesh_len)
    gi *= gi
    ll_y = np.arcsin((gi - rr) / (gi + rr)) * raddeg
    ang = np.arctan2(y, x) * raddeg
    ll_x = (270 + stdlon - ang) % 360
    return ll_x, ll_y


def get_lat_lon():

    lats = np.empty((813, 1051), dtype='float')
    lons = np.empty((813, 1051), dtype='float')

    for i in xrange(813):
        for j in xrange(1051):
            hrap_x = j + HRAP_XOR + 0.5
            hrap_y = i + HRAP_YOR + 0.5
            lon, lat = lat_lon_from_hrap(hrap_x, hrap_y)
            lats[i,j] = lat
            lons[i,j] = -lon

    return lats, lons