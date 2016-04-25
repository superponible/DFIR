#!/usr/bin/env python
#
# safebro_lookup.py
# Dave Lassalle (@superponible)
#
# This script can either crawl a website from a starting URL or accept a file
# containing one URL per line, and submit the crawled or provided URLs
# to Google's Safe Browsing Lookup API and provide the results.
#
# A Google API key is needed from:
#   https://console.developers.google.com/project
# A guide on the API is available at:
#   https://developers.google.com/safe-browsing/lookup_guide
#
# basic crawler modified from https://pypi.python.org/creepy
#

from creepy import Crawler
import urllib
import urllib2
import sys
import argparse

API_KEY = ''

def print_result(result, url):
    print '-{}- {}'.format(result, url)

def sb_lookup(url):
    global API_KEY
    url = urllib.quote_plus(url)
    result = ""
    try:
        result = urllib2.urlopen('https://sb-ssl.google.com/safebrowsing/api/lookup?client=safe-browsing&key=' + API_KEY + '&appver=1.0&pver=3.1&url=' + url)
    except urllib2.HTTPError, e:
        if e.code == 400:
            print e
            print "Bad Request - The HTTP request was not correctly formed."
        elif e.code == 401 or e.code == 403:
            print e
            print "Not Authorized - The API key is not authorized."
        elif e.code == 503:
            print e
            print 'Service Unavailable - The server cannot handle the request. Besides the normal server failures, this could also indicate that the client has been "throttled" for sending too many requests.'
        else:
            print "Unknown error: ", e
        exit(1)
    status = result.getcode()
    if status == 200:
        result = result.read()
    if status == 204:
        result = "none"
    return result

class MyCrawler(Crawler):
    def process_document(self, doc):
        result = sb_lookup(doc.url)
        print_result(result, doc.url)

def cliargs():
    '''Parse CLI args'''
    global API_KEY
    parser = argparse.ArgumentParser(description="safebro_lookup.py -- Google Safe Browsing Lookup tool")
    parser.add_argument('-u', '--url', required=False, action='store', dest='start_url', help='Base URL for crawler (will add http:// if not given)')
    parser.add_argument('-f', '--file', required=False, action='store', dest='infile', help='File containing URLs to lookup')
    parser.add_argument('-a', '--api_key', required=False, action='store', dest='api_key', help='Specify/override API_KEY hardcoded in the script')
    args = parser.parse_args()
    if not (args.start_url or args.infile):
        parser.error('Specify at either a base URL, a file of URLs, or both')
    if args.api_key:
        API_KEY = args.api_key
    elif not API_KEY:
        parser.error('Google API Key must be specified in the script or provided with -a')
    return args

def main(argv):
    args = cliargs()
    if args.infile:
        f = open(args.infile, 'r')
        lines = f.readlines()
        for line in lines:
            url = line.strip('\n')
            result = sb_lookup(url)
            print_result(result, url)
    if args.start_url:
        if not (args.start_url.startswith('http://') or args.start_url.startswith('https://')):
            args.start_url = 'http://' + args.start_url
        crawler = MyCrawler()
        crawler.set_follow_mode(Crawler.F_SAME_HOST)
        crawler.add_url_filter('\.(jpg|jpeg|gif|png|js|css|swf)$')
        crawler.crawl(args.start_url)

if __name__ == '__main__':
    main(sys.argv[1:])
