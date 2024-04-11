import os

# Function to download data
# this was written for MacOS, likely won't work on other operating systems
def download_data(date, dtime):
    directory = f"data/{date}/"
    sst_file = f"{directory}/oisst-avhrr-v02r01.{date}.nc"
    gfs_file = f"{directory}/gfs.t{dtime}.pgrb2.0p25.f000"

    if os.path.isfile(sst_file) and os.path.isfile(gfs_file):
        print("Files exist")
        return
    
    if not os.path.exists(directory):
        print("Making new directories")
        os.makedirs(directory)
    else:
        print("Directory exists but some files are missing")
        
    sst_url = f"https://www.ncei.noaa.gov/thredds/fileServer/OisstBase/NetCDF/V2.1/AVHRR/{date[:6]}/oisst-avhrr-v02r01.{date}.nc"
    sst_backup_url = f"https://www.ncei.noaa.gov/thredds/fileServer/OisstBase/NetCDF/V2.1/AVHRR/{date[:6]}/oisst-avhrr-v02r01.{date}_preliminary.nc"
    os.system(f"curl -o {directory}/oisst-avhrr-v02r01.{date}.nc {sst_url} || curl -o {directory}/oisst-avhrr-v02r01.{date}_preliminary.nc {sst_backup_url}")
        
    gfs_url = f"https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.{date}/{dtime[:2]}/atmos/gfs.t{dtime}.pgrb2.0p25.f000"
    os.system(f"curl -o {directory}/gfs.t{dtime}.pgrb2.0p25.f000 {gfs_url}")
    
    return