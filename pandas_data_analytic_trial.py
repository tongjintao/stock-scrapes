#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The program is to familarize pandas in data analytics
"""

import time
import datetime
import pandas as pd

def main():

	filename_input = 'market_report_scraper_1599_before_2016-07-08'
	df = pd.read_excel(filename_input+'.xlsx')

	""" print the mean of target stock price from investment bank by date """
	
	# State =  df.groupby(['code', 'date'])
	# code_mean = State.mean()
	# print code_mean

	""" print the variation of target stock price from investment bank by date """
	
	# newdf = df.copy()
	# State =  df.groupby(['code', 'date'])['targetPrice2']
	# newdf['x-Mean'] = State.transform( lambda x: abs(x-x.mean()) )
	# newdf['1.96*std'] = State.transform( lambda x: 1.96*x.std() )
	# newdf['Outlier'] = State.transform( lambda x: abs(x-x.mean()) > 1.96*x.std() )
	# print newdf

	""" print the variation of target stock price from investment bank by month """

	newdf = df.copy()
	newdf['date2'] = newdf['date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").strftime("%Y-%m"))
	StateMonth = newdf.groupby(['code', 'date2'])['targetPrice2']
	print StateMonth.mean()
	newdf['x-Mean'] = StateMonth.transform( lambda x: abs(x-x.mean()) )
	newdf['1.96*std'] = StateMonth.transform( lambda x: 1.96*x.std() )
	newdf['Lower'] = StateMonth.transform( lambda x: x.quantile(q=.25) - (1.5*(x.quantile(q=.75)-x.quantile(q=.25))) )
	newdf['Upper'] = StateMonth.transform( lambda x: x.quantile(q=.75) + (1.5*(x.quantile(q=.75)-x.quantile(q=.25))) )
	newdf['Outlier'] = StateMonth.transform( lambda x: abs(x-x.mean()) > 1.96*x.std() )
	print newdf

	""" export to excel """
	filename_output = filename_input + '_monthly_average'
	filename_output2 = filename_input + '_monthly_upper_lower'

	StateMonth.mean().to_frame().to_excel(filename_output+ '.xlsx')
	newdf.to_excel(filename_output2 +'.xlsx')



if __name__ == '__main__':
	start = time.time()
	main()
	elapsed = time.time() - start
	print("Completed in %s seconds") % (elapsed)
