#!/usr/bin/python
from bs4 import BeautifulSoup, Comment, NavigableString
import HTMLParser
import re
import sys
import yaml

htmlParser = HTMLParser.HTMLParser()

ljMigrateXml = sys.stdin.read()
soup = BeautifulSoup(ljMigrateXml)

event = soup.event
eventTime = event.eventtime.string
subject = event.subject.string
url = event.url.string

bodyHtml = htmlParser.unescape(event.event.string)

ljCutRe = r'<lj-cut [^>]+>'
bodyHtml = re.sub(ljCutRe, '<!-- more -->\n', bodyHtml, 1)
bodyHtml = re.sub(ljCutRe, '', bodyHtml)

print "---"
print yaml.dump({
  'layout': 'post',
  'title': str(subject),
  'date': str(eventTime),
  'published': 'true',
  'categories': 'from-livejournal',
  'dummy': []  # this is necessary for the yaml module to work :(
})
print "---"
print bodyHtml
print "<hr/>"
print "originally from: " + url

