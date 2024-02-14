from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import numpy as np
import requests

final_data = pd.DataFrame()
for i in range(10):
    
    url = "https://parks.des.qld.gov.au/xml/parkalerts.xml".format(i+1)
    
    xml_data = requests.get(url).content

    soup = BeautifulSoup(xml_data, "xml")
     
    # Find all text in the data
    texts = str(soup.findAll(text=True)).replace('\\n','')
    
    #Find the tag/child
    child = soup.find("alert")
    
    title = []
    url = []
    description = []
    details = []
    date_start = []
    date_end = []
    date_effective = []
    parks = []
    
    while True:               
        try:
            title.append(" ".join(child.find('title')))
        except:
            title.append(" ")
        
        try:
            url.append(" ".join(child.find('url')))
        except:
            url.append(" ")
            
        try:
            description.append(" ".join(child.find('descrption')))
        except:
            description.append(" ")
        
        try:
            details.append(" ".join(child.find('details')))
        except:
            details.append(" ")
        
        try:   
            # Next sibling of child, here: entry 
            child = child.find_next_sibling('alert')
        except:
            break
    
    data = []
    data = pd.DataFrame({
      "title": title,
      "url": url,
      "description": description,
      "details": details
    })
    final_data = final_data.append(data, ignore_index = True)
