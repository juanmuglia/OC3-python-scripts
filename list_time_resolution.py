from tkinter.filedialog import askdirectory
import numpy as np
import pandas as pd
import glob
import os



#path to folder with *_merged.csv files (after running merged_cores_files.py):
print ("Indicate a folder where you have OC3 merged files created with 'merge_cores_files_database.py'")
path0 = askdirectory()

path = path0 + "/"

colstouse = [0,1,2,4,5,6,7,8]




def askforinput(): 
  correct=False
  yr1=0
  yr2=0
  print ("Select ocean, averaging window for time slice, and region")
  while(not correct):
    try:
      yr1 = int(input("Enter start year for time slice: "))
      yr2 = int(input("Enter end year for time slice: "))
      correct=True
    except ValueError:
      print('Error, enter whole numbers')
    return yr1,yr2



exit = False
y1,y2 = askforinput()



sy1=str(y1)
sy2=str(y2)


line=[('Site','Ocean_flag(1=Atl.;2=Pac.;3=Ind.)','Longitude (degE)','Latitude (degN)','Site Depth (m)','Taxon_flag','Number of points in ' + sy1 + '-' + sy2 + ' timeslice')]
output = pd.DataFrame(line)
output.to_csv("sites_Ndatapoints_" + sy1 + "-" + sy2 + ".csv", mode='a', header=False,index=False)



first = True
mergedfiles = glob.glob(path + "*_merged.csv")
for file in mergedfiles:
    name0 = file.split("/")[-1]
    name = name0.split("_new")[0]
    data = pd.read_csv(file, usecols=colstouse)
    taxon = np.array(data.iloc[0,6])
    taxonlist = taxon.tolist() 
    ocean = np.array(data.iloc[0,7])
    oceanlist = ocean.tolist()       
# select time window
    olddata = data[data["age_model (y BP)"] > y1]
    mydata = olddata[olddata["age_model (y BP)"] < y2]
    line=[(name,oceanlist,data.iloc[0,0],data.iloc[0,1],data.iloc[0,2],taxonlist,len(mydata))]
    output = pd.DataFrame(line)
    output.to_csv("sites_Ndatapoints_" + sy1 + "-" + sy2 + ".csv", mode='a', index=False, header=False)
    
