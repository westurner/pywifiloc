#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
"""
pywifiloc
=========
Objectives:
 - Request a location from the Google Maps API from a wifi site survey
 - Use only Python builtins (no Requests, or httplib2)

"""
__version__ = "0.0.1"
import json
import logging
import subprocess
import time
import urllib
import urllib2
import webbrowser
from collections import namedtuple, defaultdict
from pprint import pprint, pformat
from shlex import split

NMCLI_CMD=('nmcli','-f','signal,ssid,bssid','dev','wifi','list')
# from:https://code.google.com/apis/console/b/0/
#API_KEY = ''
API_HEADERS = {
        'Content-Type':'application/json; charset=utf8',
        'User-Agent': 'pywifiloc/%s' % __version__ }

AP = namedtuple('AP', ('signal','ssid','bssid'))

def scrape_local_ap_list(samples=3, delay=2):
    """scrape output from ``nmcli dev wifi list``

    :param samples: number of samples to scrape
    :type samples: int
    :param delay: seconds to delay between samples
    :type delay: int

    :return: list of AP(signal, ssid, bssid) namedtuples
    :rtype: list
    """
    ap_ssids = {}
    ap_signals = defaultdict(lambda: 0)
    scalar = float(1) / samples
    for n in range(samples):
        p = subprocess.Popen(NMCLI_CMD, stdout=subprocess.PIPE)
        stdout,stderr = p.communicate()
        aps = sorted(
                (split(l) for l in
                    stdout.replace("""'s""",'===s').split('\n')[1:-1]),
                key=lambda x: int(x[0]),
                reverse=True)
        ap_list = [AP(
                    int(ap[0]),
                    ap[1].replace('===s',"'s"),
                    ap[2]) for ap in aps]
        sigsum = sum(ap.signal for ap in ap_list)
        logging.debug("WIFI SAMPLE %d: %d from %d APs" % (
                                    n, sigsum, len(aps)))
        for ap in ap_list:
            ap_ssids[ap.bssid] = ap.ssid
            ap_signals[ap.bssid] += ap.signal * scalar
        time.sleep(delay)

    signals = sorted(ap_signals.iteritems(), key=lambda x: x[1], reverse=True)
    return [AP(int(s[1]), ap_ssids[s[0]], s[0]) for s in signals]


BROWSERLOC_API_URL = "https://maps.googleapis.com/maps/api/browserlocation/json"
def build_browserlocation_url(aps):
    """build browserlocation api query url

    :param aps: iterable of AP namedtuples
    :type aps: iterable

    :return: URL string
    :rtype: string
    """
    querystr = '&'.join((
        'wifi=mac:%s%%7Cssid:%s%%7Css:%s' % (
            ap.bssid, urllib.quote(ap.ssid), ap.signal) for ap in aps))

    url = '%s?browser=firefox&sensor=true&%s' % (BROWSERLOC_API_URL, querystr)
    # HTTP 414 when > 2000 chars
    return url[0:(2000-url[::-1].find('&', len(url)-2000))]


def build_maps_api_data(aps):
    """TODO: does the Google Maps API support POST params?"""
    raise NotImplementedError()
    def _get_data():
        yield ('browser','firefox')
        yield ('sensor','true')
        for ap in aps:
            yield ('wifi', 'mac:%s%%7Cssid:%s%%7Css:%s' % (
                ap.bssid, urllib.quote(ap.ssid), ap.signal))


def request_json(url, data=None, headers=None):
    """wrapper for urllib2 Request and urlopen, in lieu of Requests

    :param url: URL to Request
    :type url: str
    :param data: data to include with Request
    :type data:
    :param headers: headers to include with Request
    :type headers: dict

    :return: dict response object
    :rtype: dict
    """
    req = urllib2.Request(url, data, headers=headers or API_HEADERS)
    logging.debug("HTTP  GET: %r %r %r" % (url, data, headers))
    try:
        fobj = urllib2.urlopen(req)
        response = fobj.read()
        logging.debug("HTTP RESP: %r" % dict(fobj.headers))
        resp_obj = json.loads(response)
    except urllib2.HTTPError, e:
        logging.error(str(e))
        raise

    logging.debug("HTTP JSON: %s" % pformat(resp_obj))

    resp_status = resp_obj.get('status')
    if resp_status != 'OK':
        logging.error("%r %r %r", url, data, headers)
        raise Exception('Response status is not OK')

    return resp_obj


