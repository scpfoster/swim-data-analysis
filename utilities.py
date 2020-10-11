## This file holds utility methods used to parse webpages and return the results of interest
import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
from random import randint
import logging

#todo: use this method with the previously define method rather than having the code repeated multiple times
def scrapePage(url):
    #get the page with the results for the club
    logging.debug(url)
    sleepTime = randint(10, 14)
    logging.debug("sleep time is %i seconds", sleepTime)
    time.sleep(sleepTime)
    response = requests.get(url)
    logging.debug('%s', response.url)

    #use Beautiful Soup to parse the returned page
    resp = BeautifulSoup(response.text, 'lxml')

    #return the page
    return resp

# function to get meet list
def getMeetList(season, month, base_url):
    #create param list for the URL
    call_params = {'season': season, 'province': '', 'month': month}

    #get the page after a random delay
    #I think the crawl delay is 10 seconds, so while it will take longer,
    #I will set a random delay of 10-14 seconds
    # sleepTime = randint(10, 14)
    # logging.debug("sleep time is %i seconds", sleepTime)
    # time.sleep(sleepTime)
    # response = requests.get(base_url, params=call_params)
    # logging.debug('%s', response.url)

    #parse the page and create the list
    #use Beautiful Soup to parse the returned page
    #meetList_resp = BeautifulSoup(response.text, 'lxml')

    #get the page with the meets for the season
    meetList_resp = scrapePage(base_url)

    rtnList = []
    for item in meetList_resp.find_all('tr'):
        if item.contents[5].contents[0] == "Masters":
            ## need to handle the case where there was a meet, but there are no results

            temp_dict = {}
            try:
                temp_dict['meet_date'] = item.contents[0].contents[0].contents[0]
            except:
                temp_dict['meet_date'] = None

            try:
                temp_dict['meet_url'] = item.contents[1].a.attrs['href']
            except:
                temp_dict['meet_url'] = None

            try:
                temp_dict['meet_prov'] = item.contents[2].contents[0]
            except:
                temp_dict['meet_prov'] = None

            try:
                temp_dict['meet_host'] = item.contents[3].contents[0].contents[0]
            except:
                temp_dict['meet_host'] = None

            try:
                temp_dict['meet_course'] = item.contents[4].contents[0]
            except:
                temp_dict['meet_course'] = None

            try:
                temp_dict['meet_type'] = item.contents[5].contents[0]
            except:
                temp_dict['meet_type'] = None

            try:
                temp_dict['meet_status'] = item.contents[6].contents[0]
            except:
                temp_dict['meet_status'] = None

            try:
                temp_dict['meet_id_1'] = item.contents[1].a.attrs['href'].split("/")[-1]
            except:
                temp_dict['meet_id_1'] = None

            rtnList.append(temp_dict)

    logging.debug("Number of meets: %i", len(rtnList))
    #return the list of meets
    return rtnList

### add comments ####
def getTeamList(meet_url):

    # logging.debug(meet_url)
    # sleepTime = randint(10, 14)
    # logging.debug("sleep time is %i seconds", sleepTime)
    # time.sleep(sleepTime)
    # response = requests.get(meet_url)
    # logging.debug('%s', response.url)

    # #parse the swim club list page
    # #use Beautiful Soup to parse the returned page
    # clubList_resp = BeautifulSoup(response.text, 'lxml')

    #get the page with the clubs attending the meet
    clubList_resp = scrapePage(meet_url)

    rtnList = []
    for item in clubList_resp.find_all('option'):
        temp_dict = {}
        if "Events" in item.contents[0]:
            logging.debug("Did I get here?")
            break
        elif "Participants" not in item.contents[0]:
            try:
                temp_dict['club_res_url'] = item.attrs['data-href']
            except:
                temp_dict['club_res_url'] = None
            try:
                temp_dict['club_number'] = item.attrs['value']
            except:
                temp_dict['club_number'] = None
            try:
                temp_dict['club_name'] = item.contents[0]
            except:
                temp_dict['club_name'] = None
            try:
                temp_dict['meet_id_1'] = meet_url.split("/")[-1]
            except:
                temp_dict['meet_id_1'] = None
            try:
                temp_dict['meet_id_2'] = item.attrs['data-href'].split("/")[-2]
            except:
                temp_dict['meet_id_2'] = None
            rtnList.append(temp_dict)

    return rtnList


