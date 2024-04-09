#%%
import xarray as xr
import numpy as np

#%%
date = "20230919"
dtime = "06z"
min_lon, min_lat, max_lon, max_lat = -77, 33, -50, 45

#%%
data_root = f"../data/{date}/time_{dtime}/"
gfs_file = f"gfs.t{dtime}.pgrb2.0p25.f000"
gfs_ds = xr.open_dataset(data_root+gfs_file, engine="cfgrib", backend_kwargs={'filter_by_keys': {'typeOfLevel':'isobaricInhPa'}})
gfs_ds = gfs_ds.sel(latitude=slice(max_lat,min_lat), longitude=slice(min_lon+360,max_lon+360))
#%%
gfs_ds

#%%
from Visualize import map_data

lon = gfs_ds.longitude
lat = gfs_ds.latitude

data = gfs_ds['q'].sum(dim='isobaricInhPa')
levels = np.linspace(np.nanmin(data), np.nanmax(data), 31)

title = "Humidity Summed for " +date+ " " +dtime
clb_label = "Units"

map_data(lon, lat, data, levels, title, clb_label)
