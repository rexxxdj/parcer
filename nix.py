# -*- coding: utf-8 -*-
import requests
import csv
from lxml import html

siteurl = 'https://news.ycombinator.com/'

response = requests.get(siteurl)
parsed_body = html.fromstring(response.text)

def jsonWriteLine(title,url,site):
    line = '{"title": "%s",\n "url": "%s",\n "site": "%s",\n }\n' %(title,url,site)
    return line


filename = open('nix.json','w')


for n in parsed_body.xpath('//td[@class="title"][2]'):
    title = ''.join(n.xpath('./a/text()'))
    atag = n.xpath('./a')
    for i in atag:
        url = i.get('href')
    site = ''.join(n.xpath('./span/a/span/text()'))
    
    filename.write(jsonWriteLine(title,url,site))

filename.close()
