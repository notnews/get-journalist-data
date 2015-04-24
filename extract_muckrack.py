#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
from bs4 import BeautifulSoup
import re
from urllib.parse import urlsplit

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <input file>" % (__file__))
        sys.exit()

    f = open(sys.argv[1])
    o = open("muckrack-out.csv", "wt", encoding='utf-8', newline='')
    reader = csv.DictReader(f)
    header = reader.fieldnames
    header += ['muckrack.url', 'muckrack.name', 'muckrack.title',
               'muckrack.topics', 'muckrack.location', 'muckrack.website',
               'muckrack.about', 'muckrack.covers', 'muckrack.followers',
               'muckrack.tweets']
    header += ['muckrack.facebook', 'muckrack.klout', 'muckrack.google',
               'muckrack.linkedin', 'muckrack.foursquare', 'muckrack.youtube',
               'muckrack.flickr', 'muckrack.tumblr', 'muckrack.twitter']
    header += ['muckrack.linkedtwitteracct1', 'muckrack.linkedtwitteracct2',
               'muckrack.linkedtwitteracct3']
    writer = csv.DictWriter(o, fieldnames=header, dialect='excel')
    writer.writeheader()

    for r in reader:
        name = r['twitter.username']
        print(name)
        try:
            with open('muckrack/%s.html' % name, encoding='utf-8') as m:
                html = m.read()
        except:
            html = ""
        if html != "":
            r['muckrack.url'] = 'http://muckrack.com/%s' % name
        soup = BeautifulSoup(html)
        person = soup.find('div', {'class': 'person-header-inner'})
        if person:
            n = person.find('h1')
            r['muckrack.name'] = n.text.strip()
            title = person.find('div', id='title')
            r['muckrack.title'] = title.text.strip()
            links = person.find('ul', {'class': "header-links"})
            if links:
                loc = []
                for l in links.find_all('li'):
                    loc.append(l)
                try:
                    r['muckrack.topics'] = loc[0].text.strip()
                    if loc[1].text.find('Website') == -1:
                        r['muckrack.location'] = loc[1].text.strip()
                        r['muckrack.website'] = loc[2].find('a')['href']
                    else:
                        r['muckrack.website'] = loc[1].find('a')['href']
                except:
                    pass
        socials = soup.find('div', {'class': 'social-links'})
        if socials:
            for l in socials.find_all('a'):
                href = l['href']
                url = urlsplit(href)
                colname = 'muckrack.%s' % url.netloc.split('.')[-2]
                if colname in header:
                    r[colname] = href
                else:
                    print("ERROR: %s" % url.netloc)
        about = soup.find('div', {'class': 'summary-block-contents'})
        if about:
            r['muckrack.about'] = about.text.strip()
            for a in about.find_all('a'):
                href = a['href']
                i = 0
                if a.text.startswith('@') and href.find('twitter') != -1:
                    i += 1
                    if i < 3:
                        r['muckrack.linkedtwitteracct%d' % i] = href
                    else:
                        break
        topics = soup.find_all('div', {'class': 'summary-block topics'})
        labels = []
        for t in topics:
            for l in t.find_all('span', {'class': 'label label-topic-inverse'}):
                labels.append(l.text.strip())
        r['muckrack.covers'] = '|'.join(labels)

        stats = soup.find('div', {'class': 'person-stats'})
        if stats:
            for s in stats.find_all('div', {'class': 'person-stat'}):
                a = s.text.strip()
                m = re.match(r'([\d,]+)\s+(.*)', a)
                if m:
                    r['muckrack.%s' % m.group(2)] = m.group(1)
        writer.writerow(r)

    f.close()
    o.close()
