import html2text
import requests
from bs4 import BeautifulSoup
import time
import random
import re
from datetime import datetime
import json

def clean_text(text):
    # Replace newlines within sentences with a space
    if "|" not in text:
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Replace single newlines with spaces
    return text

# Filter out paragraphs containing any of the words or phrases
def contains_any(text, words_list):
    return any(word in text for word in words_list)

words_to_remove = ['Advisorkhoj', 'advisorkhoj', 'Source']

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True

api = "https://www.advisorkhoj.com/articles"
page = api
total = 0

for i in range(114, 159):
    response = requests.get(f"https://www.advisorkhoj.com/articles?pageid={i}")
    response_content = response.content
    # Parse the HTML content
    soup = BeautifulSoup(response_content, 'html.parser')
    cards = soup.find_all('div', class_="col-md-12 col-sm-12")
    for j, card in enumerate(cards[1:]):
        h2_elements = card.find_all('h2')
    for h2 in h2_elements:
        # Extract <a> tags inside each <h2> tag
        a_tag = h2.find('a')
        post_link = a_tag.get('href')
        post_link = 'https://www.advisorkhoj.com'+ post_link if post_link.startswith('/articles') else post_link
        blog_response = requests.get(post_link)
        if blog_response.status_code !=200:
            continue
        blog_page = blog_response.content
        blog_soup = BeautifulSoup(blog_page, 'html.parser')
        isNotTitle = False if blog_soup.find(class_='main-heading') else True
        if isNotTitle:
            continue
        blog_title = "Title: " + blog_soup.find(class_='main-heading').text + "\n\n"
        # date_str = blog_soup.find(class_='padding-top20').find(class_='container').find(class_='row').find(class_='col-md-8').find(class_='padding-bottom12').find(class_='col-md-12').find(class_='margin-bottom20').text
        # date_groups = re.search(r'\b([A-Za-z]{3}) \d{1,2}, (\d{4})\b', date_str)
        # blog_date = "Date: " + datetime.strptime(date_groups.group(1) + ' ' + date_groups.group(2), "%b %Y").strftime("%B %Y") + "\n\n"
        date_elems = blog_soup.find_all(class_='margin-bottom20')
        dates = []
        for date_elem in date_elems:
            matches = re.search(r'\b([A-Za-z]{3}) \d{1,2}, (\d{4})\b', str(date_elem))
            if matches:
                date_str = datetime.strptime(matches.group(1) + ' ' + matches.group(2), "%b %Y").strftime("%B %Y")
                dates.append(date_str)
            blog_date = "Date: " + list(set(dates))[0] + "\n\n"
        # blog_contents = blog_soup.find(class_='padding-top20').find(class_='container').find(class_='row').find(class_='col-md-8').find(class_='padding-bottom12').find(class_='col-md-12').find(class_='anchor-div')
        blog_contents = blog_soup.find(class_='anchor-div') if '/articles' in post_link else blog_soup.find(class_='article_anchor')
        text_content = h.handle(str(blog_contents))
        blog_categories = "Category: ['Mutual Funds]" + "\n\n"
        # Split the text into paragraphs
        paragraphs = text_content.split('\n\n')  # Paragraphs are typically separated by double newlines

        filtered_paragraphs = [para for para in paragraphs if not contains_any(para, words_to_remove)]
        paras = []

        for para in filtered_paragraphs:
            para = clean_text(para)  # Clean up newlines in each paragraph
            paras.append(para)

        # Join the remaining paragraphs back into a single string
        filtered_text = '\n\n'.join(paras)
        filtered_text = "Content:\n\n" + filtered_text

        delimiter = '\n--- End of Article ---\n\n'

        # Specify the file path
        file_path = '/content/advisorkhoj_blogs_85.txt'

        # Append the filtered text and the delimiter to the file
        with open(file_path, 'a') as file:
            file.write(blog_title + blog_date + blog_categories + filtered_text + delimiter)

        print(f"Filtered text from page: {i}, blog: {j+1} has been appended to {file_path}")
        total+=1

                # sleep_time = random.uniform(1, 10)
                # time.sleep(sleep_time)

    # page = api +f"?pageid={i+1}"
    # sleep_time = random.uniform(5, 10)
    # time.sleep(sleep_time)
    print(f"Total: {total}")
    #     break
    #   break
    # break