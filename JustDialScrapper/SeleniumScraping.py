from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import re
import logging
import pandas as pd
from utitlity import *
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # Import at top of file
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
import io



class SeleniumDriver:
    def __init__(self, path):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

    def scrollpage(self):
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return self.driver

    def getUrl(self,url):
        self.driver.get(url)
        self.driver = self.scrollpage()

    def setLocation(self,location):
        CityPath = '//*[@id="{}"]'.format(location)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'city')))
        self.driver.find_element_by_id('city').clear()
        self.driver.find_element_by_id('city').send_keys(location)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, CityPath)))
        self.driver.find_element_by_xpath(CityPath).click()

    def searchItem(self,item):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'srchbx')))
        self.driver.find_element_by_id('srchbx').clear()
        self.driver.find_element_by_id('srchbx').send_keys(item)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]/button')))
        self.driver.find_element_by_xpath('//*[@id="search"]/button').click()
        self.scrollpage()
        return self.driver
