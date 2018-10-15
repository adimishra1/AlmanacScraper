import requests
import re
import datetime
import csv
import time

from tqdm import tqdm
from bs4 import BeautifulSoup as BS 


def getData(url):
	'''
	gets the data for a given url
	and returns them
	'''

	response = requests.get(url)
	soup = BS(response.content, 'html.parser')

	weather_data = dict()
	list_weather = soup.find_all('tr', class_=re.compile('weather'))

	for data in list_weather:

		try:
			heading = data.find_all('h3')[0].string
		except IndexError:
			heading = []

		if heading != []:

			valu = data.find_all(class_='value')
			if valu != []:
			
				weather_data[data.find_all('h3')[0].string] = valu[0].string
			else:
				weather_data[data.find_all('h3')[0].string] = None

	return weather_data

def getallUrl(url):
	'''
	Returns the list of all urls for a given city, and between 2018(1 Jan) and 1998(1 Jan)
	'''

	starttime = datetime.date(2008,1,1)
	endtime = datetime.date(2018,7,1)

	
	
	list_url = list()
	for n in range((endtime-starttime).days):
		DATE = starttime + datetime.timedelta(n)
		list_url.append(getlistUrl(url, DATE))
	return list_url


def getlistUrl(url, date):
	'''
	returns the list of urls for the corresponding city, 
	for a given date and 
	for a given url(in this project, the almanac website)
	'''

	new_url = url +'/'+ str(date)
	return new_url


def main():
	'''
	Produces list of all the urls, and gets the data in csv format for each city
	'''

	response = requests.get('https://www.almanac.com/weather/history/MD')
	soup = BS(response.content, 'html.parser')

	state_list = list()

	state_tag = soup.find_all('div', class_='statelist')[0].find_all('a',href=True)
	# Gets the url of all the states
	for tag in state_tag:

		state_url = 'https://www.almanac.com' + tag['href']
		state_list.append(state_url)

	start= None
	for num,i in enumerate(state_list):
		if(i.rsplit('/')[-1] == 'New+Carrollton'):
			start = num
	

	state_list = state_list[start:]
	sbar = tqdm(total=len(state_list))

	# For a given state, calculate the list of urls possible
	# for different dates, and then scrape the data and export
	# the data into csv for a given state

	for state in state_list:

		dateurl = getallUrl(state)
		
		header = ['Year', 'Month', 'Day', 'Maximum Temperature', 'Minimum Temperature', 'Mean Sea Level Pressure', 'Total Precipitation', 'Mean Dew Point','Mean Wind Speed', 'Maximum Sustained Wind Speed','Maximum Wind Gust','Visibility']
		header1 = header[3:]
		name = state.rsplit('/')[-1] + '.csv'

		sbar.update(1)
		#Add the header row
		with open(name,'a+') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(header)

		csvFile.close()
		#print(header)

		for sdateurl in dateurl:
			date = sdateurl.rsplit('/')[-1]

			data = getData(sdateurl)
			year_data = list()
			year_data.append(date.rsplit('-')[-1])
			year_data.append(date.rsplit('-')[-2])
			year_data.append(date.rsplit('-')[-3])

			for key in header1:
				year_data.append(data[key])

			#print(year_data)

			with open(name, 'a+') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(year_data)

			csvFile.close()
	sbar.close()

				
if __name__ == '__main__':
	main()



