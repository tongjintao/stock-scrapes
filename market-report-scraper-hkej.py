import requests
import datetime
from lxml import html

def market_report_scraper_by_day(base_url, date):
	"""input with the hkej market report url and date, the following function 
	will output the market report of each security reported on that date """

	market_report_url = base_url + date
	req = requests.get(market_report_url)
	
	if req.status_code != 200:
		raise Exception("Failed to load page: {0}".format(req.url))

	htmlPage = req.text
	# print htmlPage

	# <---- The following code is to write the webpage into a txt file --->

	# output_filename = 'market_report_' + day + '.txt'
	# with open(output_filename, 'w') as f:
	# 	f.write(htmlPage.encode('utf-8'))

	# <---- The above code is to write the webpage into a txt file --->
	
	htmlElement = html.fromstring(htmlPage)
	market_reports = htmlElement.xpath('//*[@id="stockTbl"]/div[@class="blkCtnt"]/table/tbody/tr[@class="table-rollout"] | \
										//*[@id="stockTbl"]/div[@class="blkCtnt"]/table/tbody/tr[@class="table-rollout alt"]')

	output_table = []

	for index, market_report in enumerate(market_reports):
		res = {}
		fields = market_report.getchildren()
		print index
		for field in fields:
			attribute = field.get('class')
			value = None
			if attribute.startswith('code'):
				for field_child in field.getchildren():
					value = field_child.text
			elif attribute.startswith('name'):
				for field_child in field.getchildren():
					value = field_child.text
			else:
				value = field.text
			res[attribute] = value
		output_table.append(res)

	for index, output_row in enumerate(output_table):
		print index
		for value in output_row:
			print output_row[value]

	return output_table

if __name__ == '__main__':
	base_url_hkej = 'http://stock360.hkej.com/marketWatch/Report?d='
	today = str(datetime.date.today())
	
	market_report_scraper_by_day(base_url_hkej, today)

	