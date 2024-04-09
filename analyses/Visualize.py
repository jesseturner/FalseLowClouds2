import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from Download_Model_Data import download_data
from Model_Simulated_BTD import create_btd

# Function to visualize NLCT data
def visualize_nlct(lon, lat, btd, date, dtime):
    projection = ccrs.PlateCarree()
    fig, ax = plt.subplots(1, figsize=(12, 12), subplot_kw={'projection': projection})
    cmap = plt.cm.PuBu
    levels = np.linspace(-7, 7, 31)
    c = ax.contourf(lon, lat, btd, cmap=cmap, extend='both', levels=levels)
    clb = plt.colorbar(c, shrink=0.3, pad=0.02, ax=ax)
    ax.set_title(f'Synthetic NLCT ({date} {dtime})')
    clb.set_label('Brightness Temperature Difference (K)')
    ax.add_feature(cfeature.LAND, zorder=100, color='black', edgecolor='k')
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    fig.show()


# General mapping function
def map_data(lon, lat, data, levels, title, clb_label):
    projection = ccrs.PlateCarree()
    fig, ax = plt.subplots(1, figsize=(12, 12), subplot_kw={'projection': projection})
    cmap = plt.cm.PuBu
    c = ax.contourf(lon, lat, data, cmap=cmap, extend='both', levels=levels)
    clb = plt.colorbar(c, shrink=0.3, pad=0.02, ax=ax)
    ax.set_title(title)
    clb.set_label(clb_label)
    ax.add_feature(cfeature.LAND, zorder=100, color='black', edgecolor='k')
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    fig.show()

