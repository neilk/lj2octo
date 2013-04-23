#!/usr/bin/python
from bs4 import BeautifulSoup, Comment, NavigableString
import HTMLParser
import sys

htmlParser = HTMLParser.HTMLParser()

ljMigrateXml = sys.stdin.read()
soup = BeautifulSoup(ljMigrateXml)

event = soup.event
eventTime = event.eventtime.string
subject = event.subject.string
url = event.url.string

bodyHtml = htmlParser.unescape(event.event.string)

bodySoup = BeautifulSoup(bodyHtml)

lj_cut = bodySoup.find_all('lj-cut')
if len(lj_cut):
    dummyMore = soup.new_tag('more')
    lj_cut[0].insert_before(dummyMore)
    for cut in lj_cut:
        cut.unwrap()
bodySoup.more.replace_with(Comment(" more "))

doc = soup.new_tag('document');
print "\n\n\n\n"
for el in bodySoup.body.contents:
    print "element!"
    if isinstance(el, NavigableString) and not isinstance(el, Comment):
        print "elll"
        print el
        lines = el.string.split(r'\r\n')
        for line in lines:
            print "line!" + line
            para = soup.new_tag('p')
            para.string = line
            doc.append(para)
    else:
        doc.append(el)

print eventTime
print subject
print doc.contents
print url

