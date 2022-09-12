# -*- coding: utf-8 -*-


'''
We plot here the average values for all metrics through time.
To make the comparison between different metrics possible, we 
normalize them according to their values during the entire period (01/jan to 29/feb).
'''



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.transforms as mtransforms

import os

from matplotlib import rc

# Latex font --------------------
rc('text', usetex=True)
font = {'family' : 'normal',
         'weight' : 'bold',
         'size'   : 12}

rc('font', **font)
params = {'legend.fontsize': 14}
plt.rcParams.update(params)
# -------------------------------


# Plotting 
fig, ax = plt.subplots(2, 1)
fig.set_size_inches(6, 5)






root_path = '../../results/'

# Finding the directories within the results folder
path_directories = next(os.walk(root_path +'.'))[1]

# Sorting them according to their date
path_directories.sort()
print(path_directories)
# Removing the average case
#path_directories.remove('averaged_chinese_network')





metrics = ['strength', 'closeness_weight', 'vulnerability_weight'] #, 'density', 'kappa']


# rows: networks
# cols: average metrics from each network
time_series_metrics = np.zeros((len(path_directories), len(metrics)))

row = 0
for d in path_directories:

	col = 0
	for m in metrics:
		# Load the corresponding file with the metric
		file_name = root_path + d + '/metrics/' + m + '_0.csv' 
		metric = np.genfromtxt(file_name, delimiter=';')

		if m == 'density' or m == 'kappa':
			time_series_metrics[row,col] = metric
		else:
			# Storing the average number
			time_series_metrics[row,col] = np.mean(metric[:,2])
		col += 1
	row += 1



# Normalizing metrics, considering the entire period (01/jan to 29/fev)
for c in range(len(metrics)):
	min_value = np.min(time_series_metrics[:,c])
	max_value = np.max(time_series_metrics[:,c])

	#max_value = np.max(time_series_metrics[:,c])
	time_series_metrics[:,c] = (time_series_metrics[:,c] - min_value) / (max_value - min_value)



#lbls = [r'$k$', r'$b$', r'$c$', r'$v$', r'$s$', r'$b_w$', r'$c_w$', r'$v_w$', r'$d$', r'$\kappa$'] 
#colors   = ['black', 'palevioletred','brown','darkgreen', 'gray',  'pink', 'red', 'mediumseagreen', 'purple', 'blue']

lbls = [r'$s$', r'$c_w$', r'$v_w$', r'$d$', r'$\kappa$'] 
colors = ['gray',  'red', 'mediumseagreen', 'purple', 'blue']

metric_index = 0
for m in metrics:	
	#if metric_index < 4:
	#	ax[0].plot(np.linspace(1,len(path_directories),len(path_directories)), time_series_metrics[:,metric_index], color=colors[metric_index], lw=2, label=lbls[metric_index], linestyle='--', zorder=2)
	#else:

	ax[0].plot(np.linspace(1,len(path_directories),len(path_directories)), time_series_metrics[:,metric_index], color=colors[metric_index], lw=2, label=lbls[metric_index], zorder=2)


	#ax[0].plot(np.linspace(1,len(path_directories),len(path_directories)), time_series_metrics[:,metric_index]+time_series_metrics_std[:,metric_index], 
	#	color=colors[metric_index], lw=2, zorder=2, alpha=0.5)
	#ax[0].plot(np.linspace(1,len(path_directories),len(path_directories)), time_series_metrics[:,metric_index]-time_series_metrics_std[:,metric_index], 
	#	color=colors[metric_index], lw=2, zorder=2, alpha=0.5)

	metric_index += 1

# Spring festival (Chunyun) begins
ax[0].vlines(10,-0.05,1.05, colors='k', linestyle='dashed')
ax[0].text(6, 1.05, "Spring festival", fontsize=8)

# Wuhan travel ban
ax[0].vlines(23,-0.05,1.05, colors='k', linestyle='dashed')
ax[0].text(19, 1.12, "Wuhan", fontsize=8)
ax[0].text(17.25, 1.05, "travel ban", fontsize=8)

# Lunar new year
ax[0].vlines(25,-0.05,1.05, colors='k', linestyle='dashed')
ax[0].text(24.75, 1.12, "Lunar", fontsize=8)
ax[0].text(24.75, 1.05, "new year", fontsize=8)


# End of Chunyun
ax[0].vlines(49,-0.05,1.05, colors='k', linestyle='dashed')
ax[0].text(45, 1.12, "End of the", fontsize=8)
ax[0].text(44, 1.05, "Spring festival", fontsize=8)





# Plot configuration
#plt.plot()
ax[0].legend(ncol=1, fontsize=8, loc='upper right')


# converting the names into dates: dd-mm
for i in range(len(path_directories)):
	aux_date = path_directories[i][13:] # only ddmm
	month = 'jan' if aux_date[:2]=='01' else 'feb'
	path_directories[i] = aux_date[2:] + '-' + month

for i in range(len(path_directories)):
	if( i!=0 and i!=9 and i!=22 and i!=24 and i!=48 and i!=59):
		path_directories[i] = ''

ax[0].set_xlim([1,60])
ax[0].set_ylim([-0.05,1.2])
ax[0].set_xticks([])

ax[0].set_ylabel('Normalized metrics')





















root_path = '../../results/'

# Finding the directories within the results folder
path_directories = next(os.walk(root_path +'.'))[1]

# Sorting them according to their date
path_directories.sort()
# Removing the average case
#path_directories.remove('averaged_chinese_network')

#metrics = ['degree', 'betweenness', 'closeness', 'vulnerability', 'strength', 'betweenness_weight', 'closeness_weight', 'vulnerability_weight', 'density', 'kappa']
#metrics = ['strength', 'closeness_weight', 'vulnerability_weight', 'density', 'kappa']
metrics = ['strength']


