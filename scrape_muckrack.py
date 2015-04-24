#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import os
from scraper import SimpleScraper

BASE_URL = 'http://muckrack.com'


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <input file>" % (__file__))
        sys.exit()
    if not os.path.exists('./muckrack'):
        os.mkdir('./muckrack')
    f = open(sys.argv[1])
    reader = csv.DictReader(f)
    scraper = SimpleScraper()
    i = 0
    count = 0
    for r in reader:
        count += 1
        name = r['twitter.username']
        print(count, "==>", name)
        html = scraper.get(BASE_URL + '/%s' % name)
        if html:
            with open('muckrack/%s.html' % name, "wb") as f:
                f.write(str.encode(html))
            i += 1
    print("Found: %d" % i)
    f.close()
