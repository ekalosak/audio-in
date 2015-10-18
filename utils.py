import logging
import time
import pdb
import datetime
import numpy
import re

import geopy

def make_logger(name, verbose = True):
    # https://docs.python.org/2/howto/logging-cookbook.html
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('{}.log'.format(name))
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    fmt ='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    if verbose:
        logger.addHandler(ch)
    return logger

def _writetolog(what, log, debuglevel):

    if debuglevel == "debug":
        log.debug("function <{}> returned <{}>".format(
            function, result))
    elif debuglevel == "info":
        log.info("function <{}> returned <{}>".format(
            function, result))
    else:
        raise Exception('Unsupported debugging level <{}>'.format(
            debugging))

def loggable(log, debuglevel="debug"):
    # decorator that logs returned object of function
    def wrap(function):
        def inner(*args):
            result = function(args)
            _writetolog(what, log, debuglevel)
            return result
        return inner
    return wrap

def epoch(datestring):
    # "d/m/y h:m:s" -> int
    #   time since 1/1/1970
    date = datestring.split(' ')[0]
    tim = datestring.split(' ')[1]
    day = date.split('/')[1]
    month = date.split('/')[0]
    year = date.split('/')[2]
    hour = tim.split(':')[0]
    timedata = day, month, year, hour
    timedata = map(lambda x: int(x), timedata)
    day, month, year, hour = timedata
    epo = (datetime.datetime(year,month,day,hour) -
            datetime.datetime(1970,1,1)).total_seconds()
    return epo

def latlon(addr, log):
    geolocator = geopy.geocoders.Nominatim()
    log.debug('searching for <{}> using <{}>'.format(addr, geolocator))
    location = geolocator.geocode(addr)
    log.debug('found <{}>'.format(location))
    return location.latitude, location.longitude

def approx_eq(f0, f1, prec = 4):
    assert type(f0) == float
    assert type(f1) == float
    n0, n1 = map(lambda f: round(f, prec), [f0, f1])
    return n0 == n1

def string_to_type(typestring):
    # "<type 'numpy.int64'>" -> <type 'numpy.int64'>
    tps = re.match('(.*)\'(.*)\'(.*)', qq).groups()[1]
    tp = eval(tps)
