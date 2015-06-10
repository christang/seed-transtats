from __future__ import print_function
from datetime import timedelta, date
import collections
import csv
import functools
import matplotlib.pyplot as plt
import netCDF4
import os
import numpy as np
import sys
import tarfile

import basemap
import converter
import pickled


Airport = collections.namedtuple('Airport', 'id iata lat lng i j data')


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)


def get_airports(fn):
    with open(fn) as csv_file:
        reader = csv.DictReader(csv_file)
        airports = [airport for airport in reader]
    return airports


def get_dataset(current, base='../dat/ahps/', temp='tmp/'):
    nws_zip_fn = base
    nws_zip_fn += current.strftime('%Y')
    nws_zip_fn += '/nws_precip_'
    nws_zip_fn += current.strftime('%Y%m%d')
    nws_zip_fn += '_nc.tar.gz'

    tar = tarfile.open(nws_zip_fn)
    tar.extractall(temp)

    nws_conus_fn = 'nws_precip_conus_%s.nc' % current.strftime('%Y%m%d')
    return netCDF4.Dataset(temp + nws_conus_fn)


def compute_closest_grid_point(lats, lons, lat, lon):
    d_lats = lats - float(lat)
    d_lons = lons - float(lon)
    d = np.multiply(d_lats, d_lats) + np.multiply(d_lons, d_lons)
    i, j = np.unravel_index(d.argmin(), d.shape)
    return i, j, np.sqrt(d.min())


def compute_closest_grid_points(lats, lons, airports):
    closest_grid_point = functools.partial(compute_closest_grid_point, lats, lons)

    airport_grid_points = [
        closest_grid_point(airport['lat'], airport['long'])
        for airport in airports]
    return airport_grid_points


def main():
    airports_fn = '../dat/seed/airports.csv'
    airports = get_airports(airports_fn)

    # Map airports to grids within National Weather Service netCDF4 files
    # or retrieve them from pickle files if previously computed

    pickle_fn = '../dat/pkl/lat_lon'
    lats, lons = pickled.Pickled.load_or_compute(pickle_fn, converter.get_lat_lon)

    closest_grid_points = functools.partial(compute_closest_grid_points, lats, lons, airports)

    pickle_fn = '../dat/pkl/grid_points'
    airport_grid_points = pickled.Pickled.load_or_compute(pickle_fn, closest_grid_points)

    # n.b.: Contains grid points not within CONUS that should be ignored
    # e.g.: states := set(['PR', 'GU', 'NA', 'AK', 'AS', 'HI', 'VI', 'CQ'])

    # assert:
    #   agp = filter(lambda x: x[1][2]>5, enumerate(airport_grid_points))
    #   291 = len([airports[a[0]]['state'] for a in agp])

    start_date = date(2011, 1, 1)
    end_date = date(2011, 12, 31)

    days = (end_date - start_date).days + 1

    conus_airports = [
        Airport(
            i,
            airports[i]['iata'],
            float(airports[i]['lat']),
            float(airports[i]['long']),
            airport_grid_points[i][0],
            airport_grid_points[i][1],
            np.zeros(days)
        )
        for i in xrange(len(airports))
        if airport_grid_points[i][2] < 5
    ]

    for i, current in enumerate(daterange(start_date, end_date)):
        print(current.strftime('%Y%m%d'), file=sys.stderr)

        dataset = get_dataset(current)
        precip = dataset.variables['amountofprecip'][:]

        # Write image files from netCDF4 precipitation data

        image_fn = '../dat/precip/img/%s.png' % current.strftime('%Y%m%d')
        if not os.path.exists(image_fn):
            precip_in = np.ma.masked_less(precip / 2540., 0.01)
            basemap.plot_conus_precip(lats, lons, precip_in)
            plt.savefig(image_fn, dpi=150)
            plt.clf()

        # Collect precipitation in inches for airport locations

        for airport in conus_airports:
            airport.data[i] = precip[airport.i, airport.j] / 2540.

    for airport in conus_airports:
        airport_data = np.array_str(airport.data, max_line_width=100000, precision=2, suppress_small=True)
        print('"%s","%s"' % (airport.iata, airport_data))

main()
