# -*- coding: utf-8 -*-
import requests
import csv
from lxml import html

class ycombinatorParser():
    siteurl = 'https://news.ycombinator.com/'
    response = requests.get(siteurl)
    parsed_body = html.fromstring(response.text)
    rownumber = 1

    def jsonWriteLine(rownumber,title,autor,url,site):
        line = '{"Rownumber:" %d,\n "title": "%s",\n "autor:" "%s",\n "url": "%s",\n "site": "%s",\n }\n' %(rownumber,title,autor,url,site)
        return line

    def getnews(rownews):
        newsdict = {}
        for news in rownews:
            newsdict["title"] = ''.join(news.xpath('./a/text()'))
        for i in news.xpath('./a'):
            newsdict["url"] = i.get('href')
            newsdict["site"] = ''.join(news.xpath('./span/a/span/text()'))
        return newsdict

    def getauthor(rowautor):
        authordict = {}
        for author in rowautor:
            authordict["autor"] = ''.join(author.xpath('./a[1]/text()'))
        return authordict

    filename = open('nix.json','w')

    for row in parsed_body.xpath('//tr'):
        rownews = row.xpath('./td[@class="title"][2]')
        rowautor = row.xpath('./td[@class="subtext"][1]')
        datadict = {}
        if rownews:
            datadict = getnews(rownews)
        if rowautor:
            for author in rowautor:
                datadict = getauthor(rowautor)

        if datadict:
            autor = ''
            try:
                title=datadict["title"]
                url=datadict["url"]
                site=datadict["site"]
            except KeyError:
                autor = datadict["autor"]

            if autor:  
                if 'ycombinator' in url:
                    print (ruwnumber,'PARSE ME!')              
                filename.write(jsonWriteLine(rownumber,title,autor,url,site))                
                rownumber += 1
    filename.close()

if __name__ == 'main':
    ycombinatorParser()        
