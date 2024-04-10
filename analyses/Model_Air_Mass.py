#%%
import xarray as xr
import numpy as np

#%%
date = "20230920"
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
lon = gfs_ds.longitude
lat = gfs_ds.latitude

humidity = gfs_ds['q'].sum(dim='isobaricInhPa')
humidity_levels = np.linspace(np.nanmin(humidity), np.nanmax(humidity), 31)

temp_surf = gfs_ds['t'].isel(isobaricInhPa=0)

title = "GFS Model " +date+ " " +dtime
clb_label = "Specific Humidity (kg/kg)"

# %%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# %%
projection = ccrs.PlateCarree()
fig, ax = plt.subplots(1, figsize=(12, 12), subplot_kw={'projection': projection})
cmap = plt.cm.PuBu
q = ax.contourf(lon, lat, humidity, cmap=cmap, extend='both', levels=humidity_levels)
clb = plt.colorbar(q, shrink=0.3, pad=0.02, ax=ax)

t = ax.contour(lon, lat, temp_surf, cmap=plt.cm.coolwarm)
plt.clabel(t, inline=True, fontsize=8)

ax.set_title(title)
clb.set_label(clb_label)
ax.add_feature(cfeature.LAND, zorder=100, color='black', edgecolor='k')
ax.coastlines(resolution='50m', color='black', linewidth=1)
fig.savefig('../figures/gfs_'+date+'.png', dpi = 300, bbox_inches='tight')
fig.show()
# %%
