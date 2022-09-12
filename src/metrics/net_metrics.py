import sys


import igraph as ig
import networkx as nx
import numpy as np
import pandas as pd
import vulnerability as vn

# to create directories
from pathlib import Path



# The network name comes from command line. 
net_name = sys.argv[1]

relative_path = '../../results/' + net_name + '/metrics/'

# create directory if it does not exist
Path(relative_path).mkdir(parents=True, exist_ok=True)




def export_data(g, data, stat, thresh):

    # Saving results to file
    file_out = open(relative_path +  stat + '_' + str(thresh) + '.csv', 'w')
    for i in range(g.vcount()):
        file_out.write(str(g.vs[i]['node_num']) + ';' + str(g.vs[i]['city_code']) + ';' +  str(data[i]) + '\n')
    file_out.close()


def heterogeneity(g):
  degrees = g.degree()
  acc = 0
  for k in degrees:
    acc = acc + k**2
  avg = acc/len(degrees)
  het = avg/(np.mean(degrees)**2)
  return het




# reading the network from file
g_ori = ig.Graph.Read_GraphML('../../input_data/networks/' + net_name + '.GraphML')
g_ori.to_undirected()


thresholds = [0]

# Metrics for the networks with flows above the defined thresholds
for thresh in thresholds:
    # make a copy of the original network
    g = g_ori.copy()

    ####### Removing edges whose weights are below a certain threshold #######
    edge_removal_list = []
    for i in range(g.ecount()):
        if g.es[i]['weight'] < thresh:
            edge_removal_list.append(i)

    g.delete_edges(edge_removal_list)
    ##########################################################################

    # Convert to undirected graph
    #g = g.as_undirected()
    
    print('  Density')
    density = g.density()
    file_out = open(relative_path +  'density' + '_' + str(thresh) + '.csv', 'w')
    file_out.write(str(density))
    file_out.close()

    print('  Kappa')
    kappa = heterogeneity(g)
    file_out = open(relative_path +  'kappa' + '_' + str(thresh) + '.csv', 'w')
    file_out.write(str(kappa))
    file_out.close()

    
    ########## UNWEIGHTED ##########
    print('  Degree')
    degrees = g.degree()
    export_data(g, degrees, 'degree', thresh)
    
    print('  Betweenness')
    betweenness = g.betweenness(vertices=None, directed=False, cutoff=None) #normalized_betweenness(g)
    export_data(g, betweenness, 'betweenness', thresh)

    print('  Closeness')
    closeness = g.closeness(vertices=None, mode='all', cutoff=None, weights=None, normalized=True)
    export_data(g, closeness, 'closeness', thresh)

    print('  Vulnerability')
    vuln = vn.vulnerability(g, weights=None)
    export_data(g, vuln, 'vulnerability', thresh)
    

    ########## WEIGHTED ##########

    # strength (flows are the weights)
    print('  Strength')
    strength = g.strength(weights='weight')
    export_data(g, strength, 'strength', thresh)
    
    # Inverse of the flow 
    # This is a valid notion of distance in mobility networks, 
    # since the higher the flows between neighbors, the closer they are.
    g.es['w_inv'] = 1.0 / np.array(g.es['weight'])
    
    print('  Weighted Betweenness')
    betweenness_w = g.betweenness(vertices=None, directed=False, cutoff=None, weights='w_inv') 
    export_data(g, betweenness_w, 'betweenness_weight', thresh)

    print('  Weighted Closeness')
    closeness_w = g.closeness(vertices=None, mode='all', cutoff=None, weights='w_inv', normalized=True)
    export_data(g, closeness_w, 'closeness_weight', thresh)
    
    print('  Weighted Vulnerability')
    vuln_w = vn.vulnerability(g, weights='w_inv')
    export_data(g, vuln_w, 'vulnerability_weight', thresh)
