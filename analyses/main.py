from Download_Model_Data import download_data
from Model_Simulated_BTD import create_btd
from Visualize import visualize_nlct

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