def parseSwimmerInfo(tableRow):

    #create return dictionary
    sw_dict = {}

    #parse the row
    try:
        sw_dict['sw_url'] = tableRow.find('a').attrs['href']
    except:
        sw_dict['sw_url'] = None
    try:
        #sw_id = tableRow.find('a').attrs['href'].split('/')[5]
        sw_dict['sw_id'] = tableRow.find('a').attrs['href'].split('/')[5]
    except:
        sw_dict['sw_id'] = None
    try:
        sw_dict['sw_name'] = tableRow.find('a').contents[0]
    except:
        sw_dict['sw_name'] = None
    try:
        sw_dict['sw_yob'] = tableRow.find('th').contents[1][3:7]
    except:
        sw_dict['sw_yob'] = None

    #return the dictionary
    return sw_dict


def parseRaceInfo(tableRow):

    #create return dictionary
    rc_dict = {}

    #rc_dict['sw_id'] = sw_id
    #rc_dict['sw_yob'] = sw_yob
    #try:
    #    rc_dict['sw_gender'] = tableRow.contents[0].find('a').attrs['data-query-gender']
    #except:
    #    rc_dict['sw_gender'] = None
    try:
        rc_dict['rc_dist_stroke'] = tableRow.contents[0].find(
            'span').find('a').contents[0]
    except:
        rc_dict['rc_dist_stroke'] = None
    try:
        rc_dict['rc_round'] = tableRow.contents[1].contents[0]
    except:
        rc_dict['rc_round'] = None
    try:
        rc_dict['rc_time'] = tableRow.contents[3].contents[0]
    except:
        rc_dict['rc_time'] = None
    try:
        rc_dict['rc_course'] = tableRow.contents[4].find('abbr').contents[0]
    except:
        rc_dict['rc_course'] = None

    #print(rc_dict)
    return rc_dict


def getRaceResults(club_url):
    #def getRaceResults(raceList_resp):

    ##### Remember to uncomment this to scrape the page
    #get the page with the results for the club
    raceList_resp = scrapePage(club_url)

    #create a list of tables on the page
    temp_table = raceList_resp.find_all('table')
    logging.debug("number of tables %i", len(temp_table))

    #create a gender table to use based on which table is being parsed
    gender_dict = {0: "male", 1: "female", 2: "relay"}

    #create lists to hold swimmer and race info
    swimmer_list = []
    race_list = []

    #recover the meet id from the url to attach to swimmer and race
    #call it meet_id_2 since to be consistent with other data structure
    meet_id_2 = club_url..split("/")[-2]

    #if 3 or more tables, there are results on the page
    if len(temp_table) < 3:
        logging.info("no results on the page")
        #add code to put all nulls in the return value
    else:
        for tt in range(len(temp_table)-2):
            logging.debug("on table %i", tt)
            #set a flag for the first row, want to ignore it
            firstRow = True

            #get the gender based on which table is being parsed
            sw_gender = gender_dict[tt]

            #create variables to hold the last swimmer id and yob
            sw_id = None
            sw_yob = None

            #loop through each row in the table
            for item in temp_table[tt].find_all('tr'):
                temp_sw_dict = {}
                temp_rc_dict = {}
                if firstRow == True:
                    logging.debug("first row of table, ignore")
                    firstRow = False
                elif item.has_attr('class'):
                    #parse the swimmer information
                    temp_sw_dict = parseSwimmerInfo(item)

                    #add the gender
                    try:
                        temp_sw_dict['sw_gender'] = sw_gender
                    except:
                        temp_sw_dict['sw_gender'] = None

                    #add the meet id
                    try:
                        temp_sw_dict['meet_id_2'] = meet_id_2
                    except:
                        temp_sw_dict['meet_id_2'] = None

                    #make the swimmer id and yob available
                    sw_id = temp_sw_dict['sw_id']
                    sw_yob = temp_sw_dict['sw_yob']

                    #append to the return list
                    swimmer_list.append(temp_sw_dict)

                else:

                    #parse the race information
                    temp_rc_dict = parseRaceInfo(item)

                    #add the swimmer id, yob, gender
                    temp_rc_dict['sw_id'] = sw_id
                    temp_rc_dict['sw_yob'] = sw_yob
                    temp_rc_dict['sw_gender'] = sw_gender
                    #add the meet id
                    try:
                        temp_rc_dict['meet_id_2'] = meet_id_2
                    except:
                        temp_rc_dict['meet_id_2'] = None

                    #append to the return list
                    race_list.append(temp_rc_dict)

                #else:
                #    logging.debug("expect no information in this row")
                #count += 1
    return swimmer_list, race_list
