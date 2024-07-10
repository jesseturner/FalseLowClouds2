#---NLCT (11-3.9um BTD) visualized
#---Can visualize the daily NLCT, or the longterm average. Data is accessed from Amazon Web Solutions.

# %%
#---Cloud search libraries
import s3fs
import requests
import fnmatch

#---Data libraries
import xarray as xr
import netCDF4
import numpy as np
import datetime

#---Plotting libraries
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#---Import satellite data functions
import satellite_data_functions
# %%
#---Hooking up the AWS S3 buckets:
fs = s3fs.S3FileSystem(anon=True)
# %%
#---Set the datetime range of interest:
year = 2023
month = 7
month_name = 'Jul'
day_start = 1
day_end = 2
hour = 6
# %%
#---Getting GOES-16 radiance data:
bucket = 'noaa-goes16'
product = 'ABI-L1b-RadF'
# %%
#---Gathering a month of top-of-the-hour data from ABI band 07 and band 14:
range(day_end-(day_start-1))
# %%
b07_data = []
b14_data = []
day = day_start

for i in range(day_end-(day_start-1)):
    julian = datetime.datetime(year, month, day).strftime('%j')
    data_path = bucket + '/' + product + '/'  + str(year) + '/' + str(julian).zfill(3) + '/' + str(hour).zfill(2)
    files = fs.ls(data_path)
    
    files_b07 = [file for file in files if fnmatch.fnmatchcase(file.split('/')[-1], "OR_ABI-L1b-RadF-M6C07".zfill(2)+"*")]
    files_b14 = [file for file in files if fnmatch.fnmatchcase(file.split('/')[-1], "OR_ABI-L1b-RadF-M6C14".zfill(2)+"*")]

    #---index of 0 to get top-of-the-hour
    b07_data.append(files_b07[0])
    b14_data.append(files_b14[0])

    day = day+1
# %%
b07_data

# %%
#---Setting the lat/lon range of the imagery:

#--- Georges Bank
min_lon = -71.5
min_lat = 37
max_lon = -64
max_lat = 42.5

#---Gulf Stream
# min_lon = -77
# min_lat = 33
# max_lon = -50
# max_lat = 45

#--- Oaxaca
# min_lon = -109
# min_lat = 10
# max_lon = -81
# max_lat = 24

lats = (min_lat, max_lat)
lons = (min_lon, max_lon)

# %%
#---Single day NLCT: Choose date from list, accessing from AWS, then processing to create the BTD:
date_index = 0

resp = requests.get(f'https://'+bucket+'.s3.amazonaws.com/'+b07_data[date_index][12:])
if str(resp) != '<Response [200]>':
    print('b07 file not found in AWS servers')

nc_07 = netCDF4.Dataset(b07_data[date_index], memory = resp.content)
ds_07 = xr.open_dataset(xr.backends.NetCDF4DataStore(nc_07))

resp = requests.get(f'https://'+bucket+'.s3.amazonaws.com/'+b14_data[date_index][12:])
if str(resp) != '<Response [200]>':
    print('b14 file not found in AWS servers')

nc_14 = netCDF4.Dataset(b14_data[date_index], memory = resp.content)
ds_14 = xr.open_dataset(xr.backends.NetCDF4DataStore(nc_14))

filename = b07_data[date_index].split('/')[-1]
# %%
BTD = satellite_data_functions.create_BTD(ds_07, ds_14, filename, datetime, lats, lons)
# %%
dt = BTDs[0][0].time.values
date_str = np.datetime_as_string(dt)[:10]
time_str = np.datetime_as_string(dt)[11:16]


projection=ccrs.PlateCarree()
fig,ax=plt.subplots(1, figsize=(12,12),subplot_kw={'projection': projection})
cmap = plt.cm.Greys
levels = np.linspace(0, 3, 21)

c=ax.contourf(BTDs[0][0].lon, BTDs[0][0].lat, BTDs[0][0], cmap=cmap, extend='both', levels=levels)
clb = plt.colorbar(c, shrink=0.6, pad=0.02, ax=ax)
clb.ax.tick_params(labelsize=15)
clb.set_label('BTD (K)', fontsize=15)
ax.set_title('11um - 3.9um BTD ('+date_str +' '+time_str+' UTC)', fontsize=20)

ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)

#plt.savefig("sample_images/nlct_"+date_str[0:4]+date_str[5:7]+date_str[8:10]+"_"+time_str[0:2], bbox_inches='tight')
fig.show()
# %%
#---Make list of BTDs over multiple days
BTDs = []

for i in range(len(b07_data)):

    resp = requests.get(f'https://'+bucket+'.s3.amazonaws.com/'+b07_data[i][12:])
    if str(resp) != '<Response [200]>':
        print('b07 file not found in AWS servers')

    nc_07 = netCDF4.Dataset(b07_data[i], memory = resp.content)
    ds_07 = xr.open_dataset(xr.backends.NetCDF4DataStore(nc_07))

    resp = requests.get(f'https://'+bucket+'.s3.amazonaws.com/'+b14_data[i][12:])
    if str(resp) != '<Response [200]>':
        print('b14 file not found in AWS servers')

    nc_14 = netCDF4.Dataset(b14_data[i], memory = resp.content)
    ds_14 = xr.open_dataset(xr.backends.NetCDF4DataStore(nc_14))

    filename = b07_data[i].split('/')[-1]

    BTD = satellite_data_functions.create_BTD(ds_07, ds_14, filename, datetime, lats, lons)
    BTDs.append(BTD)

# %%
#---Create the static features
static_features = 0
sum_BTD = 0
for i in range(len(BTDs)):
    BTD_positive = BTDs[i].where(BTDs[i]>0,0)
    sum_BTD += BTD_positive[0]
    static_features = (sum_BTD/len(BTDs))
np.shape(static_features)

# %%
#---Plot the static features
dt_start = BTDs[0].time.values[0]
dt_end = BTDs[len(BTDs)-1].time.values[0]
date_str_start = np.datetime_as_string(dt_start)[:10]
date_str_end = np.datetime_as_string(dt_end)[:10]
time_str = np.datetime_as_string(dt_start)[11:16]


projection=ccrs.PlateCarree()
fig,ax=plt.subplots(1, figsize=(12,12),subplot_kw={'projection': projection})
cmap = plt.cm.Greys
levels = np.linspace(0, 3, 31)

c=ax.contourf(BTDs[0].lon, BTDs[0].lat, static_features, cmap=cmap, extend='both', levels=levels)
clb = plt.colorbar(c, shrink=0.6, pad=0.02, ax=ax)
clb.ax.tick_params(labelsize=15)
clb.set_label('BTD (K)', fontsize=15)
ax.set_title('Average 11um - 3.9um BTD \n ('+date_str_start +' to '+date_str_end + ', ' + time_str+' UTC)', fontsize=20)

ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)

#plt.savefig("sample_images/nlct_"+date_str[0:4]+date_str[5:7]+date_str[8:10]+"_"+time_str[0:2], bbox_inches='tight')
fig.show()
# %%
