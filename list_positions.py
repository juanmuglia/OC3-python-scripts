from tkinter.filedialog import askdirectory
import pandas as pd
import numpy as np
import glob
import os

if os.path.exists('OC3_sites_positions.csv'):
    print("Removing existing OC3_sites_positions.csv file")
    os.remove('OC3_sites_positions.csv')
else:
    print("Creating OC3_sites_positions.csv file")


print ("Indicate the place where you have the OC3 folders")
path = askdirectory()
folders = glob.glob(path + "/*") 
cols = [2,3,4,5,0]


def askforinput(): 
  correct=False
  lon1=0
  lon2=0
  lat1 = 0
  lat2 = 0
  depth1 = 0
  depth2 = 0
  print ("Select position range")
  while(not correct):
    try:
      lon1 = (input("Enter western-most longitude (between -180 and 180): "))
      lon2 = (input("Enter eastern-most longitude (between -180 and 180): "))
      lat1 = (input("Enter southern-most latitude (between -90 and 90): "))
      lat2 = (input("Enter northern-most latitude (between -90 and 90): "))
      depth1 = (input("Enter upper depth (in m): "))
      depth2 = (input("Enter lower depth (in m): "))
      correct=True
    except ValueError:
      print('Error, enter whole numbers')
    return lon1,lon2, lat1, lat2, depth1, depth2


exit = False
l1,l2,lt1,lt2,d1,d2 = askforinput()
first = True
folders = glob.glob(path + "/*") 
for folder in folders:
  metadata = max(glob.iglob(folder + '/*metadata*.csv'))
  b = pd.read_csv(metadata, low_memory=False, usecols=cols, index_col=0)
  eastdata = b[b["Longitude (degE)"] > int(l1)]
  westdata = eastdata[eastdata["Longitude (degE)"] < int(l2)]
  northdata = westdata[westdata["Latitude (degN)"] > int(lt1)]
  southdata = northdata[northdata["Latitude (degN)"] < int(lt2)]
  downdata = southdata[southdata["Site Depth (m)"] > int(d1)]
  mydata = downdata[downdata["Site Depth (m)"] < int(d2)]
  mydata.to_csv('OC3_sites_positions.csv', mode='a',header=False)


string = 'Ocean,Site,Latitude (degN),Longitude (degE),Site Depth (m)\n'

with open('OC3_sites_positions.csv', 'r+') as file:
   content = file.read()
   file.seek(0)
   file.write(string + content)




