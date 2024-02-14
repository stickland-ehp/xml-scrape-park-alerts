from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import numpy as np
import requests
import json

final_data = pd.DataFrame()

for i in range(10):
    url = "https://parks.des.qld.gov.au/xml/parkalerts.xml".format(i+1)
    xml_data = requests.get(url).content

    soup = BeautifulSoup(xml_data, "xml")

    # Find all text in the data
    texts = str(soup.findAll(text=True)).replace('\\n','')

    # Find the tag/child
    child = soup.find("alert")

    title = []
    alert_url = []
    description = []
    details= []

    while True:
        try:
            title.append(" ".join(child.find('title').text))
        except:
            title.append(" ")

        try:
            alert_url.append(" ".join(child.find('url').text))
        except:
            alert_url.append(" ")

        try:
            description.append(" ".join(child.find('description').text))
        except:
            description.append(" ")

        try:   
            details.append(" ".join(child.find('details').text))
        except:
        details.append(" ")

        # Next sibling of child, here: alert 
        child = child.find_next_sibling('alert')
        if not child:  # Use break statement if no more alerts found.
            break
    
   data=pd.DataFrame({
         "title":title,
         "url":alert_url,
         "description":description,
         "details":details})

   final_data=final_data.append(data, ignore_index=True)

# Print the final_data to file (JSON format)
final_data.to_json(r'alerts.json', orient='records')
