from Download_Model_Data import download_data

# Main function
def main():
    dates = ["20230918", "20230919"]
    dtime = "06z"
    min_lon, min_lat, max_lon, max_lat = -77, 33, -50, 45
    for date in dates:
        download_data(date, dtime)
        #lon, lat, btd = create_btd(date, dtime)
        #visualize_nlct(lon, lat, btd, date, dtime)


if __name__ == "__main__":
    main()
