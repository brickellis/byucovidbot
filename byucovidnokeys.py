from bs4 import BeautifulSoup
import requests
import tweepy 
import datetime 

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
active_cases = soup.find("td", text="Active cases").find_next_sibling("td").get_text()
no_isolation = soup.find("td", text="Cases no longer in isolation").find_next_sibling("td").get_text()
total_cases = soup.find("td", text="Total reported cases").find_next_sibling("td").get_text()

# Reading the last date it posted a tweet as well as the last active_cases number posted. Not the best way to do it.
file5 = open("/home/pi/Downloads/recent.txt","r")
oldnumber = file5.read()
file6 = open("/home/pi/Downloads/recentpost.txt","r")
lastpost = file6.read()

# If the active cases changed, the active cases number is numeric (the site format didn't change), and I haven't already posted that day.
diditrun = "Did not run."
if active_cases != oldnumber and active_cases.isnumeric() and lastpost != datetime.datetime.now().strftime("%m/%d/%Y"):
    # Get twitter auth
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    # Say it ran.
    diditrun = "Ran!"
    # Change the last day I posted.
    file11 = open("/home/pi/Downloads/recentpost.txt","w")
    file11.write(datetime.datetime.now().strftime("%m/%d/%Y")) 
    file11.close()
    #Tweet the new data and when it was collected.
    api.update_status(datetime.datetime.now().strftime("%m/%d/%Y") + "\n" + "Active Cases: " + active_cases + "\n" + "Cases No Longer In Isolation: " + no_isolation + 
        "\n" + "Total Reported Cases: " + total_cases)
    # Change the last active_cases posted.
    file1 = open("/home/pi/Downloads/recent.txt","w")
    file1.write(active_cases) 
    file1.close()
# Add to the log of every time my program runs and whether it actually posted or not.
file10 = open("/home/pi/Downloads/dates.txt","a")
file10.write(datetime.datetime.now().strftime("%m/%d/%Y") + " " + datetime.datetime.now().strftime("%X") + " " + diditrun + "\n") 
file10.close()