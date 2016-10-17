#coding=utf-8

import re
import requests
import urllib2
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd

def find_officiers_from_stock(stocknumber):
	url_base = 'https://webb-site.com'
	url_stock = url_base + '/dbpub/orgdata.asp?code='+ str(stocknumber) +'&Submit=current'
	date = '2016-10-17'

	# Get officer url
	r = requests.get(url_stock)
	htmlPage = r.text
	htmlElement = html.fromstring(htmlPage)

	## Assuming HTML structure unchanged
	officer_path = htmlElement.xpath \
					('//html/body/div[@class="mainbody"]/ul[1]/li[2]/a') \
					[0].get('href')

	url_officer = url_base + officer_path + '&sort=namup&d=' + date

	# Get officers info
	r = requests.get(url_officer)
	htmlPage = r.text
	htmlElement = html.fromstring(htmlPage)

	officers_infos = htmlElement.xpath \
					('//html/body/div[@class="mainbody"]/table[1]/tr[@class="total"]')

	officers_db = []

	for officer_infos in officers_infos:
		# print officer_infos
		# print html.tostring(officer_infos)

		name = officer_infos.xpath('td[2]/a')
		position = officer_infos.xpath('td[5]/span/span')
		
		officer_dict = {}
		officer_dict['name'] = name[0].text
		officer_dict['link'] = name[0].get('href')
		officer_dict['position'] = position[0].text
		officer_dict['company'] = stocknumber

		officers_db.append(officer_dict)

	officers_df = pd.DataFrame(data=officers_db)

	print officers_df


if __name__ == '__main__':
	stocknumber = 1
	find_officiers_from_stock(stocknumber)