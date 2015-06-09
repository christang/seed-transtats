from datetime import timedelta, date
import csv
import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import tarfile

import basemap
import converter


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
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


def main():
    airports_fn = '../dat/seed/airports.csv'
    airports = get_airports(airports_fn)

    lats, lons = converter.get_lat_lon()

    start_date = date(2011, 1, 1)
    end_date = date(2012, 12, 31)

    for current in daterange(start_date, end_date):
        dataset = get_dataset(current)

        precip = dataset.variables['amountofprecip'][:]
        precip_in = np.ma.masked_less(precip / 2540., 0.01)

        basemap.plot_conus_precip(lats, lons, precip_in)
        plt.show()

        break

main()
