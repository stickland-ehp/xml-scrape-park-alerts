from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import json
import re
from datetime import datetime

def clean_text(text):
    # Function to clean up Unicode characters and extra whitespaces
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces
    text = text.encode('ascii', 'ignore').decode('utf-8')  # Remove non-ASCII characters
    return text.strip()

url = "https://parks.desi.qld.gov.au/xml/parkalerts.xml"
xml_data = requests.get(url).content

soup = BeautifulSoup(xml_data, "xml")

# Find all alert tags
alerts = soup.find_all("alert")

title = []
alert_id = []  # Added to capture the alert ID
alert_url = []
description = []
details = []
category = []
start_date = []
start_effective_date = []
end_date = []
parks = []

for child in alerts:
    try:
        title.append(clean_text(" ".join(child.find('title').get_text().split())))
    except:
        title.append(" ")

    try:
        alert_id.append(child['id'])  # Capture the alert ID from the 'id' attribute
    except KeyError:
        alert_id.append(" ")

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
        category.append(clean_text(" ".join(child.find('category').get_text().split())))
    except:
        category.append(" ")    

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
            park_id = park['id']  # Capture the park ID from the 'id' attribute
            park_name = clean_text(park.find('name').get_text())
            park_url = park.find('url').get_text()
            parks_list.append({"id": park_id, "name": park_name, "url": park_url})
    except:
        parks_list.append({"id": " ", "name": " ", "url": " "})
    parks.append(parks_list)

data = pd.DataFrame({
    "title": title,
    "alert_id": alert_id,
    "url": alert_url,
    "description": description,
    "details": details,
    "category": category,
    "start_date": start_date,
    "start_effective_date": start_effective_date,
    "end_date": end_date,
    "parks": parks
})

# Sort DataFrame by alert_id
final_data = data.sort_values(by="alert_id")

# Calculate the count of alerts
alerts_count = len(final_data)

# Add a timestamp to the top of the JSON output
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
summary_data = {
    "alerts_count": alerts_count,
    "script_run_time": timestamp
}

# Create an array with summary and alert data
output_data = {
    "summary": summary_data,
    "alerts": final_data.to_dict(orient='records')
}

# Print the output_data to file (JSON format) with pretty indentation
with open(r'alerts.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)
