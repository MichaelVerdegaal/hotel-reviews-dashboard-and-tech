import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://www.booking.com'
BASE_CATALOG_URL = 'https://www.booking.com/searchresults.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaKkBiAEBmAExuAEKyAEF2AEB6AEB-AECiAIBqAIDuAL_4sP6BcACAdICJGFhY2JlMjA5LWE3ZWMtNGZhZC05MzI2LWM3NmRlMmQ2MGZiZNgCBeACAQ&sid=b7ae3ce18748b2e76e194075e2e4ae6c&tmpl=searchresults&ac_click_type=b&ac_position=1&class_interval=1&dest_id=222&dest_type=country&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&nflt=ht_id%3D204%3Bclass%3D5%3Bclass%3D4%3Bclass%3D3%3Bclass%3D2%3Bclass%3D1%3Buf%3D-2601889%3B&no_rooms=1&order=class_and_price&postcard=0&raw_dest_type=country&room1=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=0&slp_r_match=0&srpvid=7a84606916b6014e&ss=United%20Kingdom&ss_all=0&ss_raw=uni&ssb=empty&sshis=0&ssne=Spain&ssne_untouched=Spain&top_ufis=1&rows=25'
KAGGLE_CSV = os.path.join(ROOT_DIR, "static/kaggle_reviews.csv")
MANUAL_CSV = os.path.join(ROOT_DIR, "static/manual_reviews.csv")
PRELIMINARY_CLEAN_DF = "static/preliminary_clean_df.pickle"
CLEAN_DF = "static/cleaned_df.pickle"
LABELED_DF = "static/labeled_df.pickle"
YOUR_REVIEWS = "static/enter_your_reviews.xlsx"

# Unless you also use localhost, don't fill in your database credentials here.
# Create a separate config file with your credentials in that case.
HOST = "localhost"
USERNAME = "root"
PASSWORD = "MyNewPass"
DATABASE = "hotelreviews"