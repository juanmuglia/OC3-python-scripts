from tkinter.filedialog import askdirectory
import os
import pandas as pd
import numpy as np
import glob
from scipy import interpolate

print ("Indicate the place where you have the OC3 folders")
path = askdirectory()


folders = glob.glob(path + "/*") 

header_list=["Latitude (degN)","Longitude (degE)","Site Depth (m)"]
header_list1=["Ocean_flag(1=Atl.;2=Pac.;3=Ind.)"]

colstouse = [1,2,3,4,5,6,7,8,9]


def askforoptions(): 
    correct=False
    num=0
    while(not correct):
        try:
            num = int(input("Write a whole number between 0 and 6:"))
            correct=True
        except ValueError:
            print('Error, write a whole number')     
    return num
 
exit = False
option = 0

while not exit:

  print ("0: exit")
  print ("1: All sites with most recent age models")
  print ("2: Only sites with Peterson and Lisiecki 2018 age models")
  print ("3: Only sites with Waelbroeck et al. 2019 age models")
  print ("4: Only sites with Jonkers et al. 2020 and Repschlaeger et al. 2021 age models")
  print ("5: Only sites with original IntCal20 age models")
  print ("6: Only sites with Waelbroeck et al. 2019 age models (updated to IntCal20)")
  print ("Choose an option") 

  option = askforoptions() 

  if option == 1:
    print ("You chose 1: All sites with most recent age models")
    if not os.path.exists('merged_files_newest'):
     os.makedirs('merged_files_newest')
#For each site folder in the folder that contains them...
    for folder in folders:
#metadata:
      metadata = max(glob.iglob(folder + '/*metadata*.csv'))
      b = pd.read_csv(metadata, low_memory=False)
      sitename = b.iloc[0,2]
#depth_model:
      depthmodel = max(glob.iglob(folder + '/*depth_model.csv'))
      x = pd.read_csv(depthmodel, low_memory=False, usecols=[5]) 
#search for newest_age_model:
#these are all age model files:
      agemodels = glob.glob(folder + '/*age_model_2*.csv')
#this is the newest one, because it has the highest date in  yyymmdd format (that's why we use this format):
      newestagemodel = max(agemodels)
      d = pd.read_csv(newestagemodel, low_memory=False, usecols=[2,3]) 
#search for newest_isotope_data (chosen with the same criterion as the age model): 
      isotopedata = glob.glob(folder + '/*isotope_data_2*.csv')
      newestisotopedata = max(isotopedata)
      e = pd.read_csv(newestisotopedata, low_memory=False, usecols=[3,4,11])
#interpolate the age model depth scale to the depth model of the isotope measurements
      realdepth = x['current_depth_model (m)']
      realdepth_noindex = pd.Series(index=realdepth)
      aage = d
      ageaux = pd.Series(index=aage['age_model_depth (m)'])
      ageaux[:] = aage['age_model (y BP)']
      ageaux.columns = ["age_model (y BP)"]
      mx = np.asarray(realdepth,dtype=np.float64)
      mxp = np.asarray(ageaux.index,dtype=np.float64)
      mfp = np.asarray(ageaux)
      mfp_1d = np.ravel(mfp)
      realdepth_noindex[:] = np.interp(mx,mxp,mfp_1d)
#Include indexes in the interpolated age model: 
      realdepth_index = realdepth_noindex.reset_index() 
      realdepth_index.columns = ["published_archival_depth (m)","age_model (y BP)"]
#put depth age isotope columns together:
      realdepth_index.reset_index(drop=True, inplace=True)
      e.reset_index(drop=True, inplace=True)
      depthageisotope = pd.concat([realdepth_index,e], axis = 1)
#remove lines with repeating numbers in the age model:
      depthageisotope = depthageisotope.loc[realdepth_index['age_model (y BP)'].shift(1) != realdepth_index['age_model (y BP)']]
#create columns for the metadata:	
      a = depthageisotope.reindex(columns = header_list)
