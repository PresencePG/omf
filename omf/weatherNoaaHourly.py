import requests, csv, json, collections
#for list of available stations go to:
#ftp://ftp.ncdc.noaa.gov/pub/data/uscrn/products/hourly02 

def pullWeather(year, station, outputPath):
	url = 'https://www1.ncdc.noaa.gov/pub/data/uscrn/products/hourly02/' + year + '/CRNH0203-' + year + '-' + station + '.txt'
	r = requests.get(url)
	data = r.text
	tempData = []
	for x in range(0,8760):
		temp = ''
		for y in range(x*244+59,x*244+64):
			temp+=data[y]
		tempData.append(float(temp))
	with open(outputPath, 'wb') as myfile:
		wr = csv.writer(myfile,lineterminator = '\n')
		for x in range(0,8760): 
			wr.writerow([tempData[x]])

#TODO: create a tests function.
def _tests():
	pullWeather('2017','KY_Versailles_3_NNW','weatherNoaaTemp.csv')

if __name__ == '__main__':
	_tests()