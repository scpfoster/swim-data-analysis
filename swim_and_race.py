# This file is to get swim and race results for a given season
import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
from random import randint
import logging
import utilities as util

# set the logging level as info
logging.basicConfig(level=logging.INFO)

# dictionary to hold the season info
season_dict = {}
season_dict['season'] = '17'
season_dict['meet_file'] = 'meets_2016_2017.csv'
season_dict['club_file'] = 'clubs_2016_2017.csv'
season_dict['swimmers_file'] = 'swimmers_2016_2017.csv'
season_dict['race_file'] = 'races_2016_2017.csv'

# read in the previously captured list of clubs for each meet for the season
swims_df = pd.read_csv(season_dict['club_file'])

# create a list of URLS holding each clubs results
clubURLS = swims_df['club_res_url'].tolist()

# define lists to hold the results
sw_list = []
rc_list = []

#for each club, get the swimmer info and race results
count_of_club = 1
num_clubs = len(clubURLS)

for item in clubURLS:
    logging.info("club %i of %i total clubs", count_of_club, num_clubs)
    try:
        if "https" in item:
            tmp_sw_list, tmp_rc_list = util.getRaceResults(item)
            sw_list += tmp_sw_list
            rc_list += tmp_rc_list
    except:
        print(item, "is not a valid url")
    count_of_club += 1

#put results in a dataframe
swim_df = pd.DataFrame(sw_list)
race_df = pd.DataFrame(rc_list)

#save dataframe to csv
swim_df.to_csv(season_dict['swimmers_file'], index=False)
race_df.to_csv(season_dict['race_file'], index=False)
