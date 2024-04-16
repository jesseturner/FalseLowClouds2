import xarray as xr

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

