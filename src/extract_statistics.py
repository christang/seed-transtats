import functools
from pandas import *

import pickled


def load_transtats(year):
    csv_fns = (
        '../dat/transtats/%d/On_Time_On_Time_Performance_%d_%d.csv' % (year, year, i + 1)
        for i in xrange(12)
    )

    usecols = (
        "DayOfWeek","FlightDate","UniqueCarrier",
        "Origin","Dest",
        "DepTime","DepDelay","DepDel15","TaxiOut",
        "TaxiIn","ArrTime","ArrDelay","ArrDel15",
        "Cancelled","CancellationCode","Diverted",
        "CRSElapsedTime","ActualElapsedTime","AirTime","Flights","Distance",
        "CarrierDelay","WeatherDelay","NASDelay","SecurityDelay","LateAircraftDelay",
    )

    return concat(read_csv(csv_fn, na_values='', usecols=usecols) for csv_fn in csv_fns)


def load_precips(year):
    csv_fn = '../dat/seed/airports_precip_%d.csv' % (year, )

    return read_csv(csv_fn)


def load_dataset(year):
    return load_transtats(year), load_precips(year)


def main():
    year = 2012
    get_dataset = functools.partial(load_dataset, year)

    pickle_fn = '../dat/pkl/workspace_%d' % year
    pickled.Pickled.load_or_compute(pickle_fn, get_dataset)

main()
