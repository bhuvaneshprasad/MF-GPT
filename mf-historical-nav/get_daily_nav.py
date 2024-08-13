import csv
import requests

# Loop through pages from 1 to 600
for page_no in range(1, 884):
    url = f'https://www.nirmalbang.com/ajaxpages/mutualfund/mfdailynav.aspx?Fund=&Category=&Scheme=&Alphabet=&pageNo={page_no}&PageSize=10'
    
    # Make the GET request
    response = requests.get(url)

    json_response = response.json()

    for json in json_response:
        with open("daily_nav.csv", 'a', newline='') as f:
            w = csv.writer(f)
            w.writerow([json['SCHEMECODE'], json['S_NAME'], json['NAVDATE'], json['NAVRS']])
    print(page_no)