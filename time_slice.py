from tkinter.filedialog import askdirectory
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as patches
from scipy import signal
from scipy import interpolate
import glob
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
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
  ocean = 0
  lon1=0
  lon2=0
  lat1 = 0
  lat2 = 0
  depth1 = 0
  depth2 = 0
  ocean = 0
  yr1=0
  yr2=0
  print ("Select ocean, averaging window for time slice, and region")
  while(not correct):
    try:
      species = int(input("Enter taxon (1=C. wuellerstorfi; 2=Any Cibs.; 3=All taxa): ")) 
      ocean = int(input("Enter Ocean flag (1=Atl.;2=Pac.;3=Ind.; 4=Ind.-Pac.; 5=Global): ")) 
      yr1 = int(input("Enter start year for time slice: "))
      yr2 = int(input("Enter end year for time slice: "))
      lon1 = (input("Enter western-most longitude (between -180 and 180): "))
      lon2 = (input("Enter eastern-most longitude (between -180 and 180): "))
      lat1 = (input("Enter southern-most latitude (between -90 and 90): "))
      lat2 = (input("Enter northern-most latitude (between -90 and 90): "))
      depth1 = (input("Enter upper depth (in m): "))
      depth2 = (input("Enter lower depth (in m): "))
      correct=True
    except ValueError:
      print('Error, enter whole numbers')
    return species,ocean,yr1,yr2,lon1,lon2, lat1, lat2, depth1, depth2



exit = False
sp,oc,y1,y2,l1,l2,lt1,lt2,d1,d2 = askforinput()




first = True
mergedfiles = glob.glob(path + "*_merged.csv")
if sp == 1:
 if oc < 4:
  for file in mergedfiles:
    data = pd.read_csv(file, usecols=colstouse)
# select ocean
    cwdata = data[data["Taxon_flag"] == 1]
    oceandata = cwdata[cwdata["Ocean_flag(1=Atl.;2=Pac.;3=Ind.)"] == oc]
# select time window
    olddata = oceandata[oceandata["age_model (y BP)"] > y1]
    newdata = olddata[olddata["age_model (y BP)"] < y2]
    eastdata = newdata[newdata["Longitude (degE)"] > int(l1)]
    westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
    northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
    southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
    downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
    mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
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
  out.to_csv("slice.csv",index=False)
  print ("End")
 elif oc == 4:
  for file in mergedfiles:
    data = pd.read_csv(file, usecols=colstouse)
# select ocean
    cwdata = data[data["Taxon_flag"] == 1]
    oceandata = cwdata[cwdata["Ocean_flag(1=Atl.;2=Pac.;3=Ind.)"] > 1]
# select time window
    olddata = oceandata[oceandata["age_model (y BP)"] > y1]
    newdata = olddata[olddata["age_model (y BP)"] < y2]
    eastdata = newdata[newdata["Longitude (degE)"] > int(l1)]
    westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
    northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
    southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
    downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
    mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
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
  out.to_csv("slice.csv",index=False)
  print ("End")
 elif oc == 5:
  for file in mergedfiles:
    data = pd.read_csv(file, usecols=colstouse)
# select ocean
    cwdata = data[data["Taxon_flag"] == 1]
    oceandata = cwdata
# select time window
    olddata = oceandata[oceandata["age_model (y BP)"] > y1]
    newdata = olddata[olddata["age_model (y BP)"] < y2]
    eastdata = newdata[newdata["Longitude (degE)"] > int(l1)]
    westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
    northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
    southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
    downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
    mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
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
  out.to_csv("slice.csv",index=False)
  print ("End")
elif sp == 2:
 if oc < 4:
  for file in mergedfiles:
    data = pd.read_csv(file, usecols=colstouse)
    data["Taxon_flag"] = max(data["Taxon_flag"])
# select ocean
    cdata = data[data["Taxon_flag"] != 5]
    oceandata = cdata[cdata["Ocean_flag(1=Atl.;2=Pac.;3=Ind.)"] == oc]
