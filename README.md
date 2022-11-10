# OC3-python-scripts
Python scripts to analyze and plots data extracted from the OC3 database of benthic foraminifera d13C and d18O.

The database may be found in https://doi.org/10.5281/zenodo.7234739


The choice of csv format for the OC3 database allows accessibility from a wide variety of 
computer software, and very light computational needs.
In order to facilitate analysis, we have created a number of python programming language scripts that 
perform tasks for users. Because the scripts are equipped with simple user interfaces, no knowledge
of python is required, but they do need a number of python packages to be installed to work. 

The python scripts are included in this github.
They are simultaneously compiled and run by entering, in the command line (Windows systems) or
terminal (UNIX systems), "python scriptname.py", where scriptname refers to the name of the chosen python
script. The minimum python version required is 3.6.
The scripts run locally. In order to retrieve OC3 data, the entire or parts of the OC3 database 
 needs to be downloaded to the local system. 

The scripts provided for analyzing the OC3 database are as follows:


 list_positions.py: This script retrieves the position and site name metadata of a region of interest (defined by
longitude, latitude and depth ranges) and lists them in a single csv file. This allows users to quickly visualize the position
and basin information of all sites in a chosen region. 

* time_series_d13c.py and time_series_d18o.py: These scripts retrieve the data and age models from the OC3 database
location and create time series plots (encapsulated postscript (eps) files) of benthic foraminiferal d13C and d18O, respectively, with all age models available
for each of the sites. The name of the site and the benthic foraminifera species are displayed in the time series images. 
Age model uncertainties are displayed as error bars when available.    

* merge_cores_files_database.py: This script grabs the isotope data from the OC3 location,
and lets the user choose one of the available age models to linearly interpolate to the isotope data's depth-in-core scale. 
Once the age model is chosen, the script generates a folder of merged csv files with position, age, isotope data, and taxon
information for each site. The number of rows of all columns in each generated file is the same, in order to facilitate access 
with any data analysis software. 
The following python scripts included with the database make use of the merged csv files 
generated with this scirpt: 

** list_time_resolution.py: This script lists the number of data points at each site inside a predefined time slice. 
The result is saved in a csv file.

** time_slice.py: This script lets the user define a taxon group 
(emph{Cibicidoides wuellerstorfi}, any emph{Cibicidoides}, or all taxa), a time interval, 
and a region of interest (defined by
longitude, latitude and depth ranges), and calculates
the time mean of the benthic foraminiferal d13C and d18O data for all sites that include data in the defined time interval and region. 
The result is saved in a csv file, and plotted in longitude-latitude, latitude-depth, and
longitude-depth two dimensional scatter plots. The images are saved as eps files.  

** compare_time_slices.py: This script lets the user define a taxon group as in the previous script 
and two time intervals. It plots, in
latitude-depth sections for each basin, the benthic foraminiferal d13C or d18O data from the first time slice (left panels),
and the benthic foraminiferal d13C or d18O difference between the second and first time slices (right panels). 
The images are saved as eps files. In order to calculate the differences and visualize, the scripts bins the data positions
into a regular 5º x 200 m grid. 
