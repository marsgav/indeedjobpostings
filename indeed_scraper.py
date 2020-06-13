#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:13:20 2020

@author: marthagavidia
"""
#code adapted from CodeHeroku, tutorial linked in README

from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

## Chromedriver downloaded to work with Selenium
driver = webdriver.Chrome("./chromedriver")

dataframe = pd.DataFrame(columns=["Title","Location","Company","Salary","Description"])#specifying dateframe with column names

#sets start for webpage to start scraping for a specified range
for i in range(0,200,10):

	##Webpage changes per keyword searched
	driver.get("https://www.indeed.com/jobs?q=Unstructured+Data&l=Newark%2C+NJ&start="+str(i))#webpage to be scraped
	driver.implicitly_wait(4)#waits for all elements of page to load

	all_jobs = driver.find_elements_by_class_name('result')#job elements under results class

	for job in all_jobs:

		result_html = job.get_attribute('innerHTML')
		soup = BeautifulSoup(result_html,'html.parser')#initializes BeautifulSoup

		try:
			title = soup.find("a",class_="jobtitle").text.replace('\n','')#sorts out the html code in which elements are found
		except:
			title = 'None' #when job name not displayed

		try:
			location = soup.find(class_="location").text
		except:
			location = 'None' #when location not displayed

		try:
			company = soup.find(class_="company").text.replace("\n","").strip()
		except:
			company = 'None' #when company not displayed

		try:
			salary = soup.find(class_="salary").text.replace("\n","").strip()
		except:
			salary = 'None' #when salary not displayed

		sum_div = job.find_elements_by_class_name("summary")[0]#scraping stops when pop up comes up
		try:
			sum_div.click()#this is for instances where no pop up but click is needed to access description information
		except:
			close_button = driver.find_elements_by_class_name("popover-x-button-close")[0]#if pop up comes up, this finds the element to close the pop up
			close_button.click()#closes pop up
			sum_div.click()# tries clicking for more description information again
			

		job_desc = driver.find_element_by_id('vjs-desc').text #extracts text of job descriptions


		dataframe = dataframe.append({'Title':title,'Location':location,"Company":company,"Salary":salary,"Description":job_desc},
						ignore_index=True) #add everything that was scraped to dataframe via dictionary input


dataframe.to_csv("unstrucdata.csv") #saves as csv, update name per keyword searched

