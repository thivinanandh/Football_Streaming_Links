# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import os
from pprint import pprint
import re
 
url = 'http://www.redditsoccerstreams.tv'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')


## obtain all the links from the given URL and save it as a DF
table = soup.find( "table" )

## replace Watch with href Links 
regex = '<td><a href=\"(.*?)\">.*?<\/a><\/td>'
subst = '<td>\\1</td>'
tableNew = re.sub(regex,subst,str(table),re.MULTILINE)
tableDF = pd.read_html(str(tableNew))[0]
c = ["Time","Match","Link"]
tableDF.columns =c 
# %%

## this function identifies, if there is an iframe present within the
## given url or not. 
def iframeIdentifier(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    if(len(soup.find_all('iframe'))):
        return soup.find_all('iframe')[0]['src']
    else:
        return "IframenotFound"


for  rowIndex in range(tableDF.shape[0]):
    row = tableDF.iloc[rowIndex,:]
    oldLink = row["Link"]
    if("http:" not in oldLink):
        continue
    newLink = iframeIdentifier(oldLink)
    if(newLink != "IframenotFound"):
        row["Link"] = newLink



# %%
tableDF_valid = tableDF[tableDF["Link"].str.contains("http") ]
templateLoader = FileSystemLoader(searchpath="./")
templateEnv = Environment(loader=templateLoader)
template = templateEnv.get_template('template.html')
filename = "index.html"
with open(filename, 'w') as fh:
    fh.write(template.render(
        my_string = "Hello Jinja2",
        show_one = True,
        show_two = False,
        my_list    = tableDF_valid['Link'].to_list(),
        names = tableDF_valid['Match'].to_list(),
        zip=zip
    ))
print("Match link generation completed")
# %%
