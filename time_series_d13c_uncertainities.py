from tkinter.filedialog import askdirectory
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as patches
from scipy import signal
from scipy import interpolate
import glob
import os

print ("Indicate the place where you have the OC3 folders")
path = askdirectory()



folders = glob.glob(path + "/*") 

if not os.path.exists('plots_d13c_errorbars'):
    os.makedirs('plots_d13c_errorbars')

df_dict = dict()

colors=['blue','green','red','gold','gray','deeppink']
ecolors=['lightsteelblue','lightgreen','lightcoral','wheat','silver','lightpink']

for folder in folders:
#metadata:
      metadata = max(glob.iglob(folder + '/*metadata*.csv'))
      b = pd.read_csv(metadata, low_memory=False)
      sitename = b.iloc[0,2]
#depth_model:
      depthmodel = max(glob.iglob(folder + '/*depth_model.csv'))
      x = pd.read_csv(depthmodel, low_memory=False, usecols=[5]) 
      realdepth = x['current_depth_model (m)']
      realdepth_noindex = pd.Series(index=realdepth)
#search for newest_isotope_data (chosen with the same criterion as the age model): 
      isotopedata = glob.glob(folder + '/*isotope_data_2*.csv')
      newestisotopedata = max(isotopedata)
      e = pd.read_csv(newestisotopedata, low_memory=False, usecols=[3,4,10,11])
      if len(e) > 1 & e['d13C (PDB)'].isnull().all()==0.00:
       taxon = e.iloc[0,2]
#search for newest_age_model:
#these are all age model files:
       agemodels = glob.glob(folder + '/*age_model_2*.csv')
#this is the newest one, because it has the highest date in  yyymmdd format (that's why we use this format):
       counter = 0
       for file_name in agemodels:  # loop over files
        df_dict[file_name] = pd.read_csv(file_name)
        d = df_dict[file_name]
        eplus=d.iloc[:,[4,6]].min(axis=1)
        eminus=d.iloc[:,[5,7]].max(axis=1)
        agemodelnote = d.iloc[0,9]
        aage = pd.concat([d['age_model_depth (m)'],d['age_model (y BP)'],eplus,eminus], axis = 1)
        aage.columns = ['age_model_depth (m)','age_model (y BP)','errorplus','errorminus']
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
#do  everything again but for the uncertainities:
        errorplusaux = pd.Series(index=aage['age_model_depth (m)'])
        errorplusaux[:] = aage['errorplus']
        errorplusaux.columns = ["errorplus"]
        mxp = np.asarray(errorplusaux.index,dtype=np.float64)
        mfp = np.asarray(errorplusaux)
        mfp_1d = np.ravel(mfp)
        realdepth_noindex[:] = np.interp(mx,mxp,mfp_1d)
#Include indexes in the interpolated age model: 
        errorplus_index = realdepth_noindex.reset_index() 
        errorplus_index.columns = ["published_archival_depth (m)","errorplus"]
#put depth age isotope columns together:
        errorplus_index.reset_index(drop=True, inplace=True)
        errorminusaux = pd.Series(index=aage['age_model_depth (m)'])
        errorminusaux[:] = aage['errorminus']
        errorminusaux.columns = ["errorminus"]
        mxp = np.asarray(errorminusaux.index,dtype=np.float64)
        mfp = np.asarray(errorminusaux)
        mfp_1d = np.ravel(mfp)
        realdepth_noindex[:] = np.interp(mx,mxp,mfp_1d)
#Include indexes in the interpolated age model: 
        errorminus_index = realdepth_noindex.reset_index() 
        errorminus_index.columns = ["published_archival_depth (m)","errorminus"]
#put depth age isotope columns together:
        errorminus_index.reset_index(drop=True, inplace=True)
        e.reset_index(drop=True, inplace=True)
        depthageisotope0 = pd.concat([realdepth_index,errorplus_index,errorminus_index,e], axis = 1)
        depthageisotope = depthageisotope0.drop(depthageisotope0.columns[[2, 4]],axis = 1)
#remove lines with repeating numbers in the age model:
        depthageisotope = depthageisotope.loc[realdepth_index['age_model (y BP)'].shift(1) != realdepth_index['age_model (y BP)']]
        depthageisotope = depthageisotope[depthageisotope['d13C (PDB)'].notna()]
        d13c = depthageisotope['d13C (PDB)']
        age = depthageisotope['age_model (y BP)']
        agep = abs(age-depthageisotope['errorplus'])
        agem = abs(age-depthageisotope['errorminus'])
        asymmetric_error = [agem, agep]
        plt.plot(figsize=(4.8,1.8))
        plt.plot(age,d13c,label=agemodelnote, marker="o",ms=5,color = colors[counter])
        plt.errorbar(age,d13c, xerr = asymmetric_error, fmt = 'o',ecolor = colors[counter], elinewidth = 2, capsize=3, ms=0.000001, alpha=0.5)
        plt.legend()
        plt.tick_params(which='major', labelsize=8, labelbottom=True)
        plt.xlabel('time (y BP)',fontsize=15)
        plt.ylabel('$\delta^{13}C\;\;(^o/_{oo})$',fontsize=15)
        plt.xlim([max(10000,min(age)),min(23000,max(age))])
        plt.ylim([min(d13c)-0.2,max(d13c)+0.2])       
        plt.title(sitename + ',  ' + taxon,fontsize=14)
        plt.savefig('plots_d13c_errorbars/' + sitename + '.pdf', format='pdf', dpi=5000)
        counter = counter+1
       plt.plot().clear()
       plt.close()
       plt.cla()
       plt.clf()




