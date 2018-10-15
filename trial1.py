import requests
import re
import datetime
import csv
import os

from tqdm import tqdm
from bs4 import BeautifulSoup as BS 
import multiprocessing as mp

PROCS=50

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

def parse(state):

	dateurl = getallUrl(state)

	header = ['Date','Year', 'Month', 'Day', 'Maximum Temperature', 'Minimum Temperature', 'Mean Sea Level Pressure', 'Total Precipitation', 'Mean Dew Point','Mean Wind Speed', 'Maximum Sustained Wind Speed','Maximum Wind Gust','Visibility']
	header1 = header[4:]
	name = state.rsplit('/')[-1] + '.csv'
	#sbar.update(1)
	#Add the header row
	if not os.path.isfile(name):
		with open(name,'a+') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(header)

		csvFile.close()
	#print(header)
	ubar = tqdm(total=len(dateurl))
	for sdateurl in dateurl:
		date = sdateurl.rsplit('/')[-1]
		curr_date = datetime.datetime.strptime(date,'%Y-%m-%d')
		#print(" Date {} Type {}".format(curr_date, type(curr_date)))
		last_date = list()
		with open(name, 'r') as csvFile:
			csv_reader = csv.reader(csvFile, delimiter=',')
			
			for row in reversed(list(csv_reader)):
				last_date.append(row)
				
				break
		last_date = last_date[0][0]
		flag=0
		try:
			last_date = datetime.datetime.strptime(last_date,'%Y-%m-%d %H:%M:%S')
		except TypeError:
			flag=1
			last_date = curr_date
			
		except ValueError:
			flag=1
			last_date = curr_date
			


		if last_date > curr_date :
			pass
		elif last_date <= curr_date:
			if last_date < curr_date or flag==1:
				flag=0
				ubar.update(1)
				data = getData(sdateurl)
				year_data = list()
				year_data.append(curr_date)
				year_data.append(date.rsplit('-')[0])
				year_data.append(date.rsplit('-')[1])
				year_data.append(date.rsplit('-')[2])

				for key in header1:
					year_data.append(data[key])

				#print(year_data)
				with open(name, 'a+') as csvFile:
					writer = csv.writer(csvFile)
					writer.writerow(year_data)

				csvFile.close()
			else:
				pass


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

	start = end = None
	for num,i in enumerate(state_list):
		if(i.rsplit('/')[-1] == 'Ellicott+City'):
			end = num 
		

	state_list = state_list[0:end]
	sbar = tqdm(total=len(state_list))
	# For a given state, calculate the list of urls possible
	# for different dates, and then scrape the data and export
	# the data into csv for a given state

	pool = mp.Pool(processes=PROCS)
	#mapped_process = partial(parse, callback=update)
	pool.starmap(parse,zip((i for i in state_list)))
	pool.close()
	pool.join()

	

		
		
			


				
if __name__ == '__main__':
	main()



