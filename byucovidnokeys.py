from bs4 import BeautifulSoup
import requests
import tweepy 
import datetime 

consumer_key = 'XXXX' 
consumer_secret = 'XXXX' 
access_token = 'XXXX' 
access_token_secret = 'XXXX' 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


listingurl = "https://www.byu.edu/coronavirus/"
response = requests.get(listingurl)
soup = BeautifulSoup(response.text, "html.parser")

active_cases = soup.find("td", text="Active cases").find_next_sibling("td").get_text()
no_isolation = soup.find("td", text="Cases no longer in isolation").find_next_sibling("td").get_text()
total_cases = soup.find("td", text="Total reported cases").find_next_sibling("td").get_text()


file5 = open("/home/pi/Downloads/recent.txt","r")
oldnumber = file5.read()
diditrun = "Did not run."
if active_cases != oldnumber:
    diditrun = "Ran!"
    api.update_status(datetime.datetime.now().strftime("%m/%d/%Y") + "\n" + "Active Cases: " + active_cases + "\n" + "Cases No Longer In Isolation: " + no_isolation + 
        "\n" + "Total Reported Cases: " + total_cases)
    file1 = open("/home/pi/Downloads/recent.txt","w")
    file1.write(active_cases) 
    file1.close()

file10 = open("/home/pi/Downloads/dates.txt","a")
file10.write(datetime.datetime.now().strftime("%m/%d/%Y") + " " + datetime.datetime.now().strftime("%X") + " " + diditrun + "\n") 
file10.close()