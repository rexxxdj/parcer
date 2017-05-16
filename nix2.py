# -*- coding: utf-8 -*-
import requests
import csv
from lxml import html

class ycombinatorParser():
    siteurl = 'https://news.ycombinator.com/'    

    def getNextPage(pageurl):
        response = requests.get(pageurl)
        parsed_body = html.fromstring(response.text)
        nextpage=parsed_body.xpath('//a[@class="morelink"]')
        try:
            nexthref=nextpage[0].get('href')
        except IndexError:
            nexthref = ''
        return nexthref  


    def parsePage(parsed_body,outputfile,rownumber):

        def jsonWriteLine(rownumber,title,autor,url,site):
            line = '{"Rownumber:" %d,\n "title": "%s",\n "autor:" "%s",\n "url": "%s",\n "site": "%s",\n }\n' %(rownumber,title,autor,url,site)
            return line

        def getNews(rownews):
            newsdict = {}
            for news in rownews:
                newsdict["title"] = ''.join(news.xpath('./a/text()'))
            for i in news.xpath('./a'):
                newsdict["url"] = i.get('href')
                newsdict["site"] = ''.join(news.xpath('./span/a/span/text()'))
            return newsdict

        def getAuthor(rowautor):
            authordict = {}
            for author in rowautor:
                authordict["autor"] = ''.join(author.xpath('./a[1]/text()'))
            return authordict

        for row in parsed_body.xpath('//tr'):
            rownews = row.xpath('./td[@class="title"][2]')
            rowautor = row.xpath('./td[@class="subtext"][1]')
            datadict = {}
            if rownews:
                datadict = getNews(rownews)
            if rowautor:
                for author in rowautor:
                    datadict = getAuthor(rowautor)

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
                    outputfile.write(jsonWriteLine(rownumber,title,autor,url,site))                
                    rownumber += 1
        return rownumber




    filename = open('nix.json','w')
    pageflag = True
    rownumber = 1
    pageparse = siteurl
    while pageflag:        
        print ("Parsing: ", pageparse)
        response = requests.get(pageparse)
        parsed_body = html.fromstring(response.text)    
        

        rownumber = parsePage(parsed_body,filename,rownumber)-1


        pageparse = siteurl+getNextPage(pageparse)

        if pageparse == siteurl:
            pageflag = False


    filename.close()




if __name__ == 'main':
    ycombinatorParser()        