def get_maps_url(lat, lng):
    return 'https://maps.google.com/maps?q=%s,+%s' % (lat,lng)


def request_browser_location(aps):
    """request browser location from Maps API

    :param aps: iterable of AP namedtuples
    :type aps: iterable

    :return: accuracy, lat, lng
    :rtype: tuple
    """
    api_queryurl = build_browserlocation_url(aps)
    resp_obj = request_json(api_queryurl)

    accuracy = resp_obj['accuracy']
    lat,lng = resp_obj['location']['lat'], resp_obj['location']['lng']
    return accuracy, lat, lng


GEOCODE_API_URL='https://maps.googleapis.com/maps/api/geocode/json'
def request_reverse_geocode(lat, lng):
    """request reverse geocode from Maps API

    :param lat: latitude
    :type lat: str
    :param lng: longitude
    :type lng: str

    :return: parsed JSON response object
    :rtype: dict
    """
    api_queryurl = "%s?latlng=%s,%s&sensor=false" % (
                    GEOCODE_API_URL, lat, lng)
    resp_obj = request_json(api_queryurl)
    return resp_obj


TIMEZONE_API_URL='https://maps.googleapis.com/maps/api/timezone/json'
def request_timezone(location):
    """request timezone from Maps API

    :param location: location string (eg. "lat,lng")
    :type location: str

    :return: timeZoneId, timeZoneName
    :rtype: tuple of str
    """
    api_queryurl = '%s?location=%s&timestamp=%s&sensor=false' % (
        TIMEZONE_API_URL, location, time.time())
    resp_obj = request_json(api_queryurl)

    return resp_obj['timeZoneId'], resp_obj['timeZoneName']


import unittest
class Test_pywifiloc(unittest.TestCase):
    def test_scrape_local_ap_list(self):
        aps = scrape_local_ap_list()
        logging.debug(pprint(aps))


def main():
    import optparse
    import logging

    prs = optparse.OptionParser(usage="./%prog : args")

    prs.add_option('-v', '--verbose',
                    dest='verbose',
                    action='store_true',)
    prs.add_option('-q', '--quiet',
                    dest='quiet',
                    action='store_true',)
    prs.add_option('-t', '--test',
                    dest='run_tests',
                    action='store_true',)

    prs.add_option('-l', '--location',
                    dest='location',
                    action='store',
                    nargs=2)

    prs.add_option('-s', '--samples',
                    dest='sample_count',
                    action='store',
                    default=3)
    prs.add_option('-d', '--delay',
                    dest='sample_delay',
                    action='store',
                    default=2)

    prs.add_option('-L', '--ap-limit',
                    dest='ap_limit',
                    default=None,
                    action='store')
    prs.add_option('-b', '--browseto',
                    dest='browseto',
                    action='store_true')

    prs.add_option('-r', '--reverse',
                    dest='reverse_geocode',
                    action='store_true')

    prs.add_option('-z', '--timezone',
                    dest='timezone',
                    action='store_true')

    (opts, args) = prs.parse_args()

    if not opts.quiet:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

    if opts.run_tests:
        import sys
        sys.argv = [sys.argv[0]] + args
        import unittest
        exit(unittest.main())

    acc, lat, lng = None, None, None
    if opts.location:
        lat, lng = opts.location
    else:
        aps = scrape_local_ap_list()[0:opts.ap_limit]
        acc,lat,lng = request_browser_location(aps)
        print("accuracy: %s" % acc)
    print("lat/lng: %s, %s" % (lat, lng))

    maps_url = get_maps_url(lat,lng)
    print("map url: %s" % maps_url)
    if opts.browseto:
        webbrowser.open_new_tab(maps_url)

    if opts.reverse_geocode:
        resp_obj = request_reverse_geocode(lat, lng)
        for result in resp_obj.get('results',[]):
            print("address: %s" % result.get('formatted_address'))

    if opts.timezone:
        tz = request_timezone('%s,%s' % (lat, lng))
        print("timezone: %s -- %s" % (tz[0], tz[1]))

if __name__ == "__main__":
    main()
