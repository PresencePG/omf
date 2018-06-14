import opendssdirect as dss
import networkx as nx
import matplotlib.pyplot as plt
import pip


def calculateGraph(df, phase=1):
	graph = nx.Graph()
	data = df[['Bus1', 'Bus2']].to_dict(orient="index")
	for key in data:
		voltage_line = data[key]
		graph.add_edge(voltage_line["Bus1"].split(".")[0], voltage_line["Bus2"].split(".")[0])
	positions = {}
	for name in dss.Circuit.AllBusNames():
		dss.Circuit.SetActiveBus(name)
		if phase in dss.Bus.Nodes():
			index = dss.Bus.Nodes().index(phase)
			re, im = dss.Bus.PuVoltage()[index:index+2]
			voltage = abs(complex(re, im))
			distance = dss.Bus.Distance()
			print distance
			positions[dss.Bus.Name()] = (distance, voltage)
	return graph, positions

def plotGraph():
	lines = dss.utils.lines_to_dataframe()
	graph, position = calculateGraph(lines)
	fig, ax = plt.subplots(1, 1, figsize=(16, 10))
	nx.draw_networkx_nodes(graph, position, labels={x: x for x in graph.nodes()})
	nx.draw_networkx_nodes(graph, position, labels={x: x for x in graph.nodes()})
	nx.draw_networkx_nodes(graph, position, labels={x: x for x in graph.nodes()})
	ax.set_xlabel('Distances [km]')
	ax.set_ylabel('Voltage [P.u]')
	ax.set_title('VOLTAGE PROFILE')
	plt.show()

if __name__ == "__main__":
	dss.run_command('Redirect ./short_circuit.dss')
	dss.run_command('New EnergyMeter.Main Line.650632 1')
	'''
    dss.run_command(
        "New Storage.{bus_name} Bus1={bus_name} phases=1 kV=2.2 kWRated={rating} kWhRated={kwh_rating} kWhStored={initial_state} %IdlingkW=0 %reserve=0 %EffCharge=100 %EffDischarge=100 State=CHARGING".format(
        bus_name='675',
        rating=20,
        kwh_rating=20,
        initial_state=20
    ))
    '''

	'''
    dss.run_command(
        "New Storage.{bus_name} Bus1={bus_name} phases=1 kV=2.2 kWRated={rating} kWhRated={kwh_rating} kWhStored={initial_state} %IdlingkW=0 %reserve=0 %EffCharge=100 %EffDischarge=100 State=CHARGING".format(
        bus_name='611',
        rating=20,
        kwh_rating=20,
        initial_state=20
    ))
    '''
	dss.run_command('Solve')
	'''
    dss.run_command('Clear')
	dss.run_command('New Circuit.MyCircuit  BasekV=0.6')
	dss.run_command('New line.MyLine Bus1=SourceBus  Bus2=LoadBus R1=1 X1=0.5 R0=1 X0=0.5 Length=1')
	dss.run_command('New Load.MyLoad Bus1=LoadBus kV=0.6 kW=3 PF=0.6')
	dss.run_command('Show voltages')
	dss.run_command('Show curr')
	dss.run_command('Show powers')
	dss.run_command('Show losses')
	'''
	plotGraph()
	print dss.Vsources.PU()
