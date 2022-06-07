#python crawler.py --website TOI --output Output --d 1
"""
--website is the name of the website from configuretemp file
--output path of the output location
--d depth of the scraping
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import datetime
import pandas as pd
from DataParser import Parser
import os
import argparse

class Website:
    """
    Contains information about website structure
    """

    def __init__(self, name, url, titleTag, bodyTag,dateTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.dateTag = dateTag

class tempcrawlers:

    def __init__(self, frontierlinks=[], visited=[]):
        print('inside')
        self.frontierlinks = frontierlinks
        self.visited = visited
        df = pd.DataFrame(columns=['Url','HeadLine','Content','Date','HTMLPath','TxtPath','WebsiteName'])
        self.datadf = df

    def requestfunction(self, link):
        """
        Function to make request to the website
        returns soup object and html content
        """
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.text, 'lxml')
            content = r.content
        except Exception as e:
            print('Request function Error: ',str(e))
            soup = None
            content = None
        finally:
            return soup, content

    def linkextractor(self, pageobj, baseurl,checklist):
        """
        Extract all the url from the pageobj filterin outside
        and already visited urls        
        """
        try:
            extractedlinks = set()
            links = pageobj.find_all('a',href=True)
            for link in links:
                link = link['href']
                link = link.strip()
                if not link.startswith('http'):
                    link = urljoin(baseurl, link)
                if link not in self.frontierlinks and link.startswith(baseurl) and link not in self.visited and link not in checklist:
                    extractedlinks.add(link)
        except Exception as e:
            print('Error in link extractor: ', str(e))
        finally:
            return extractedlinks

    def parse(self, baseurl, urls, checklist, site, outputPath):
        """
        parse the content of the page to get headline, article and date
        """
        try:
            returnextractlinks = []
            datalinks = []
            for url in urls:
                #links = []
                obj, content = self.requestfunction(url)
                if obj:
                    data = Parser()
                    dataex = data.dataparse(site, url, outputPath, obj, content)
                    if dataex:
                        datalinks.append(url)
                        self.datadf.loc[len(self.datadf)] = dataex
                    links = self.linkextractor(obj, baseurl, checklist)
                    self.visited.append(url)
                    returnextractlinks.extend(links)
        except Exception as e:
            print('Error in parse: ', str(e))
        finally:
            return returnextractlinks,datalinks

    def depthcheck(self, depth, baseurl, checklist, site,outputPath):
        """
        To check the depth of the website
        """
        i=0
        linksdict = []
        links = [baseurl]
        while i <= depth:
            links, data = self.parse(baseurl, links, checklist, site, outputPath)
            links,data = list(set(links)), list(set(data))
            print('Length at depth: ',i ,' = ', len(links))
            self.frontierlinks.extend(links)
            linksdict.extend(data)
            i=i+1
        return linksdict,self.datadf




if __name__ == "__main__":
    start = datetime.datetime.now()
    timestamp = start.strftime('%Y_%m_%d%H_%M_%S')
    timestamp = timestamp.replace(' ','_')
    timestamp = timestamp.replace('-','_')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--website', help = 'Website list to be selected')
    parser.add_argument('-o', '--output',help='Output folder path')
    parser.add_argument('-d', '--depth',help='depth to reach')
    args = parser.parse_args()
    
    name = args.website
    outputPath = args.output
    depth = int(args.depth)
    
    df = pd.read_csv('configuretemp.csv',sep=',',encoding='utf-8')
    df = df[df['Name'].str.match(name)]
    for i,value in df.iterrows():
        values = value
    baseurl = values[1]
    site = Website(values[0], values[1], values[2], values[3], values[4].split('|'))
    outputPath = os.path.join(outputPath,site.name,'Output'+'_'+timestamp)
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    checklist = list()
    if os.path.exists('urllist.txt'):
        with open('urllist.txt','r') as f:
            for line in f.readlines():
                line = line.strip()
                checklist.append(line)
    else:
        checklist = []
    
    crawlers = tempcrawlers()
    extractedurls, df = crawlers.depthcheck(depth,baseurl,checklist,site,outputPath)
    csvPath = os.path.join(outputPath,'data_'+timestamp+'.csv')
    if not os.path.isfile(csvPath):
        df.to_csv(csvPath,encoding='utf-8', index = False)
    else:
        df.to_csv(csvPath, mode='a', header=False, index=False,encoding='utf-8')
    print(len(extractedurls))
    with open('urllist.txt','a') as f:
        for link in extractedurls:
            f.write(link+'\n')
    print(datetime.datetime.now()-start)
