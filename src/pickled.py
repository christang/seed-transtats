import cPickle
import os
import time


class RateLimitException(Exception):

    pass


class Pickled(object):

    delay = 5

    def __init__(self, cwd='dat/pkl'):
        self.cwd = cwd

    @staticmethod
    def load_or_compute(pickle_fn, compute, retry=1, retry_none=True):
        result = cPickle.load(open(pickle_fn)) if os.path.isfile(pickle_fn) else None

        if result is None and retry_none:
            result = Pickled.try_compute(compute, retry)
            cPickle.dump(result, open(pickle_fn, 'wb'), cPickle.HIGHEST_PROTOCOL)

        return result

    @staticmethod
    def try_compute(compute, retry):
        while retry > 0:
            try:
                return compute()
            except RateLimitException:
                time.sleep(Pickled.delay)
                retry -= 1
        return None
