# BYU Covid Bot
<img src="https://github.com/brickellis/byucovidbot/blob/master/byucovid.JPG" height="200" width="300">
A twitter python bot which uses beautifulsoup to scrape BYU's daily COVID-19 numbers and tweet them. 
The twitter account is @BotByu

## Implementation

This is built on a raspberry pi running in the corner of my bedroom.

## Steps Involved

- Learn how to install python3 modules using pip.
- Use requests to download the html for the BYU Covid Updates page.
- Read beautifulsoup tutorials/documentation to figure out how to grab the correct element on the BYU page.
- Get a developer account for Twitter.
- Use tweepy to make authorized requests to post COVID-19 updates.
- Learn to use ssh to transfer my python script to my raspberry pi and install the necessary python3 modules.
- Use crontab to schedule the running of my python3 script every two hours on the hour.

## Future Steps

- Add automated graphs showing changes over time.
- Add web scraping of COVID-19 statistics for Utah County and other local universities.
