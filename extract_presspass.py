#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
from bs4 import BeautifulSoup


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <input file>" % (__file__))
        sys.exit()

    f = open(sys.argv[1])
    o = open("presspass-out.csv", "wt", encoding='utf-8', newline='')
    reader = csv.DictReader(f)
    header = reader.fieldnames
    header += ['presspass.url', 'presspass.name', 'presspass.description',
               'presspass.beats', 'presspass.organizations',
               'presspass.followers', 'presspass.tweets']
    writer = csv.DictWriter(o, fieldnames=header, dialect='excel')
    writer.writeheader()

    for r in reader:
        name = r['twitter.username']
        print(name)
        try:
            with open('html/%s.html' % name, encoding='utf-8') as m:
                html = m.read()
        except:
            html = ""
        if html.find(">> This user does not exist :)") == -1:
            r['presspass.url'] = 'http://www.presspass.me/journalist/%s' % name
            soup = BeautifulSoup(html)
            top = soup.find('div', {'class': 'top'})
            if top:
                n = top.find('div', {'class': 'name'})
                if n:
                    r['presspass.name'] = n.text.strip()
                desc = soup.find('div', {'class': 'description'})
                if desc:
                    if desc.text.find("With Press Pass people with newsworthy") == -1:
                        r['presspass.description'] = desc.text.strip()
            section = soup.find('div', {'class': 'section'})
            if section:
                for li in section.find_all('li'):
                    res = li.text.replace(li['class'][0].capitalize(), '').strip()
                    if res != "None":
                        r['presspass.%s' % li['class'][0]] = res
        writer.writerow(r)

    f.close()
    o.close()
