import functools

from lib.datasets import load_dataset
from lib.pickled import Pickled


def main():
    year = 2012
    get_dataset = functools.partial(load_dataset, year)

    pickle_fn = '../dat/pkl/workspace_%d' % year
    transtats, departs, arrives = Pickled.load_or_compute(pickle_fn, get_dataset)

    return departs, arrives

departs, arrives = main()
print departs.corr(min_periods=12, method='kendall')
print arrives.corr(min_periods=12, method='kendall')
