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
import string
from datetime import datetime as dt

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

def get_president(date):
    sw1 = dt.strptime("31/10/2003", "%d/%m/%Y")
    sw2 = dt.strptime("31/10/2011", "%d/%m/%Y")
    d = dt.strptime(date, "%d/%m/%Y")

    if d <= sw1:
        return 'Duisenberg'
    if d <= sw2:
        return 'Trichet'
    return 'Draghi'

def get_statement(url, president):
    # function extracts transcript for a given statement (identified by url)

    # get HTML soup
    soup = get_HTML(url)
    article = soup.find('article')
    paragraphs = article.find_all('p')

    # concat paragaphs to one string
    speech = ''
    for i in range(len(paragraphs)):
        paragraph = paragraphs[i].text.strip().replace('\xa0', ' ')
        paragraph = paragraph.replace(president + ': ', '') # filter header of answers

        if not ('transcript' in paragraph and 'questions' in paragraph and 'answers' in paragraph): # filter first paragraph (link to Q&A)
            if not paragraph.startswith('Question:'): # filter questions
                speech += paragraph + ' '

    return speech

def get_statements(year):
    # function loads all historic introduction statements from the ECB webpage
    # and returns a data frame containing the date and link to each statement

    # get HTML soup
    url = "https://www.ecb.europa.eu/press/pressconf/" + str(year) + "/html/index.en.html"
    year_soup = get_HTML(url)

    # isolate statement dates and links
    dates = year_soup.find_all("dt")
    links = year_soup.findAll("span", { "class" : "doc-title" })

    # store result in pandas data frame
    d = []

    for i in range(len(links)):
        date = dates[i].text.strip()
        pres = get_president(date)
        link = 'https://www.ecb.europa.eu' + links[i].find('a')['href']
        text = get_statement(link, pres)
        d.append({'Date': date, 'President': pres, 'Text': text})

    return pd.DataFrame(d)


# ----------------------------------------------------------------------
# Run web scrapping
# ----------------------------------------------------------------------

# download date and links for each ECB introductory statement
# and store each data frame in a CSV file
first = True
for year in range(1998,2018):
    df = get_statements(year)
    df['Date'] = pd.to_datetime(df.Date, format="%d/%m/%Y")
    df.to_csv("../data/"+str(year)+".csv", index=False, encoding='utf-8')

    if first:
        cdf = df
        first = False
    else:
        cdf = pd.concat([cdf, df], ignore_index=True)

    time.sleep(1)

# and a single CSV file combining all statements
cdf.sort_values('Date').to_csv("../data/combined.csv", index=False, encoding='utf-8')
