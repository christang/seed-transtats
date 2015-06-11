import functools
from datetime import timedelta
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


def join_weather(dataset, precips):
    dataset['Weather0'] = np.zeros(len(dataset))
    dataset['Weather1'] = np.zeros(len(dataset))

    levels = dataset.index.levels
    labels = zip(*dataset.index.labels)
    for i, j in labels:
        date = levels[0][i]
        iata = levels[1][j]
        yest = (to_datetime(date, format="%Y-%m-%d") - timedelta(1)).strftime("%Y-%m-%d")
        try:
            weather = precips.get_group(iata)[date]
            dataset['Weather0'][date][iata] = weather
        except KeyError:
            dataset['Weather0'][date][iata] = float('nan')

        try:
            weather = precips.get_group(iata)[yest]
            dataset['Weather1'][date][iata] = weather
        except KeyError:
            dataset['Weather1'][date][iata] = float('nan')


def load_dataset(year):
    transtats = load_transtats(year)

    dep_per_date_airport = transtats.groupby(['FlightDate','Origin'])[
        "DepDelay","DepDel15","TaxiOut","TaxiIn","ArrDelay","ArrDel15","Cancelled","Diverted",
        "CarrierDelay","WeatherDelay","NASDelay","SecurityDelay","LateAircraftDelay",
    ].mean()
    arr_per_date_airport = transtats.groupby(['FlightDate','Dest'])[
        "DepDelay","DepDel15","TaxiOut","TaxiIn","ArrDelay","ArrDel15","Cancelled","Diverted",
        "CarrierDelay","WeatherDelay","NASDelay","SecurityDelay","LateAircraftDelay",
    ].mean()

    precips = load_precips(year).groupby(['iata'])

    # The following can probably be accomplished more efficiently by reshaping the
    # precipitation data and table joining with the above data sets

    join_weather(dep_per_date_airport, precips)
    join_weather(arr_per_date_airport, precips)

    return transtats, dep_per_date_airport, arr_per_date_airport


def main():
    year = 2012
    get_dataset = functools.partial(load_dataset, year)

    pickle_fn = '../dat/pkl/workspace_%d' % year
    transtats, departs, arrives = pickled.Pickled.load_or_compute(pickle_fn, get_dataset)

    return departs, arrives

departs, arrives = main()
print departs.corr(min_periods=12, method='kendall')
print arrives.corr(min_periods=12, method='kendall')
