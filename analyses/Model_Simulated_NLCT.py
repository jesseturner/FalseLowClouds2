import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
#import cartopy.crs as ccrs
import cartopy.feature as cfeature
from Download_Model_Data import download_data

# Function to create BTD
def create_btd(date, dtime):
    data_root = f"data/{date}/time_{dtime}/"
    gfs_file = f"gfs.t{dtime}.pgrb2.0p25.f000"
    sst_file = f"oisst-avhrr-v02r01.{date}.nc"
    gfs_ds = xr.open_dataset(data_root+gfs_file, engine="cfgrib", backend_kwargs={'filter_by_keys': {'typeOfLevel':'isobaricInhPa'}})
    sst_ds = xr.open_dataset(data_root+sst_file).squeeze()
    sst_ds.sst.values += 273.15
    min_lon, min_lat, max_lon, max_lat = -77, 33, -50, 45
    sst_ds = sst_ds.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon+360, max_lon+360))
    gfs_ds = gfs_ds.sel(latitude=slice(min_lat,max_lat), longitude=slice(min_lon+360,max_lon+360))
    max_humidity_indices = gfs_ds['q'].argmax(dim='isobaricInhPa')
    begin, end = sst_ds.sst.shape[0], sst_ds.sst.shape[1]
    dims = gfs_ds.t.values[0][0:begin, 0:end]
    T_maxq = gfs_ds['t'].isel(isobaricInhPa=max_humidity_indices)[0:begin, 0:end].values
    q = gfs_ds['q'].isel(isobaricInhPa=max_humidity_indices).values[0:begin, 0:end]
    q_n = (q - 0.005) / (0.012 - 0.005)
    sst = sst_ds.sst[:,:].values
    b_07 = q_n*T_maxq + (1-q_n)*sst
    b_14 = 2*q_n*T_maxq + (1-(2*q_n))*sst
    btd = b_14 - b_07
    return sst_ds.lon, sst_ds.lat, btd

# Function to visualize NLCT data
def visualize_nlct(lon, lat, btd, date, dtime):
    #projection = ccrs.PlateCarree()
    fig, ax = plt.subplots(1, figsize=(12, 12))#, subplot_kw={'projection': projection})
    cmap = plt.cm.PuBu
    levels = np.linspace(-7, 7, 31)
    c = ax.contourf(lon, lat, btd, cmap=cmap, extend='both', levels=levels)
    clb = plt.colorbar(c, shrink=0.3, pad=0.02, ax=ax)
    ax.set_title(f'Synthetic NLCT ({date} {dtime})')
    clb.set_label('Brightness Temperature Difference (K)')
    ax.add_feature(cfeature.LAND, zorder=100, color='black', edgecolor='k')
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    fig.show()

# Main function
def main():
    dates = ["20230919"]
    dtime = "06z"
    for date in dates:
        download_data(date, dtime)
        lon, lat, btd = create_btd(date, dtime)
        visualize_nlct(lon, lat, btd, date, dtime)

if __name__ == "__main__":
    main()
