#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import os
from scraper import SimpleScraper

BASE_URL = 'http://www.presspass.me/journalist'


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {0!s} <input file>".format((__file__)))
        sys.exit()

    if not os.path.exists('./presspass'):
        os.mkdir('./presspass')

    f = open(sys.argv[1])
    reader = csv.DictReader(f)
    scraper = SimpleScraper()
    i = 0
    count = 0
    for r in reader:
        count += 1
        name = r['twitter.username']
        print(count, "==>", name)
        html = scraper.get(BASE_URL + '/{0!s}'.format(name))
        if html:
            with open('presspass/{0!s}.html'.format(name), "wb") as f:
                f.write(str.encode(html))
            i += 1
    print("Found: {0:d}".format(i))
    f.close()
