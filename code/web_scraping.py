# ----------------------------------------------------------------------
# Information
# ----------------------------------------------------------------------

# Web scrap historic ECB introduction statements
#
# (Author) Hans-Peter Höllwirth
# (Date)   06.2017

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

from bs4 import BeautifulSoup
import urllib
import pandas as pd
import ssl
import os
import time

os.chdir("/Users/Hans-Peter/Documents/Masters/14D010/project/code")

# ----------------------------------------------------------------------
# Web scrapping functions
# ----------------------------------------------------------------------

def get_HTML(url):
	# function loads html source code of given url
    ssl._create_default_https_context = ssl._create_unverified_context
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent,}
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_statements(year):
	# function loads all historic introduction statements from the ECB webpage
    # and returns a data frame containing the date and link to each statement

	# get HTML Soup
	url = "https://www.ecb.europa.eu/press/pressconf/" + str(year) + "/html/index.en.html"
	year_soup = get_HTML(url)

	# isolate statement dates and links
	dates = year_soup.find_all("dt")
	links = year_soup.findAll("span", { "class" : "doc-title" })

	# store result in pandas data frame
	d = []

	for i in range(len(links)):
		date = dates[i].text.strip()
		link = 'https://www.ecb.europa.eu' + links[i].find('a')['href']
		d.append({'Date': date, 'Link': link})

	return pd.DataFrame(d)


# ----------------------------------------------------------------------
# Run web scrapping
# ----------------------------------------------------------------------

# download date and links for each ECB introductory statement
# and store each data frame in a CSV file
for year in range(1998,2018):
    df = get_statements(year)
    df.to_csv("../data/"+str(year)+".csv", index=False, encoding='utf-8')
    #print('.', end='')
    time.sleep(1)