# rows: networks

cities = ['Shanghai', 'Beijing', 'Guangzhou', 'Chengdu', 'Wuhan']
cities_code = ['310000', '110000', '440100', '510100', '420100']
time_series_metrics = np.zeros((len(path_directories),len(cities)))
time_series_metrics_std = np.zeros((len(path_directories),len(cities)))

row = 0

mean_values = []
std_values = []

for d in path_directories:

	
	for m in metrics:
		# Load the corresponding file with the metric
		file_name = root_path + d + '/metrics/' + m + '_0.csv' 
		df = pd.read_csv(file_name, delimiter=';', header=None, usecols=[1,2], names=['city_code', 'metric'])

		col = 0
		for cc in cities_code:
			# find the metric related to the city code cc
			metric = float(df[df['city_code'] == cc]['metric'])
			time_series_metrics[row,col] = metric
			col += 1

		mean_values.append(np.mean(df['metric']))
		std_values.append(np.std(df['metric']))

	row += 1

mean_values = np.array(mean_values)
std_values = np.array(std_values)

print(mean_values)
print(std_values)

'''
# Normalizing metrics, considering the entire period (01/jan to 29/fev)
min_value = np.min(time_series_metrics)
max_value = np.max(time_series_metrics)
time_series_metrics = (time_series_metrics - min_value) / (max_value - min_value)'''



# Plotting 
#fig, ax = plt.subplots(1, 1)
#fig.set_size_inches(6, 2.5)

#lbls = [r'$k$', r'$b$', r'$c$', r'$v$', r'$s$', r'$b_w$', r'$c_w$', r'$v_w$', r'$d$', r'$\kappa$'] 
#colors   = ['black', 'palevioletred','brown','darkgreen', 'gray',  'pink', 'red', 'mediumseagreen', 'purple', 'blue']

lbls = cities
colors   = ['gray',  'red', 'mediumseagreen', 'purple', 'blue']
colors = ['palevioletred','brown','darkgreen', 'pink', 'darkgoldenrod']

city_index = 0
for m in cities:	
	ax[1].plot(np.linspace(1,len(path_directories),len(path_directories)), time_series_metrics[:,city_index], color=colors[city_index], lw=2, label=lbls[city_index], zorder=2)
	city_index += 1


ax[1].plot(np.linspace(1,len(path_directories),len(path_directories)), mean_values, color='gray', lw=2, zorder=2)
#ax[1].plot(np.linspace(1,len(path_directories),len(path_directories)), mean_values+std_values, color='plum', lw=2, zorder=2, alpha=0.5)
#ax[1].plot(np.linspace(1,len(path_directories),len(path_directories)), mean_values-std_values, color='plum', lw=2, zorder=2, alpha=0.5)

mean_values_minus_std_values = np.array([ np.max([0,mean_values[i]-std_values[i]]) for i in range(len(std_values))])

ax[1].fill_between(np.linspace(1,len(path_directories),len(path_directories)), mean_values_minus_std_values, mean_values+std_values, color='gray', alpha=0.5)


# Spring festival (Chunyun) begins
ax[1].vlines(10,-0.05,3000, colors='k', linestyle='dashed')
ax[1].text(6, 3100, "Spring festival", fontsize=8)

# Wuhan travel ban
ax[1].vlines(23,-0.05,3000, colors='k', linestyle='dashed')
ax[1].text(19, 3300, "Wuhan", fontsize=8)
ax[1].text(17.25, 3100, "travel ban", fontsize=8)

# Lunar new year
ax[1].vlines(25,-0.05,3000, colors='k', linestyle='dashed')
ax[1].text(24.75, 3300, "Lunar", fontsize=8)
ax[1].text(24.75, 3100, "new year", fontsize=8)


# End of Chunyun
ax[1].vlines(49,-0.05,3000, colors='k', linestyle='dashed')
ax[1].text(45, 3300, "End of the", fontsize=8)
ax[1].text(44, 3100, "Spring festival", fontsize=8)





# Plot configuration
plt.plot()
ax[1].legend(ncol=1, fontsize=8.5, loc=(0.5,0.3))


# converting the names into dates: dd-mm
for i in range(len(path_directories)):
	aux_date = path_directories[i][13:] # only ddmm
	month = 'jan' if aux_date[:2]=='01' else 'feb'
	path_directories[i] = aux_date[2:] + '-' + month



for i in range(len(path_directories)):
	if( i!=0 and i!=9 and i!=22 and i!=24 and i!=48 and i!=59):
		path_directories[i] = ''



ax[1].set_xlim([1,60])
ax[1].set_ylim([-0.05,3500])


plt.xticks(ticks=np.linspace(1,60,60), labels=path_directories, fontsize=12, rotation=90)

ax[1].set_ylabel('Strength')




# label physical distance to the left and up:
trans = mtransforms.ScaledTranslation(-20/72, 7/72, fig.dpi_scale_trans)
ax[0].text(0.0, 0.95, 'a)', transform=ax[0].transAxes + trans, fontsize='medium', va='bottom', fontfamily='serif', fontweight='bold')
ax[1].text(0.0, 0.95, 'b)', transform=ax[1].transAxes + trans, fontsize='medium', va='bottom', fontfamily='serif', fontweight='bold')


plt.tight_layout()

fig.savefig(root_path + 'time_series_metrics_and_strength_big_cities.png', dpi=300)
fig.savefig(root_path + 'time_series_metrics_and_strength_big_cities.pdf', dpi=300)
fig.savefig(root_path + 'time_series_metrics_and_strength_big_cities.png', dpi=300)
fig.savefig(root_path + 'time_series_metrics_and_strength_big_cities.pdf', dpi=300)