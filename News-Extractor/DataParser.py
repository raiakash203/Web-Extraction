import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import datefinder
import fnmatch
import os
from urllib.parse import urljoin
from utilityfunction import *


class Parser:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except Exception as e:
            print(e)
            return None
        return BeautifulSoup(req.text, 'lxml'),req.content

    def safeGet(self, pageObj, selector):
        """
        function to get a content string from a
​    ​    Beautiful Soup object and a selector. Returns an empty
​    ​    string if no object is found for the given selector
        """
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def statusCheck(self,outputPath):
        html = os.path.join(outputPath,'HTML')
        output = os.path.join(outputPath,'Text')
        if not os.path.exists(html):
            os.makedirs(html)
            htmllen = 1
        else:
            htmllen = len(fnmatch.filter(os.listdir(html), '*.html')) + 1
        if not os.path.exists(output):
            os.makedirs(output)
            outputlen = 1
        else:
            outputlen = len(fnmatch.filter(os.listdir(output), '*.txt')) + 1
        htmlLocation = os.path.join(html, str(htmllen)+'.html')
        outputLocation = os.path.join(output, str(outputlen)+'.txt')
        return htmlLocation,outputLocation

    def htmlStore(self, content, htmlFile):
        with open(htmlFile,'wb') as f:
            f.write(content)

    def articleStore(self, url, title, body, date, outputFile):
        with open(outputFile, 'wb') as f:
            f.write(('URL: '+url+'\n'+'Date: '+date+'\n'+'Title: '+title+'\n'+'Article: '+body).encode('utf-8'))

    def dataparse(self, site, url, outputPath, bs, content):
        """
        Extract content from a given page URL
        """
        #bs,content = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            try:
                for item in site.dateTag:
                    date = self.safeGet(bs,item)
                    if date:
                        break
                matches = datefinder.find_dates(date)
                *_, last = matches
                date = last.strftime("%d-%m-%Y %H:%M:%S")
            except:
                date = 'None'
            #date = ''.join([match.strftime("%d-%m-%Y %H:%M:%S") for match in matches])
        if title != '' and body != '':
            htmlFile,outputFile = self.statusCheck(outputPath)
            self.htmlStore(content, htmlFile)
            self.articleStore(url, title, body, date, outputFile)
            #df.loc[len(df)] = [url, title, body, date, keyword]
            #print(url)
            outputPath1 = "/home/NSCS/src/"
            htmlFile = htmlFile.split('/',11)[-1]
            outputFile = outputFile.split('/',11)[-1]
            outputFile = os.path.join(outputPath1,outputFile)
            htmlFile = os.path.join(outputPath1,htmlFile)
            return [url, title, body, date, htmlFile, outputFile,site.name]
        else:
            return None
            #return [url, None, None, None, None]