# select time window
    olddata = oceandata[oceandata["age_model (y BP)"] > y1]
    newdata = olddata[olddata["age_model (y BP)"] < y2]
    eastdata = newdata[newdata["Longitude (degE)"] > int(l1)]
    westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
    northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
    southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
    downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
    mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
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
  out.to_csv("slice.csv",index=False)
  print ("End")
 elif oc == 4:
  for file in mergedfiles:
    data = pd.read_csv(file, usecols=colstouse)
    data["Taxon_flag"] = max(data["Taxon_flag"])
# select ocean
    cdata = data[data["Taxon_flag"] != 5]
    oceandata = cdata[cdata["Ocean_flag(1=Atl.;2=Pac.;3=Ind.)"] > 1]
# select time window
    olddata = oceandata[oceandata["age_model (y BP)"] > y1]
    newdata = olddata[olddata["age_model (y BP)"] < y2]
    eastdata = newdata[newdata["Longitude (degE)"] > int(l1)]
    westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
    northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
    southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
    downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
    mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
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
  out.to_csv("slice.csv",index=False)
  print ("End")
 elif oc == 5:
  for file in mergedfiles:
    data = pd.read_csv(file, usecols=colstouse)
    data["Taxon_flag"] = max(data["Taxon_flag"])
# select ocean
    cdata = data[data["Taxon_flag"] != 5]
    oceandata = cdata
# select time window
    olddata = oceandata[oceandata["age_model (y BP)"] > y1]
    newdata = olddata[olddata["age_model (y BP)"] < y2]
    eastdata = newdata[newdata["Longitude (degE)"] > int(l1)]
    westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
    northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
    southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
    downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
    mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
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
  out.to_csv("slice.csv",index=False)
  print ("End")
elif sp == 3:
 if oc < 4:
  for file in mergedfiles:
    data = pd.read_csv(file, usecols=colstouse)
    data["Taxon_flag"] = max(data["Taxon_flag"])
# select ocean
    cdata = data
    oceandata = cdata[cdata["Ocean_flag(1=Atl.;2=Pac.;3=Ind.)"] == oc]
# select time window
    olddata = oceandata[oceandata["age_model (y BP)"] > y1]
    newdata = olddata[olddata["age_model (y BP)"] < y2]
    eastdata = newdata[newdata["Longitude (degE)"] > int(l1)]
    westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
    northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
    southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
    downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
    mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
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
  out.to_csv("slice.csv",index=False)
  print ("End")
 elif oc == 4:
  for file in mergedfiles:
    data = pd.read_csv(file, usecols=colstouse)
    data["Taxon_flag"] = max(data["Taxon_flag"])
# select ocean
    cdata = data
    oceandata = cdata[cdata["Ocean_flag(1=Atl.;2=Pac.;3=Ind.)"] > 1]
# select time window
    olddata = oceandata[oceandata["age_model (y BP)"] > y1]
    newdata = olddata[olddata["age_model (y BP)"] < y2]
    eastdata = newdata[newdata["Longitude (degE)"] > int(l1)]
    westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
    northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
    southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
    downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
    mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
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
  out.to_csv("slice.csv",index=False)
  print ("End")
 elif oc == 5:
  for file in mergedfiles:
    data = pd.read_csv(file, usecols=colstouse)
    data["Taxon_flag"] = max(data["Taxon_flag"])
# select ocean
    cdata = data
    oceandata = cdata
# select time window
    olddata = oceandata[oceandata["age_model (y BP)"] > y1]
    newdata = olddata[olddata["age_model (y BP)"] < y2]
    eastdata = newdata[newdata["Longitude (degE)"] > int(l1)]
    westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
    northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
    southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
    downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
    mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
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
  out.to_csv("slice.csv",index=False)
#  print ("End")


data = pd.read_csv('slice.csv')
data = data[data['d13C (VPDB)'] != -999.0]
ocean = data['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)']
 
x=data['Longitude (degE)']
y=data['Latitude (degN)']
z=data['d13C (VPDB)']
lat = y
fig = plt.figure(figsize=(13,5))
if min(ocean) == 1.:
 lon = x
 ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=0)) 
else:
 lon = x-180.
 ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=180))
