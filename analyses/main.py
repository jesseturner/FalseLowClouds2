from Download_Model_Data import download_data
from Model_Simulated_BTD import create_btd
from Visualize import visualize_nlct
from Model_Air_Mass import create_air_mass
from Visualize import visualize_air_mass

# Main function
def main():
    dates = ["20230919"]
    dtime = "06z"
    min_lon, min_lat, max_lon, max_lat = -77, 33, -50, 45
    for date in dates:
        download_data(date, dtime)
        #lon, lat, btd = create_btd(date, dtime)
        #visualize_nlct(lon, lat, btd, date, dtime)
        lon, lat, data = create_air_mass(date, dtime, min_lon, min_lat, max_lon, max_lat)
        visualize_air_mass(lon, lat, data, date, dtime)


if __name__ == "__main__":
    main()
