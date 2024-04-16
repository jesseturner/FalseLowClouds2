#%%
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np

#%%
data_root = "../data/"
#--- Select the data date and time
date = "20230920"
time = "06z"

#%%
#--- Load the model data
gfs_file = data_root+date+"/gfs.t"+time+".pgrb2.0p25.f000"
gfs_ds = xr.open_dataset(gfs_file, engine="cfgrib", backend_kwargs={'filter_by_keys': {'typeOfLevel':'isobaricInhPa'}})
# %%
#--- Load the SST data
sst_file = data_root+date+"/oisst-avhrr-v02r01."+date+".nc"

sst_ds = xr.open_dataset(sst_file)
sst_ds =  sst_ds.squeeze()
sst_ds.sst.values = sst_ds.sst.values+273.15

# %%
#--- Filter the dataset to the region of interest

#---Gulf Stream
min_lon = -77
min_lat = 33
max_lon = -50
max_lat = 45
# %%
#--- Slice the model and SST data to the selected region
sst_ds = sst_ds.sel(lat=slice(min_lat,max_lat), lon=slice(min_lon+360,max_lon+360))
#------ GFS data latitude is reversed compared to the SST data, this flips it into position.
gfs_ds = gfs_ds.sel(latitude=slice(None, None, -1))
gfs_ds = gfs_ds.sel(latitude=slice(min_lat,max_lat), longitude=slice(min_lon+360,max_lon+360))

# %%
#--- Identify the indices where the maximum humidity occurs for each height level
max_humidity_indices = gfs_ds['q'].argmax(dim='isobaricInhPa')
# %%
max_humidity_heights = gfs_ds['isobaricInhPa'].isel(isobaricInhPa=max_humidity_indices).values
# %%
#--- Visualize the max humidity indices/heights
projection=ccrs.PlateCarree()
fig,ax=plt.subplots(1, figsize=(12,12),subplot_kw={'projection': projection})
cmap = plt.cm.RdBu
#levels = np.linspace(np.nanmin(max_humidity_heights), np.nanmax(max_humidity_heights), 31)
levels = np.linspace(900, 1000, 11)

c=ax.contourf(max_humidity_indices.longitude, max_humidity_indices.latitude, max_humidity_heights, cmap=cmap, extend='both', levels=levels)
clb=plt.colorbar(c, shrink=0.3, pad=0.02, ax=ax)
ax.set_title('Max humidity heights ('+date+' '+ time+')')
clb.set_label('Pressure (hPa)')
clb.ax.invert_yaxis()

ax.add_feature(cfeature.LAND, zorder=100, color='black', edgecolor='k')
ax.coastlines(resolution='50m', color='black', linewidth=1)
#fig.savefig('../figures/max_humidity_heights_'+date+'.png', dpi = 300, bbox_inches='tight')
fig.show()
# %%

# %%
