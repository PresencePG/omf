import os, omf, csv
from matplotlib import pyplot as plt
from pprint import pprint as pp
from dateutil.parser import parse as parse_dt
import matplotlib.dates as mdates


''' TODOS
XXX A little bit of plotting.
XXX Additional devices? See superHouse.glm.
OOO Parse and display datetimes correctly. {'# timestamp': '2012-01-01 23:53:00 EST'}
OOO Other variables to watch? Studies to do?
OOO Switch to superHouse.glm?
'''

def workAndGraph(modelType):
	# Run GridLAB-D on the GLM.
	if modelType == 'Gas':
		fileName = 'heat_gas_gridlabd_sim.glm'
	elif modelType == 'HeatPump':
		fileName = 'heatPump_gridlabd_sim.glm'
	elif modelType == 'Resistance':
		fileName = 'resistance_heat_gridlabd_sim.glm'
	print(fileName)
	print type(fileName)
	print ('gridlabd '
		+fileName)
	os.system('gridlabd '+fileName)

	# Get the data
	fileOb = open('out_house_power.csv')
	for x in range(8):
		# Burn the headers.
		fileOb.readline()
	data = list(csv.DictReader(fileOb))
	# pp(data)

	# Do something about datetimes.
	# dt = parse_dt("Aug 28 1999 12:00AM")
	# print dt

	# Plot something.
	plt.switch_backend('MacOSX')
	plt.figure()
	formatter = mdates.DateFormatter('%H-%m-%S')
	dates = mdates.datestr2num([x.get('# timestamp').split(' ')[1] for x in data])
	plt.plot_date(dates, [float(x.get('heating_demand', 0.0)) for x in data], '-', label="Heating")
	plt.plot_date(dates, [float(x.get(' cooling_demand', 0.0)) for x in data], '-', label="Cooling")
	ax = plt.gcf().axes[0]
	ax.xaxis.set_major_formatter(formatter)
	plt.gcf().autofmt_xdate(rotation=45)
	plt.title('New Years Day, Huntsville, AL, '+modelType+' Heating System')
	plt.legend()
	plt.xlabel('Time Stamp')
	plt.ylabel('Demand (kW)')
	plt.figure()
	plt.title('New Years Day, Huntsville, AL, Temperatures')
	plt.plot_date(dates, [float(x.get(' air_temperature', 0.0)) for x in data], '-', label="Indoor")
	plt.plot_date(dates, [float(x.get(' outdoor_temperature', 0.0)) for x in data], '-', label="Outdoors")
	plt.plot_date(dates, [float(x.get(' heating_setpoint', 0.0)) for x in data], '-', label="heating_setpoint")
	ax = plt.gcf().axes[0]
	ax.xaxis.set_major_formatter(formatter)
	plt.gcf().autofmt_xdate(rotation=45)
	plt.legend()
	plt.xlabel('Time Stamp')
	plt.ylabel('Temperature (degF)')
	plt.show()

if __name__ == '__main__':
	try: 
		#Parse Command Line
		parser = argparse.ArgumentParser(description='Simulates heat/cool power use on a canonical .glm single house model')
		parser.add_argument('model_type', metavar='base', type=str,
		                    help='Please specify type of model, being gas, resistance, or heat pump')
		args = parser.parse_args()
		modelType = args.model_type
		workAndGraph(modelType)
	except:
		workAndGraph('Resistance')