import igraph as ig
import pandas as pd
import numpy as np
import sys


# The network name comes from command line. 
net_name = sys.argv[1]


# reading the network from file
g = ig.Graph.Read_GraphML('../input_data/networks/' + net_name + '.GraphML')
g.to_undirected()


# Coordinates
df = pd.read_csv('../input_data/coordinates.csv', delimiter=',')

g.vs["y"] = -df["LATITUDE"]
g.vs["x"] = df["LONGITUDE"]
g.vs["label"] = df["CITY_NAME"]


min_x = np.min(g.vs["x"])
max_x = np.max(g.vs["x"])
min_y = np.min(g.vs["y"])
max_y = np.max(g.vs["y"])

dim_x = max_x - min_x
dim_y = max_y - min_y
scale = 20.0
width = dim_x*scale
height = dim_y*scale



# Metrics
df = pd.read_csv('../results/' + net_name + '/metrics/strength_0.csv', delimiter=';', header=None)
df.columns = ['id', 'city_code', 'metric']
print(df['metric'])

g.vs['strength'] = df['metric']



# normalization
node_size = np.array(df['metric'])
max_size = max(node_size)
min_size = min(node_size)

# Min and max plot sizes
T_min = 8
T_max = 20
node_size = T_min + ( (node_size - min_size) / (max_size - min_size) ) * (T_max - T_min) # normalization

g.vs["size"] = node_size.tolist()



layout = []
for i in range(g.vcount()):

	# coordinates
	layout.append((g.vs[i]["x"],g.vs[i]["y"]))

	# keep only the names of the biggest cities and color them differently
	if(g.vs[i]["label"] != "Shanghai" and 
	   g.vs[i]["label"] != "Beijing" and
	   g.vs[i]["label"] != "Guangzhou" and
	   g.vs[i]["label"] != "Chengdu" and
	   g.vs[i]["label"] != "Wuhan"):

		g.vs[i]["label"] = ""


	if(g.vs[i]['strength'] < 161):
		g.vs[i]['color'] = 'green'
	elif(g.vs[i]['strength'] >= 161 and g.vs[i]['strength'] < 340):
		g.vs[i]['color'] = 'yellow'
	elif(g.vs[i]['strength'] >= 340 and g.vs[i]['strength'] < 493):
		g.vs[i]['color'] = 'orange'
	else:
		g.vs[i]['color'] = 'red'



# Edge color
for i in range(g.ecount()):
	if(g.es[i]['weight'] < 0.018):
		g.es[i]['color'] = 'green'
	elif(g.es[i]['weight'] >= 0.018 and g.es[i]['weight'] < 0.049):
		g.es[i]['color'] = 'yellow'
	elif(g.es[i]['weight'] >= 0.049 and g.es[i]['weight'] < 1):
		g.es[i]['color'] = 'orange'
	else:
		g.es[i]['color'] = 'red'



visual_style = {}
visual_style["vertex_size"] = g.vs["size"]
visual_style["edge_width"] = 0.1
visual_style["layout"] = layout
visual_style["bbox"] = (width, height)
visual_style["margin"] = 30

ig.plot(g, '../results/network_' + net_name + '.png', **visual_style)