#write the metadata in those columns:
      a['Latitude (degN)'] = b.loc[0, "Latitude (degN)"]
      a['Longitude (degE)'] = b.loc[0, "Longitude (degE)"]
      a['Site Depth (m)'] = b.loc[0, "Site Depth (m)"]
#create a column for the ocean flag:
      f = depthageisotope.reindex(columns = header_list1)
      f['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] = b.loc[0, "Ocean"]
      f = f.replace(['Pacific','Atlantic','Indian','Arctic','Mediterranean'],[2,1,3,1,1])
#put all the columns together:
      i = pd.concat([a,depthageisotope,f], axis = 1)
#save (pandas creates an unnecessary index column. We'll erase it later):
      i.to_csv('merged_files_newest/' + sitename + '--newest_merged.csv')
#Do another loop to re-save each file with only the columns we need:
    mergedfiles = glob.glob("merged_files_newest/*.csv") 
    for file_ in mergedfiles:
      g = pd.read_csv(file_, low_memory=False, usecols = colstouse, index_col=1)
      g.to_csv(file_)
  elif option == 2:
    print ("You chose 2: Only sites with Peterson and Lisiecki 2018 age models")
    if not os.path.exists('merged_files_peterson'):
      os.makedirs('merged_files_peterson')
#For each site folder in the folder that contains them...
    for folder in folders:
#search for age model:
      for file in glob.glob(folder + '/*age_model_peterson.csv'):
        agemodel = file
        d = pd.read_csv(agemodel, low_memory=False, usecols=[2,3])
        metadata = max(glob.iglob(folder + '/*metadata*.csv'))
        b = pd.read_csv(metadata, low_memory=False)
        sitename = b.iloc[0,2]
#depth_model:
        depthmodel = max(glob.iglob(folder + '/*depth_model.csv'))
        x = pd.read_csv(depthmodel, low_memory=False, usecols=[5]) 
#isotope data:
        isotopedata = glob.glob(folder + '/*isotope_data_2*.csv')
        newestisotopedata = max(isotopedata)
        e = pd.read_csv(newestisotopedata, low_memory=False, usecols=[3,4,11])
#interpolate the age model depth scale to the depth model of the isotope measurements
        realdepth = x['current_depth_model (m)']
        realdepth_noindex = pd.Series(index=realdepth)
        aage = d
        ageaux = pd.Series(index=aage['age_model_depth (m)'])
        ageaux[:] = aage['age_model (y BP)']
        ageaux.columns = ["age_model (y BP)"]
        mx = np.asarray(realdepth,dtype=np.float64)
        mxp = np.asarray(ageaux.index,dtype=np.float64)
        mfp = np.asarray(ageaux)
        mfp_1d = np.ravel(mfp)
        realdepth_noindex[:] = np.interp(mx,mxp,mfp_1d)
#Include indexes in the interpolated age model: 
        realdepth_index = realdepth_noindex.reset_index() 
        realdepth_index.columns = ["published_archival_depth (m)","age_model (y BP)"]
#put depth age isotope columns together:
        realdepth_index.reset_index(drop=True, inplace=True)
        e.reset_index(drop=True, inplace=True)
        depthageisotope = pd.concat([realdepth_index,e], axis = 1)
#remove lines with repeating numbers in the age model:
        depthageisotope = depthageisotope.loc[realdepth_index['age_model (y BP)'].shift(1) != realdepth_index['age_model (y BP)']]
#create columns for the metadata:	
        a = depthageisotope.reindex(columns = header_list)
#write the metadata in those columns:
        a['Latitude (degN)'] = b.loc[0, "Latitude (degN)"]
        a['Longitude (degE)'] = b.loc[0, "Longitude (degE)"]
        a['Site Depth (m)'] = b.loc[0, "Site Depth (m)"] 
#create a column for the ocean flag:
        f = depthageisotope.reindex(columns = header_list1)
        f['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] = b.loc[0, "Ocean"]
        f = f.replace(['Pacific','Atlantic','Indian','Arctic','Mediterranean'],[2,1,3,1,1])
#put all the columns together:
        i = pd.concat([a,depthageisotope,f], axis = 1)
#save (pandas creates an unnecessary index column. We'll erase it later):
        i.to_csv('merged_files_peterson/' + sitename + '--peterson_merged.csv')
#Do another loop to re-save each file with only the columns we need:
    mergedfiles = glob.glob("merged_files_peterson/*.csv") 
    for file_ in mergedfiles:
      g = pd.read_csv(file_, low_memory=False, usecols = colstouse, index_col=1)
      g.to_csv(file_)
  elif option == 3:
    print ("You chose 3: Only sites with Waelbroeck et al. 2019 age models")
    if not os.path.exists('merged_files_waelbroeck'):
      os.makedirs('merged_files_waelbroeck')
    for folder in folders:
#search for age model:
      for file in glob.glob(folder + '/*age_model_waelbroeck.csv'):
        agemodel = file
        d = pd.read_csv(agemodel, low_memory=False, usecols=[2,3])
        metadata = max(glob.iglob(folder + '/*metadata*.csv'))
        b = pd.read_csv(metadata, low_memory=False)
        sitename = b.iloc[0,2]
#depth_model:
        depthmodel = max(glob.iglob(folder + '/*depth_model.csv'))
        x = pd.read_csv(depthmodel, low_memory=False, usecols=[5]) 
#isotope data:
        isotopedata = glob.glob(folder + '/*isotope_data_2*.csv')
        newestisotopedata = max(isotopedata)
        e = pd.read_csv(newestisotopedata, low_memory=False, usecols=[3,4,11])
#interpolate the age model depth scale to the depth model of the isotope measurements
        realdepth = x['current_depth_model (m)']
        realdepth_noindex = pd.Series(index=realdepth)
        aage = d
        ageaux = pd.Series(index=aage['age_model_depth (m)'])
        ageaux[:] = aage['age_model (y BP)']
        ageaux.columns = ["age_model (y BP)"]
        mx = np.asarray(realdepth,dtype=np.float64)
        mxp = np.asarray(ageaux.index,dtype=np.float64)
        mfp = np.asarray(ageaux)
        mfp_1d = np.ravel(mfp)
        realdepth_noindex[:] = np.interp(mx,mxp,mfp_1d)
#Include indexes in the interpolated age model: 
        realdepth_index = realdepth_noindex.reset_index() 
        realdepth_index.columns = ["published_archival_depth (m)","age_model (y BP)"]
#put depth age isotope columns together:
        realdepth_index.reset_index(drop=True, inplace=True)
        e.reset_index(drop=True, inplace=True)
        depthageisotope = pd.concat([realdepth_index,e], axis = 1)
#remove lines with repeating numbers in the age model:
        depthageisotope = depthageisotope.loc[realdepth_index['age_model (y BP)'].shift(1) != realdepth_index['age_model (y BP)']]
#create columns for the metadata:	
        a = depthageisotope.reindex(columns = header_list)
#write the metadata in those columns:
        a['Latitude (degN)'] = b.loc[0, "Latitude (degN)"]
        a['Longitude (degE)'] = b.loc[0, "Longitude (degE)"]
        a['Site Depth (m)'] = b.loc[0, "Site Depth (m)"] 
#create a column for the ocean flag:
        f = depthageisotope.reindex(columns = header_list1)
        f['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] = b.loc[0, "Ocean"]
        f = f.replace(['Pacific','Atlantic','Indian','Arctic','Mediterranean'],[2,1,3,1,1])
#put all the columns together:
        i = pd.concat([a,depthageisotope,f], axis = 1)
#save (pandas creates an unnecessary index column. We'll erase it later):
        i.to_csv('merged_files_waelbroeck/' + sitename + '--waelbroeck_merged.csv')
#Do another loop to re-save each file with only the columns we need:
    mergedfiles = glob.glob("merged_files_waelbroeck/*.csv") 
    for file_ in mergedfiles:
      g = pd.read_csv(file_, low_memory=False, usecols = colstouse, index_col=1)
      g.to_csv(file_)
  elif option == 4:
    print ("You chose 4: Only sites with Jonkers et al. 2020 or Repschlaeger et al. 2021 age models")
    if not os.path.exists('merged_files_jonkers-repschlaeger'):
      os.makedirs('merged_files_jonkers-repschlaeger')
    for folder in folders:
#search for age model:
     for file in glob.glob(folder + '/*age_model_jonkers.csv') + glob.glob(folder + '/*age_model_repschlaeger.csv'):
        agemodels = glob.glob(folder + '/*age_model_jonkers.csv') + glob.glob(folder + '/*age_model_repschlaeger.csv')
        agemodel = max(agemodels)
        d = pd.read_csv(agemodel, low_memory=False, usecols=[2,3])
        metadata = max(glob.iglob(folder + '/*metadata*.csv'))
        b = pd.read_csv(metadata, low_memory=False)
        sitename = b.iloc[0,2]
#depth_model:
        depthmodels = glob.glob(folder + '/*depth_model*jonkers.csv') + glob.glob(folder + '/*depth_model*repschlaeger.csv') 
        depthmodel = max(depthmodels)
        x = pd.read_csv(depthmodel, low_memory=False, usecols=[5]) 
#isotope data:
        isotopedatas = glob.glob(folder + '/*isotope_data*jonkers.csv') + glob.glob(folder + '/*isotope_data*repschlaeger.csv')
        isotopedata = max(isotopedatas)
        e = pd.read_csv(isotopedata, low_memory=False, usecols=[3,4,11])
#interpolate the age model depth scale to the depth model of the isotope measurements
        realdepth = x['current_depth_model (m)']
        realdepth_noindex = pd.Series(index=realdepth)
        aage = d
        ageaux = pd.Series(index=aage['age_model_depth (m)'])
        ageaux[:] = aage['age_model (y BP)']
        ageaux.columns = ["age_model (y BP)"]
        mx = np.asarray(realdepth,dtype=np.float64)
        mxp = np.asarray(ageaux.index,dtype=np.float64)
        mfp = np.asarray(ageaux)
        mfp_1d = np.ravel(mfp)
        realdepth_noindex[:] = np.interp(mx,mxp,mfp_1d)
#Include indexes in the interpolated age model: 
        realdepth_index = realdepth_noindex.reset_index() 
        realdepth_index.columns = ["published_archival_depth (m)","age_model (y BP)"]
#put depth age isotope columns together:
        realdepth_index.reset_index(drop=True, inplace=True)
        e.reset_index(drop=True, inplace=True)
        depthageisotope = pd.concat([realdepth_index,e], axis = 1)
#remove lines with repeating numbers in the age model:
        depthageisotope = depthageisotope.loc[realdepth_index['age_model (y BP)'].shift(1) != realdepth_index['age_model (y BP)']]
#create columns for the metadata:	
        a = depthageisotope.reindex(columns = header_list)
#write the metadata in those columns:
        a['Latitude (degN)'] = b.loc[0, "Latitude (degN)"]
        a['Longitude (degE)'] = b.loc[0, "Longitude (degE)"]
        a['Site Depth (m)'] = b.loc[0, "Site Depth (m)"] 
#create a column for the ocean flag:
        f = depthageisotope.reindex(columns = header_list1)
        f['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] = b.loc[0, "Ocean"]
        f = f.replace(['Pacific','Atlantic','Indian','Arctic','Mediterranean'],[2,1,3,1,1])
#put all the columns together:
        i = pd.concat([a,depthageisotope,f], axis = 1)
#save (pandas creates an unnecessary index column. We'll erase it later):
        i.to_csv('merged_files_jonkers-repschlaeger/' + sitename + '--jonkers-repschlaeger_merged.csv')
#Do another loop to re-save each file with only the columns we need:
    mergedfiles = glob.glob("merged_files_jonkers-repschlaeger/*.csv") 
    for file_ in mergedfiles:
      g = pd.read_csv(file_, low_memory=False, usecols = colstouse, index_col=1)
      g.to_csv(file_)
  elif option == 5:
    print ("You chose 5: Only sites with original IntCal20 age models")
    if not os.path.exists('merged_files_intcal20'):
     os.makedirs('merged_files_intcal20')
    for folder in folders:
       for file in glob.glob(folder + '/*age_model_mulitza.csv'):
        agemodels = glob.glob(folder + '/*age_model_mulitza.csv')
        agemodel = max(agemodels)
        d = pd.read_csv(agemodel, low_memory=False, usecols=[2,3])
        metadata = max(glob.iglob(folder + '/*metadata*.csv'))
        b = pd.read_csv(metadata, low_memory=False)
        sitename = b.iloc[0,2]
        depthmodels1 = glob.glob(folder + '/*depth_model.csv') + glob.glob(folder + '/*depth_model*jonkers.csv') + glob.glob(folder + '/*depth_model*repschlaeger.csv') + glob.glob(folder + '/*depth_model*mulitza.csv')
        depthmodelsaux = glob.glob(folder + '/*depth_model*mulitza.csv')
        depthmodel= min(depthmodelsaux) if depthmodelsaux else max(depthmodels1)
        x = pd.read_csv(depthmodel, low_memory=False, usecols=[5]) 
#isotope data:
        isotopedatas = glob.glob(folder + '/*isotope_data*jonkers.csv') + glob.glob(folder + '/*isotope_data*repschlaeger.csv') + glob.glob(folder + '/*isotope_data*mulitza.csv')
        isotopedatas1= isotopedatas if isotopedatas else glob.glob(folder + '/*isotope_data*.csv')
        isotopedataaux = glob.glob(folder + '/*isotope_data*mulitza.csv')
        isotopedata= min(isotopedataaux) if isotopedataaux else max(isotopedatas1)
        e = pd.read_csv(isotopedata, low_memory=False, usecols=[3,4,11])
#interpolate the age model depth scale to the depth model of the isotope measurements
        realdepth = x['current_depth_model (m)']
        realdepth_noindex = pd.Series(index=realdepth)
        aage = d
        ageaux = pd.Series(index=aage['age_model_depth (m)'])
        ageaux[:] = aage['age_model (y BP)']
        ageaux.columns = ["age_model (y BP)"]
        mx = np.asarray(realdepth,dtype=np.float64)
        mxp = np.asarray(ageaux.index,dtype=np.float64)
        mfp = np.asarray(ageaux)
        mfp_1d = np.ravel(mfp)
        realdepth_noindex[:] = np.interp(mx,mxp,mfp_1d)
#Include indexes in the interpolated age model: 
        realdepth_index = realdepth_noindex.reset_index() 
        realdepth_index.columns = ["published_archival_depth (m)","age_model (y BP)"]
#put depth age isotope columns together:
        realdepth_index.reset_index(drop=True, inplace=True)
        e.reset_index(drop=True, inplace=True)
        depthageisotope = pd.concat([realdepth_index,e], axis = 1)
#remove lines with repeating numbers in the age model:
        depthageisotope = depthageisotope.loc[realdepth_index['age_model (y BP)'].shift(1) != realdepth_index['age_model (y BP)']]
#create columns for the metadata:	
        a = depthageisotope.reindex(columns = header_list)
#write the metadata in those columns:
        a['Latitude (degN)'] = b.loc[0, "Latitude (degN)"]
        a['Longitude (degE)'] = b.loc[0, "Longitude (degE)"]
        a['Site Depth (m)'] = b.loc[0, "Site Depth (m)"] 
#create a column for the ocean flag:
        f = depthageisotope.reindex(columns = header_list1)
        f['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] = b.loc[0, "Ocean"]
        f = f.replace(['Pacific','Atlantic','Indian','Arctic','Mediterranean'],[2,1,3,1,1])
#put all the columns together:
        i = pd.concat([a,depthageisotope,f], axis = 1)
#save (pandas creates an unnecessary index column. We'll erase it later):
        i.to_csv('merged_files_intcal20/' + sitename + '--intcal20_merged.csv')
    mergedfiles = glob.glob("merged_files_intcal20/*.csv") 
    for file_ in mergedfiles:
      g = pd.read_csv(file_, low_memory=False, usecols = colstouse, index_col=1)
      g.to_csv(file_)
  elif option == 6:
    print ("You chose 3: Only sites with Waelbroeck et al. 2019 age models (updated to IntCal20)")
    if not os.path.exists('merged_files_waelbroeck-intcal20'):
     os.makedirs('merged_files_waelbroeck-intcal20')
    for folder in folders:
#search for age model:
      for file in glob.glob(folder + '/*age_model_waelbroeck-updated2022.csv'): 
        agemodel = file
        d = pd.read_csv(agemodel, low_memory=False, usecols=[2,3])
        metadata = max(glob.iglob(folder + '/*metadata*.csv'))
        b = pd.read_csv(metadata, low_memory=False)
        sitename = b.iloc[0,2]
#depth_model:
        depthmodel = max(glob.iglob(folder + '/*depth_model.csv'))
        x = pd.read_csv(depthmodel, low_memory=False, usecols=[5]) 
#isotope data:
        isotopedata = glob.glob(folder + '/*isotope_data_2*.csv')
        newestisotopedata = max(isotopedata)
        e = pd.read_csv(newestisotopedata, low_memory=False, usecols=[3,4,11])
#interpolate the age model depth scale to the depth model of the isotope measurements
        realdepth = x['current_depth_model (m)']
        realdepth_noindex = pd.Series(index=realdepth)
        aage = d
        ageaux = pd.Series(index=aage['age_model_depth (m)'])
        ageaux[:] = aage['age_model (y BP)']
        ageaux.columns = ["age_model (y BP)"]
        mx = np.asarray(realdepth,dtype=np.float64)
        mxp = np.asarray(ageaux.index,dtype=np.float64)
        mfp = np.asarray(ageaux)
        mfp_1d = np.ravel(mfp)
        realdepth_noindex[:] = np.interp(mx,mxp,mfp_1d)
#Include indexes in the interpolated age model: 
        realdepth_index = realdepth_noindex.reset_index() 
        realdepth_index.columns = ["published_archival_depth (m)","age_model (y BP)"]
#put depth age isotope columns together:
        realdepth_index.reset_index(drop=True, inplace=True)
        e.reset_index(drop=True, inplace=True)
        depthageisotope = pd.concat([realdepth_index,e], axis = 1)
#remove lines with repeating numbers in the age model:
        depthageisotope = depthageisotope.loc[realdepth_index['age_model (y BP)'].shift(1) != realdepth_index['age_model (y BP)']]
#create columns for the metadata:	
        a = depthageisotope.reindex(columns = header_list)
#write the metadata in those columns:
        a['Latitude (degN)'] = b.loc[0, "Latitude (degN)"]
        a['Longitude (degE)'] = b.loc[0, "Longitude (degE)"]
        a['Site Depth (m)'] = b.loc[0, "Site Depth (m)"] 
#create a column for the ocean flag:
        f = depthageisotope.reindex(columns = header_list1)
        f['Ocean_flag(1=Atl.;2=Pac.;3=Ind.)'] = b.loc[0, "Ocean"]
        f = f.replace(['Pacific','Atlantic','Indian','Arctic','Mediterranean'],[2,1,3,1,1])
#put all the columns together:
        i = pd.concat([a,depthageisotope,f], axis = 1)
#save (pandas creates an unnecessary index column. We'll erase it later):
        i.to_csv('merged_files_waelbroeck-intcal20/' + sitename + '--waelbroeck-intcal20_merged.csv')
#Do another loop to re-save each file with only the columns we need:
    mergedfiles = glob.glob("merged_files_waelbroeck-intcal20/*.csv") 
    for file_ in mergedfiles:
      g = pd.read_csv(file_, low_memory=False, usecols = colstouse, index_col=1)
      g.to_csv(file_)
  elif option == 0:
    print ("Exiting")
    exit = True
  else:
    print ("choose a number between 0 and 5") 
print ("End")

