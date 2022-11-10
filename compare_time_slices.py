from tkinter.filedialog import askdirectory
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as patches
import glob
import os
from scipy import stats
import random

#path to folder with *_merged.csv files (after running merged_cores_files.py):
print ("Indicate a folder where you have OC3 merged files created with 'merge_cores_files_database.py'")
path0 = askdirectory()
path = path0 + "/"

colstouse = [0,1,2,4,5,6,7,8]

rann=str(int(random.uniform(0, 100)*100))


def askforinput(): 
  correct=False
  species = 0
  yr1=0
  yr2=0
  yr3=0
  yr4=0
  print ("Select averaging window for time slice")
  while(not correct):
    try:
      species = int(input("Enter taxon (1=C. wuellerstorfi; 2=Any Cibs.; 3=All taxa): ")) 
      yr1 = int(input("Enter start year of first time slice: "))
      yr2 = int(input("Enter end year of first time slice: "))
      yr3 = int(input("Enter start year of second time slice: "))
      yr4 = int(input("Enter end year of second time slice: "))
      correct=True
    except ValueError:
      print('Error, enter whole numbers')
    return species,yr1,yr2,yr3,yr4

exit = False
sp,y1,y2,y3,y4 = askforinput()
mergedfiles = glob.glob(path + "*_merged.csv")
first = True
for file in mergedfiles:
  data = pd.read_csv(file, usecols=colstouse)
# select time window
  olddata = data[data["age_model (y BP)"] > y1]
  mydata = olddata[olddata["age_model (y BP)"] < y2]
# average over time window
  mean = mydata.describe()["mean":"mean"]
  if first == True:
# create initial output data frame
    out = mean
    first = False
  else:
# add rows for each additional core
    out = out.append(mean)
# replace missing values with -999
out = out.fillna(value=-999)
out = out[out['Longitude (degE)'] != -999.0]
out.to_csv("slice1.csv",index=False)
first = True
for file in mergedfiles:
  data = pd.read_csv(file, usecols=colstouse)
# select time window
  olddata = data[data["age_model (y BP)"] > y3]
  mydata = olddata[olddata["age_model (y BP)"] < y4]
# average over time window
  mean = mydata.describe()["mean":"mean"]
  if first == True:
# create initial output data frame
    out = mean
    first = False
  else:
# add rows for each additional core
    out = out.append(mean)
# replace missing values with -999
out = out.fillna(value=-999)
out = out[out['Longitude (degE)'] != -999.0]
out.to_csv("slice2.csv",index=False)





if sp == 2:
 data1 = pd.read_csv('slice1.csv')
 data1 = data1[data1['d13C (PDB)'] != -999.0]
 data1 = data1[data1["Taxon_flag"] != 5] 
 data2 = pd.read_csv('slice2.csv')
 data2 = data2[data2['d13C (PDB)'] != -999.0]
 data2 = data2[data2["Taxon_flag"] != 5] 
elif sp == 1:
 data1 = pd.read_csv('slice1.csv')
 data1 = data1[data1['d13C (PDB)'] != -999.0]
 data1 = data1[data1["Taxon_flag"] == 1] 
 data2 = pd.read_csv('slice2.csv')
 data2 = data2[data2['d13C (PDB)'] != -999.0]
 data2 = data2[data2["Taxon_flag"] == 1] 
elif sp == 3:
 data1 = pd.read_csv('slice1.csv')
 data1 = data1[data1['d13C (PDB)'] != -999.0]
 data2 = pd.read_csv('slice2.csv')
 data2 = data2[data2['d13C (PDB)'] != -999.0]


