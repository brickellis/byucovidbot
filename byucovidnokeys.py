from bs4 import BeautifulSoup
import requests
import tweepy 
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

# Twitter API Keys and Secrets
consumer_key = 'XXXX' 
consumer_secret = 'XXXX' 
access_token = 'XXXX' 
access_token_secret = 'XXXX' 


# The url used to find the COVID-19 numbers.
listingurl = "https://www.byu.edu/coronavirus/"
response = requests.get(listingurl)
soup = BeautifulSoup(response.text, "html.parser")

# The three pieces of data scraped from the site.
active_cases_str = soup.find("td", text="Active cases").find_next_sibling("td").get_text()
no_isolation_str = soup.find("td", text="Cases no longer in isolation").find_next_sibling("td").get_text()
total_cases_str = soup.find("td", text="Total reported cases").find_next_sibling("td").get_text()
scraped_data = [time.time(),active_cases_str,no_isolation_str,total_cases_str]

# Check for scrape error and convert text to int
if active_cases_str.isnumeric() and no_isolation_str.isnumeric():
    active_cases = int(active_cases_str)
    no_isolation = int(no_isolation_str)
    total_cases = int(total_cases_str)
    scrape_check = True
else:
    scrape_check = False

# Read all data from csv
covid_data = pd.read_csv('coviddata.csv', parse_dates=['timestamp'], date_parser=lambda epoch: pd.to_datetime(epoch, unit='s'))

# Reading the last date it posted a tweet as well as the last active_cases number posted.
covid_data_length = len(covid_data) - 1
oldnumber = covid_data.iat[covid_data_length, 1]
lastpost = covid_data.iat[covid_data_length, 0]

# If the active cases changed, the active cases number is numeric (the site format didn't change), and I haven't already posted that day.
diditrun = "Did not run."
if active_cases != oldnumber and scrape_check == True:
    # Get twitter auth
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    # Say it ran.
    diditrun = "Ran!"
    # Add new data to csv
    with open('coviddata.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([scraped_data])
    # Render graph image with new data
    covid_data = pd.read_csv('coviddata.csv', parse_dates=['timestamp'], date_parser=lambda epoch: pd.to_datetime(epoch, unit='s'))
    ax = plt.gca()
    fig = covid_data.plot(kind='line', x='timestamp', y='active', ax=ax, color="red")
    fig = covid_data.plot(kind='line', x='timestamp', y='inactive', ax=ax, color="blue", figsize=(20,16), fontsize=26).get_figure()
    fig.savefig("graph.png")

    # Tweet the new data and when it was collected.
    tweet = datetime.datetime.now().strftime("%m/%d/%Y") + "\n" + "Active Cases: " + active_cases_str + "\n" + "Cases No Longer In Isolation: " + no_isolation_str + "\n" + "Total Reported Cases: " + total_cases_str
    api.update_with_media('graph.png', tweet)

# Add to the log of every time my program runs and whether it actually posted or not.
file10 = open("/home/pi/Downloads/dates.txt","a")
file10.write(datetime.datetime.now().strftime("%m/%d/%Y") + " " + datetime.datetime.now().strftime("%X") + " " + diditrun + "\n") 
file10.close()