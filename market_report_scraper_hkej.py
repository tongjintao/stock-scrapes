import requests
import datetime
from lxml import html
import pandas as pd

def generate_market_report_from_xpath(market_reports, date):
	output_table = []
	for index, market_report in enumerate(market_reports):
		res = {}
		res['date'] = date
		try:
			fields = market_report.getchildren()
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
		except:
			continue
	return output_table


def market_report_scraper_by_date(base_url, date):
	"""input with the hkej market report url and datetime.date, the following function 
	will output the market report of each security reported on that date in xlsx """

	date = str(date)
	market_report_base_url = base_url + date
	req = requests.get(market_report_base_url)
	
	if req.status_code != 200:
		raise Exception("Failed to load page: {0}".format(req.url))

	htmlPage = req.text
	htmlElement = html.fromstring(htmlPage)

	pages = htmlElement.xpath('//*[@id="stockTbl"]/div[@class="blkCtnt"]/div[@class="pagingWrap"]/span/a')
	market_report_urls = []

	for page in pages:
		url = 'http://stock360.hkej.com'+ page.get('href')
		market_report_urls.append(url)

	output_table = []

	for market_report_url in market_report_urls:
		req = requests.get(market_report_url)
	
		if req.status_code != 200:
			raise Exception("Failed to load page: {0}".format(req.url))

		htmlPage = req.text
		htmlElement = html.fromstring(htmlPage)

		market_reports = htmlElement.xpath('//*[@id="stockTbl"]/div[@class="blkCtnt"]/table/tbody/tr[@class="table-rollout"] | \
											//*[@id="stockTbl"]/div[@class="blkCtnt"]/table/tbody/tr[@class="table-rollout alt"]')
		output_table_by_page = generate_market_report_from_xpath(market_reports, date)
		output_table.extend(output_table_by_page)

	df = pd.DataFrame(data=output_table)
	output_filename = 'market_report_scraper_' + date + '.xlsx'
	
	# df = df[['date','firm','name','code','sector','action1','targetPrice1','action2','targetPrice2','summary']]

	df.to_excel(output_filename, index=False)

	return df

def market_report_scraper_from_date(base_url, start_date, days):
	df = pd.DataFrame()
	for date in [start_date - datetime.timedelta(n) for n in range(days)]:
		print date
		df_by_date = market_report_scraper_by_date(base_url, date)
		df = df.append(df_by_date,)
	
	df = df[['date','firm','name','code','sector','action1','targetPrice1','action2','targetPrice2','summary']]
	output_filename = 'market_report_scraper_' + str(days) + '_before_' + str(start_date) + '.xlsx'
	df.to_excel(output_filename, index=False)
	return df

if __name__ == '__main__':
	base_url_hkej = 'http://stock360.hkej.com/marketWatch/Report?d='
	today = datetime.date.today()
	one_day = datetime.timedelta(days=1)
	
	# market_report_scraper_by_date(base_url_hkej, datetime.date(2012, 2, 23))
	market_report_scraper_from_date(base_url_hkej, today, 1599)

	