minminlat = max(np.min([np.min(data1['Latitude (degN)']), np.min(data2['Latitude (degN)'])])+5*abs(np.min([np.min(data1['Latitude (degN)']), np.min(data2['Latitude (degN)'])]))/np.min([np.min(data1['Latitude (degN)']), np.min(data2['Latitude (degN)'])]),-90.)
maxmaxlat = min(np.max([np.max(data1['Latitude (degN)']), np.max(data2['Latitude (degN)'])])+5*abs(np.max([np.max(data1['Latitude (degN)']), np.max(data2['Latitude (degN)'])]))/np.max([np.max(data1['Latitude (degN)']), np.max(data2['Latitude (degN)'])]),90.)
minmindepth = np.min([np.min(data1['Site Depth (m)']), np.min(data2['Site Depth (m)'])])
maxmaxdepth = np.max([np.max(data1['Site Depth (m)']), np.max(data2['Site Depth (m)'])])
minmind13c = np.min([np.min(data1['d13C (PDB)']), np.min(data2['d13C (PDB)'])])
maxmaxd13c = np.max([np.max(data1['d13C (PDB)']), np.max(data2['d13C (PDB)'])])

limit0 = min(abs(max(data1['d13C (PDB)'])),abs(min(data1['d13C (PDB)'])))
mlimit0 = limit0*(-1.)


biny = np.arange(-90.,91.,5.)
binx = np.arange(0.,5100.,200.)






fig, ax = plt.subplots(3, 2, sharex=True, sharey=True)
plt.subplots_adjust(wspace=0.29,hspace=0.097)
fig.suptitle('$\delta^{13}$C$\;\;(^{o}/_{oo})$',fontsize=16)