ax.scatter(lon, lat)
ax.stock_img()
ax.coastlines()
ax.gridlines(draw_labels=True)
plt.scatter(lon,y,edgecolors='none',s=50,c=z,cmap='Reds')
plt.colorbar()
plt.title('$\delta^{13}$C$\;\;(^{o}/_{oo})$',fontsize=15)
plt.ylabel('Latitude ($^{o}$N)',fontsize=15)
plt.xlabel('Longitude ($^{o}$E)',fontsize=15)
plt.savefig('Lon-Lat_d13C_' + rann + '.eps', format='eps', dpi=500)
x=data['Longitude (degE)']
y=data['Site Depth (m)']
z=data['d13C (VPDB)']
fig = plt.figure()
plt.scatter(x,y,edgecolors='none',s=50,c=z,cmap='Reds')
plt.ylim(max(y)+200., min(y)+200.)
plt.colorbar()
plt.title('$\delta^{13}$C$\;\;(^{o}/_{oo})$',fontsize=15)
plt.ylabel('Depth (m)',fontsize=15)
plt.xlabel('Longitude ($^{o}$E)',fontsize=15)
plt.savefig('Lon-Depth_d13C_' + rann + '.eps', format='eps', dpi=500)
x=data['Latitude (degN)']
y=data['Site Depth (m)']
z=data['d13C (VPDB)']
fig = plt.figure()
plt.scatter(x,y,edgecolors='none',s=50,c=z,cmap='Reds')
plt.ylim(max(y)+200., min(y)+200.)
plt.colorbar()
plt.title('$\delta^{13}$C$\;\;(^{o}/_{oo})$',fontsize=15)
plt.ylabel('Depth (m)',fontsize=15)
plt.xlabel('Latitude ($^{o}$N)',fontsize=15)
plt.savefig('Lat-Depth_d13C_' + rann + '.eps', format='eps', dpi=500)

data = pd.read_csv('slice.csv')
data = data[data['d18O (VPDB)'] != -999.0]
ocean = data['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)']
 
x=data['Longitude (degE)']
y=data['Latitude (degN)']
z=data['d18O (VPDB)']
lat = y
fig = plt.figure(figsize=(13,5))
if min(ocean) == 1.:
 lon = x
 ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=0)) 
else:
 lon = x-180.
 ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=180))
ax.scatter(lon, lat)
ax.stock_img()
ax.coastlines()
ax.gridlines(draw_labels=True)
plt.scatter(lon,y,edgecolors='none',s=50,c=z,cmap='Reds')
plt.colorbar()
plt.title('$\delta^{18}$O$\;\;(^{o}/_{oo})$',fontsize=15)
plt.ylabel('Latitude ($^{o}$N)',fontsize=15)
plt.xlabel('Longitude ($^{o}$E)',fontsize=15)
plt.savefig('Lon-Lat_d18O_' + rann + '.eps', format='eps', dpi=500)
x=data['Longitude (degE)']
y=data['Site Depth (m)']
z=data['d18O (VPDB)']
fig = plt.figure()
plt.scatter(x,y,edgecolors='none',s=50,c=z,cmap='Reds')
plt.ylim(max(y)+200., min(y)+200.)
plt.colorbar()
plt.title('$\delta^{18}$O$\;\;(^{o}/_{oo})$',fontsize=15)
plt.ylabel('Depth (m)',fontsize=15)
plt.xlabel('Longitude ($^{o}$E)',fontsize=15)
plt.savefig('Lon-Depth_d18O_' + rann + '.eps', format='eps', dpi=500)
x=data['Latitude (degN)']
y=data['Site Depth (m)']
z=data['d18O (VPDB)']
fig = plt.figure()
plt.scatter(x,y,edgecolors='none',s=50,c=z,cmap='Reds')
plt.ylim(max(y)+200., min(y)+200.)
plt.colorbar()
plt.title('$\delta^{18}$O$\;\;(^{o}/_{oo})$',fontsize=15)
plt.ylabel('Depth (m)',fontsize=15)
plt.xlabel('Latitude ($^{o}$N)',fontsize=15)
plt.savefig('Lat-Depth_d18O_' + rann + '.eps', format='eps', dpi=500)


os.rename("slice.csv", "slice" + rann + ".csv")
print ("Created six plots and a csv file. End")









