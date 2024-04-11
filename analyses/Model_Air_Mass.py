#%%
import xarray as xr
import numpy as np

#%%
date = "20230919"
dtime = "06z"
min_lon, min_lat, max_lon, max_lat = -77, 33, -50, 45

#%%
#--- Loading the model data
data_root = f"../data/{date}/"
gfs_file = f"gfs.t{dtime}.pgrb2.0p25.f000"
gfs_ds = xr.open_dataset(data_root+gfs_file, engine="cfgrib", backend_kwargs={'filter_by_keys': {'typeOfLevel':'isobaricInhPa'}})
gfs_ds = gfs_ds.sel(latitude=slice(max_lat,min_lat), longitude=slice(min_lon+360,max_lon+360))
#%%
gfs_ds

#%%
#--- Creating the figure variables
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
#--- Figure with humidity and temperature contours
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
#--- Selecting a point to get profile
selected_point_lon = 295
selected_point_lat = 39

s_p_profile = gfs_ds.sel(latitude=selected_point_lat, longitude=selected_point_lon, method='nearest')

# %% 
#--- Figure for the selected point profiles

projection = ccrs.PlateCarree()
fig, ax = plt.subplots(1, figsize=(12, 12), subplot_kw={'projection': projection})

#------ Map model location
cmap = plt.cm.PuBu
q = ax.contourf(lon, lat, humidity, cmap=cmap, extend='both', levels=humidity_levels)
clb = plt.colorbar(q, shrink=0.3, pad=0.02, ax=ax)

t = ax.contour(lon, lat, temp_surf, cmap=plt.cm.coolwarm)
plt.clabel(t, inline=True, fontsize=8)

s_p = ax.scatter(selected_point_lon, selected_point_lat, s=30, c='red', edgecolor='white')

ax.set_title(title)
clb.set_label(clb_label)
ax.add_feature(cfeature.LAND, zorder=100, color='black', edgecolor='k')
ax.coastlines(resolution='50m', color='black', linewidth=1)

fig.show()

# %%
#--- Figure for the selected point profiles
fig, ax_temp = plt.subplots(figsize=(6, 6))
ax_hum = ax_temp.twiny()  # Create a twin axes sharing the same y-axis

# Plot temperature profile
ax_temp.plot(s_p_profile['t'].values, s_p_profile['isobaricInhPa'].values, c="red", linewidth=3, label='Temperature')
ax_temp.set_xlabel('Temperature (°C)')
ax_temp.set_ylabel('Pressure Height')
ax_temp.invert_yaxis()

# Plot humidity profile
ax_hum.plot(s_p_profile['q'].values, s_p_profile['isobaricInhPa'].values, c="blue", linewidth=3, label='Humidity')
ax_hum.set_xlabel('Specific Humidity (kg/kg)')

# Set title and grid
ax_temp.set_title('Atmospheric Profile')
ax_temp.grid(True)
ax_temp.legend()
plt.show()
# %%
