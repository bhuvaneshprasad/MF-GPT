import csv
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json

def get_amc_category_codes(amc_codes_json_file, category_codes_json_file):
    with open(amc_codes_json_file, 'r') as json_file:
        amc_codes_dict = json.load(json_file)
        
    with open(category_codes_json_file, 'r') as json_file:
        category_codes_dict = json.load(json_file)

    return list(amc_codes_dict.values()), list(category_codes_dict.values())

def get_launch_date(amc_code, category_code, scheme_code):
    url = f'https://www.nirmalbang.com/ajaxpages/mutualfund/MfSnapShot.aspx?Fund={amc_code}&Category={category_code}&Scheme={scheme_code}'
    
    # Make the GET request
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table rows (tr) within the table that contains the Launch Date
    table = soup.find('table', class_='table-hover')
    rows = table.find_all('tr')

    # Loop through rows to find the one that contains 'Launch Date'
    launch_date = None
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 0 and 'Launch Date' in cells[0].text:
            launch_date = cells[1].text.strip()
            break

    # Process the Launch Date to adjust the year
    if launch_date:
        # Define the regex pattern to capture the date parts
        pattern = r'(\d{2}-\w{3}-)(\d{2})'
        match = re.search(pattern, launch_date)
        if match:
            day_month = match.group(1)
            year_suffix = match.group(2)
            year_suffix_int = int(year_suffix)
            
            # Get the current year
            current_year = datetime.now().year % 100
            
            # Determine the correct century and construct the new year
            if year_suffix_int <= current_year:
                new_year = f'20{year_suffix}'
            else:
                new_year = f'19{year_suffix}'
            
            # Construct the new launch date
            new_launch_date = f'{day_month}{new_year}'
            return new_launch_date
        else:
            print('Launch Date not in expected format')
    else:
        print('Launch Date not found')

def get_page_len(date_str):
    date_format = '%d-%b-%Y'
    date_object = datetime.strptime(date_str, date_format)
    today = datetime.today()
    date_diff = today - date_object
    days_difference = date_diff.days
    return int(((days_difference / 7) * 5) / 10)

def get_scheme_codes(amc_code, category_code):
    scheme_codes = []
    url = f'https://www.nirmalbang.com/ajaxpages/mutualfund/MFFundSelect.aspx?Category={category_code}&schcat={amc_code}'
    response = requests.get(url)
    text = response.text
    pattern = r'\*\|([^#]+)#(\d+)(?:&&)?'
    matches = re.findall(pattern, text)
    for match in matches:
        scheme_name, scheme_code = match
        if scheme_name != '' and scheme_code != '':
            scheme_codes.append(scheme_code)
    return scheme_codes

amc_codes, category_codes = get_amc_category_codes("amc_codes.json", "category_codes.json")

for amc_code in amc_codes:
    for category_code in category_codes:
        scheme_codes = get_scheme_codes(amc_code, category_code)
        for scheme_code in scheme_codes:
            launch_date = get_launch_date(amc_code, category_code, scheme_code)
            page_length = get_page_len(launch_date)
            base_url = 'https://www.nirmalbang.com/ajaxpages/mutualfund/MFhistorical_nav.aspx'
            params = {
                'Fund': amc_code,
                'Category': category_code,
                'Scheme': scheme_code,
                'FromDate': '23-Jul-2024',
                'ToDate': launch_date,
                'PageSize': '10'
            }
            
            for page_no in range(1, page_length):
                params['pageNo'] = page_no
                response = requests.get(base_url, params=params)
                json_response = response.json()
                if(len(json_response) == 0):
                    break
                for json in json_response:
                    with open(f"navs\\nav_data_{amc_code}.json", 'a') as f:
                        w = csv.writer(f)
                        w.writerow([json['SCHEMECODE'], json['S_NAME'], json['NAVDATE'], json['NAVRS']])
                print(f'Page {page_no}')
                break
            break
        break
    break

launch_date = get_launch_date(400032, 7, 3641)
page_length = get_page_len(launch_date)
print(page_length)
scheme_codes = get_scheme_codes(400032, 72)
print(scheme_codes)

