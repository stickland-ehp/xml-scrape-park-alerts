from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import numpy as np
import requests
import json
import re

def clean_text(text):
    # Function to clean up Unicode characters and extra whitespaces
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces
    text = text.encode('ascii', 'ignore').decode('utf-8')  # Remove non-ASCII characters
    return text.strip()

all_data = []  # Initialize a list to store individual DataFrames

for i in range(10):
    url = "https://parks.des.qld.gov.au/xml/parkalerts.xml".format(i+1)
    xml_data = requests.get(url).content

    soup = BeautifulSoup(xml_data, "xml")

    # Find all text in the data
    texts = str(soup.find_all(text=True)).replace('\\n', '')

    # Find the tag/child
    child = soup.find("alert")

    title = []
    alert_url = []
    description = []
    details = []
    start_date = []
    start_effective_date = []
    end_date = []
    parks = []

    while True:
        try:
            title.append(clean_text(" ".join(child.find('title').get_text().split())))
        except:
            title.append(" ")

        try:
            alert_url.append(" ".join(child.find('url').get_text().split()))
        except:
            alert_url.append(" ")

        try:
            description.append(clean_text(" ".join(child.find('description').get_text().split())))
        except:
            description.append(" ")

        try:
            details.append(clean_text(" ".join(child.find('details').get_text().split())))
        except:
            details.append(" ")

        try:
            start_date.append(child.find('date').find('start').get_text())
        except:
            start_date.append(" ")

        try:
            start_effective_date.append(child.find('date').find('startEffective').get_text())
        except:
            start_effective_date.append(" ")

        try:
            end_date.append(child.find('date').find('end').get_text())
        except:
            end_date.append(" ")

        parks_list = []
        try:
            parks_data = child.find('parks').find_all('park')
            for park in parks_data:
                park_name = clean_text(park.find('name').get_text())
                park_url = park.find('url').get_text()
                parks_list.append({"name": park_name, "url": park_url})
        except:
            parks_list.append({"name": " ", "url": " "})
        parks.append(parks_list)

        # Next sibling of child, here: alert
        child = child.find_next_sibling('alert')
        if not child:  # Use break statement if no more alerts found.
            break

    data = pd.DataFrame({
        "title": title,
        "url": alert_url,
        "description": description,
        "details": details,
        "start_date": start_date,
        "start_effective_date": start_effective_date,
        "end_date": end_date,
        "parks": parks
    })

    all_data.append(data)

# Concatenate all individual DataFrames into a single DataFrame
final_data = pd.concat(all_data, ignore_index=True)

# Print the final_data to file (JSON format)
final_data.to_json(r'alerts.json', orient='records')
