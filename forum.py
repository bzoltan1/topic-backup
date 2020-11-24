#!/usr/bin/python3
import datetime
from datetime import timedelta
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import subprocess
import re
import argparse
from argparse import RawTextHelpFormatter
import sys

chrome_driver_path = '/home/balogh/chromedriver'
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36")
chrome_options.add_argument('--headless')
webdriver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)

epilog_text = "Backup tool for topics on Inda forums\n"

parser = argparse.ArgumentParser(description="Inda forum backup tool",
                                 epilog=epilog_text,
                                 formatter_class=RawTextHelpFormatter)
parser.add_argument('-t',
                    '--topic',
                    dest='topic',
                    action="store")

options = parser.parse_args()

with webdriver as driver:
    wait = WebDriverWait(driver, 1)
    driver.maximize_window()


    driver.get(options.topic)
    driver.implicitly_wait(1)
    forward = True
    page=1
    while forward:
        results = driver.find_elements_by_xpath('//*[@id="maintd"]/table')
        for result in results:
            nick = result.find_element_by_xpath('./tbody/tr[1]/td[1]/a[2]/strong').text
            title=result.find_element_by_xpath('./tbody/tr[1]/td[1]/span/a[2]')
            number=result.find_element_by_xpath('./tbody/tr[1]/td[3]/span[2]').text
            try:
                responded = result.find_element_by_xpath('./tbody/tr[3]/td/a').text
            except Exception:
                responded=""
            print("%s - %s - %s - %s" % (number,nick, title.get_attribute('title'), responded))
            artictle=result.find_element_by_xpath('./tbody/tr[2]/td/div')
            print(artictle.get_attribute('innerHTML'))
        page += 1
        navilink_table =  driver.find_element_by_xpath('//*[@id="maintd"]/form[1]/table/tbody/tr/td[1]')
        navilinks = navilink_table.find_elements_by_xpath('./a')

        for navilink in navilinks:
            print(navilink.text)
            if str(page) ==  navilink.text:
               driver.execute_script("arguments[0].click();", navilink)
               forward=True
               break
            if not navilink.text:
                forward=False
    driver.close()