dataa = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 1] 
y=dataa['Latitude (degN)']
x=dataa['Site Depth (m)']
z=dataa['d13C (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
plot=ax[0, 0].pcolormesh(biny,binx,ret.statistic, edgecolors='white',cmap='bwr', vmin=mlimit0, vmax=limit0)
ax[0, 0].set_ylim(5000., 0.)
ax[0, 0].set_xlim(minminlat, maxmaxlat)
ax[0, 0].set_yticks([int(minmindepth/1000.)*1000.,(int(minmindepth/1000.)*1000.+int(maxmaxdepth/1000.)*1000.)/2,int(maxmaxdepth/1000.)*1000.])
ax[0, 0].set_ylabel('Depth (m)',fontsize=15)
ax[0, 0].set_title(str(int(y2/1000)) + '-' + str(int(y1/1000)) + ' ky BP',fontsize=13)
ax[0, 0].text(38, 4700, 'Atlantic', fontsize=11)

datap = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 2] 
y=datap['Latitude (degN)']
x=datap['Site Depth (m)']
z=datap['d13C (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
plot=ax[1, 0].pcolormesh(biny,binx,ret.statistic, edgecolors='white',cmap='bwr', vmin=mlimit0, vmax=limit0)
ax[1, 0].set_ylabel('Depth (m)',fontsize=15)
ax[1, 0].text(38, 4700, 'Pacific', fontsize=11)
aux=pd.concat([x,y,z], axis = 1)
cbar_ax = fig.add_axes([0.471, 0.15, 0.02, 0.7])
cbar_ax.tick_params(labelsize=7)
pcm = ax[1, 0].pcolormesh(aux, cmap='bwr', vmin=mlimit0, vmax=limit0)
fig.colorbar(pcm, cax=cbar_ax,extend="both")

datai = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 3] 
y=datai['Latitude (degN)']
x=datai['Site Depth (m)']
z=datai['d13C (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
plot=ax[2, 0].pcolormesh(biny,binx,ret.statistic, edgecolors='white',cmap='bwr', vmin=mlimit0, vmax=limit0)
ax[2, 0].set_xlabel('Latitude ($^{o}$N)',fontsize=15)
ax[2, 0].set_ylabel('Depth (m)',fontsize=15)
ax[2, 0].text(38, 4700, 'Indian', fontsize=11)


dataa = data1
y=dataa['Latitude (degN)']
x=dataa['Site Depth (m)']
z=dataa['d13C (PDB)']
dataa2 = data2
yy=dataa2['Latitude (degN)']
xx=dataa2['Site Depth (m)']
zz=dataa2['d13C (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
ret2 = stats.binned_statistic_2d(xx, yy, zz, 'mean', bins=[binx, biny])
limit=min(abs(np.nanmax(np.array(ret2.statistic-ret.statistic).ravel())),abs(np.nanmin(np.array(ret2.statistic-ret.statistic).ravel())))
mlimit = limit*(-1.)

dataa = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 1]
y=dataa['Latitude (degN)']
x=dataa['Site Depth (m)']
z=dataa['d13C (PDB)']
dataa2 = data2[data2['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 1]
yy=dataa2['Latitude (degN)']
xx=dataa2['Site Depth (m)']
zz=dataa2['d13C (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
ret2 = stats.binned_statistic_2d(xx, yy, zz, 'mean', bins=[binx, biny])
diff=ret2.statistic-ret.statistic
plot=ax[0, 1].pcolormesh(biny,binx,diff, edgecolors='white',cmap='bwr', vmin=mlimit, vmax=limit)
ax[0, 1].text(38, 4700, 'Atlantic', fontsize=11)
ax[0, 1].set_title(str(int(y4/1000)) + '-' + str(int(y3/1000)) + ' minus ' + str(int(y2/1000)) + '-' + str(int(y1/1000)) + ' ky BP',fontsize=13)

datap = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 2]
y=datap['Latitude (degN)']
x=datap['Site Depth (m)']
z=datap['d13C (PDB)']
datap2 = data2[data2['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 2]
yy=datap2['Latitude (degN)']
xx=datap2['Site Depth (m)']
zz=datap2['d13C (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
ret2 = stats.binned_statistic_2d(xx, yy, zz, 'mean', bins=[binx, biny])
diff=ret2.statistic-ret.statistic
plot=ax[1, 1].pcolormesh(biny,binx,diff, edgecolors='white',cmap='bwr', vmin=mlimit, vmax=limit)
aux=pd.concat([x,y,z], axis = 1)
cbar_ax = fig.add_axes([0.905, 0.15, 0.02, 0.7])
cbar_ax.tick_params(labelsize=7)
pcm = ax[1, 1].pcolormesh(aux, cmap='bwr', vmin=mlimit, vmax=limit)
fig.colorbar(pcm, cax=cbar_ax,extend="both")
ax[1, 1].text(38, 4700, 'Pacific', fontsize=11)

datai = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 3]
y=datai['Latitude (degN)']
x=datai['Site Depth (m)']
z=datai['d13C (PDB)']
datai2 = data2[data2['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 3]
yy=datai2['Latitude (degN)']
xx=datai2['Site Depth (m)']
zz=datai2['d13C (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
ret2 = stats.binned_statistic_2d(xx, yy, zz, 'mean', bins=[binx, biny])
diff=ret2.statistic-ret.statistic
plot=ax[2, 1].pcolormesh(biny,binx,diff, edgecolors='white',cmap='bwr', vmin=mlimit, vmax=limit)
ax[2, 1].set_xlabel('Latitude ($^{o}$N)',fontsize=15)
ax[2, 1].text(38, 4700, 'Indian', fontsize=11)

plt.savefig('Lat-Depth_d13C_' + rann + '.eps', format='eps', dpi=500)








if sp == 2:
 data1 = pd.read_csv('slice1.csv')
 data1 = data1[data1['d18O (PDB)'] > 0.0]
 data1 = data1[data1["Taxon_flag"] != 5] 
 data2 = pd.read_csv('slice2.csv')
 data2 = data2[data2['d18O (PDB)'] > 0.0]
 data2 = data2[data2["Taxon_flag"] != 5] 
elif sp == 1:
 data1 = pd.read_csv('slice1.csv')
 data1 = data1[data1['d18O (PDB)'] > 0.0]
 data1 = data1[data1["Taxon_flag"] == 1] 
 data2 = pd.read_csv('slice2.csv')
 data2 = data2[data2['d18O (PDB)'] > 0.0]
 data2 = data2[data2["Taxon_flag"] == 1] 
elif sp == 3:
 data1 = pd.read_csv('slice1.csv')
 data1 = data1[data1['d18O (PDB)'] > 0.0]
 data2 = pd.read_csv('slice2.csv')
 data2 = data2[data2['d18O (PDB)'] > 0.0]





minminlat = max(np.min([np.min(data1['Latitude (degN)']), np.min(data2['Latitude (degN)'])])+5*abs(np.min([np.min(data1['Latitude (degN)']), np.min(data2['Latitude (degN)'])]))/np.min([np.min(data1['Latitude (degN)']), np.min(data2['Latitude (degN)'])]),-90.)
maxmaxlat = min(np.max([np.max(data1['Latitude (degN)']), np.max(data2['Latitude (degN)'])])+5*abs(np.max([np.max(data1['Latitude (degN)']), np.max(data2['Latitude (degN)'])]))/np.max([np.max(data1['Latitude (degN)']), np.max(data2['Latitude (degN)'])]),90.)
minmindepth = np.min([np.min(data1['Site Depth (m)']), np.min(data2['Site Depth (m)'])])
maxmaxdepth = np.max([np.max(data1['Site Depth (m)']), np.max(data2['Site Depth (m)'])])
minmind18O = np.min([np.min(data1['d18O (PDB)']), np.min(data2['d18O (PDB)'])])
maxmaxd18O = np.max([np.max(data1['d18O (PDB)']), np.max(data2['d18O (PDB)'])])

limit0 = max(data1['d18O (PDB)'])
mlimit0 = min(data1['d18O (PDB)'])

biny = np.arange(-90.,91.,5.)
binx = np.arange(0.,5100.,200.)






fig, ax = plt.subplots(3, 2, sharex=True, sharey=True)
plt.subplots_adjust(wspace=0.29,hspace=0.097)
fig.suptitle('$\delta^{18}$O$\;\;(^{o}/_{oo})$',fontsize=16)

dataa = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 1] 
y=dataa['Latitude (degN)']
x=dataa['Site Depth (m)']
z=dataa['d18O (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
plot=ax[0, 0].pcolormesh(biny,binx,ret.statistic, edgecolors='white',cmap='bwr', vmin=mlimit0, vmax=limit0)
ax[0, 0].set_ylim(5000., 0.)
ax[0, 0].set_xlim(minminlat, maxmaxlat)
ax[0, 0].set_yticks([int(minmindepth/1000.)*1000.,(int(minmindepth/1000.)*1000.+int(maxmaxdepth/1000.)*1000.)/2,int(maxmaxdepth/1000.)*1000.])
ax[0, 0].set_ylabel('Depth (m)',fontsize=15)
ax[0, 0].set_title(str(int(y2/1000)) + '-' + str(int(y1/1000)) + ' ky BP',fontsize=13)
ax[0, 0].text(38, 4700, 'Atlantic', fontsize=11)

datap = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 2] 
y=datap['Latitude (degN)']
x=datap['Site Depth (m)']
z=datap['d18O (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
plot=ax[1, 0].pcolormesh(biny,binx,ret.statistic, edgecolors='white',cmap='bwr', vmin=mlimit0, vmax=limit0)
ax[1, 0].set_ylabel('Depth (m)',fontsize=15)
ax[1, 0].text(38, 4700, 'Pacific', fontsize=11)
aux=pd.concat([x,y,z], axis = 1)
cbar_ax = fig.add_axes([0.471, 0.15, 0.02, 0.7])
cbar_ax.tick_params(labelsize=7)
pcm = ax[1, 0].pcolormesh(aux, cmap='bwr', vmin=mlimit0, vmax=limit0)
fig.colorbar(pcm, cax=cbar_ax,extend="both")

datai = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 3] 
y=datai['Latitude (degN)']
x=datai['Site Depth (m)']
z=datai['d18O (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
plot=ax[2, 0].pcolormesh(biny,binx,ret.statistic, edgecolors='white',cmap='bwr', vmin=mlimit0, vmax=limit0)
ax[2, 0].set_xlabel('Latitude ($^{o}$N)',fontsize=15)
ax[2, 0].set_ylabel('Depth (m)',fontsize=15)
ax[2, 0].text(38, 4700, 'Indian', fontsize=11)


dataa = data1
y=dataa['Latitude (degN)']
x=dataa['Site Depth (m)']
z=dataa['d18O (PDB)']
dataa2 = data2
yy=dataa2['Latitude (degN)']
xx=dataa2['Site Depth (m)']
zz=dataa2['d18O (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
ret2 = stats.binned_statistic_2d(xx, yy, zz, 'mean', bins=[binx, biny])

limit=min(abs(np.nanmax(np.array(ret2.statistic-ret.statistic).ravel())),abs(np.nanmin(np.array(ret2.statistic-ret.statistic).ravel())))
mlimit = limit*(-1.)

dataa = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 1]
y=dataa['Latitude (degN)']
x=dataa['Site Depth (m)']
z=dataa['d18O (PDB)']
dataa2 = data2[data2['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 1]
yy=dataa2['Latitude (degN)']
xx=dataa2['Site Depth (m)']
zz=dataa2['d18O (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
ret2 = stats.binned_statistic_2d(xx, yy, zz, 'mean', bins=[binx, biny])
diff=ret2.statistic-ret.statistic
plot=ax[0, 1].pcolormesh(biny,binx,diff, edgecolors='white',cmap='bwr', vmin=mlimit, vmax=limit)
ax[0, 1].text(38, 4700, 'Atlantic', fontsize=11)
ax[0, 1].set_title(str(int(y4/1000)) + '-' + str(int(y3/1000)) + ' minus ' + str(int(y2/1000)) + '-' + str(int(y1/1000)) + ' ky BP',fontsize=13)

datap = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 2]
y=datap['Latitude (degN)']
x=datap['Site Depth (m)']
z=datap['d18O (PDB)']
datap2 = data2[data2['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 2]
yy=datap2['Latitude (degN)']
xx=datap2['Site Depth (m)']
zz=datap2['d18O (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
ret2 = stats.binned_statistic_2d(xx, yy, zz, 'mean', bins=[binx, biny])
diff=ret2.statistic-ret.statistic
plot=ax[1, 1].pcolormesh(biny,binx,diff, edgecolors='white',cmap='bwr', vmin=mlimit, vmax=limit)
aux=pd.concat([x,y,z], axis = 1)
cbar_ax = fig.add_axes([0.905, 0.15, 0.02, 0.7])
cbar_ax.tick_params(labelsize=7)
pcm = ax[1, 1].pcolormesh(aux, cmap='bwr', vmin=mlimit, vmax=limit)
fig.colorbar(pcm, cax=cbar_ax,extend="both")
ax[1, 1].text(38, 4700, 'Pacific', fontsize=11)

datai = data1[data1['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 3]
y=datai['Latitude (degN)']
x=datai['Site Depth (m)']
z=datai['d18O (PDB)']
datai2 = data2[data2['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] == 3]
yy=datai2['Latitude (degN)']
xx=datai2['Site Depth (m)']
zz=datai2['d18O (PDB)']
ret = stats.binned_statistic_2d(x, y, z, 'mean', bins=[binx, biny])
ret2 = stats.binned_statistic_2d(xx, yy, zz, 'mean', bins=[binx, biny])
diff=ret2.statistic-ret.statistic
plot=ax[2, 1].pcolormesh(biny,binx,diff, edgecolors='white',cmap='bwr', vmin=mlimit, vmax=limit)
ax[2, 1].set_xlabel('Latitude ($^{o}$N)',fontsize=15)
ax[2, 1].text(38, 4700, 'Indian', fontsize=11)

plt.savefig('Lat-Depth_d18O_' + rann + '.eps', format='eps', dpi=500)








