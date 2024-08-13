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

words_to_remove = ['Also read', 'Also Read', 'ALSO READ', 'Disclaimer', 'Moneycontrol', 'MoneyControl', 'moneycontrol']

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True

api = "https://www.moneycontrol.com/news/tags/mutual-funds/news/"
page = api
total = 0

for i in range(1, 31):
    response = requests.get(page)
    response_content = response.content
    # Parse the HTML content
    soup = BeautifulSoup(response_content, 'html.parser')
    li_elements = soup.find_all('li', class_='clearfix', id=lambda x: x and x.startswith('newslist-'))
    for j, li_element in enumerate(li_elements):
        h2_elements = li_element.find_all('h2')
        for h2 in h2_elements:
            isPremium = True if h2.find('span', class_="isPremiumCrown") else False
            isLiveBlog = True if h2.find('span', class_="lvb_icn") else False
            if isPremium:
                print(f"Premium article from page: {i}, blog: {j+1} has been skipped...")
                continue
            if isLiveBlog:
                print(f"Live Blog article from page: {i}, blog: {j+1} has been skipped...")
                continue
            # Extract <a> tags inside each <h2> tag
            a_tags = h2.find_all('a')
            for a_tag in a_tags:
                post_link = a_tag.get('href')
                blog_response = requests.get(post_link)
                blog_page = blog_response.content
                blog_soup = BeautifulSoup(blog_page, 'html.parser')
                try:
                  blog_title = "Title: " + blog_soup.find(class_='article_title').text + "\n\n"
                except:
                  print(f"Blog article from page: {i}, blog: {j+1} has been skipped due to non-article content...")
                  continue
                desc = blog_soup.find(class_='article_desc') or "NA"
                blog_desc = "Description: " + str(desc)  + "\n\n"
                blog_date = "Date: " + datetime.strptime(blog_soup.find('div', class_='article_schedule').find('span').text, "%B %d, %Y").strftime("%B %Y") + "\n\n"
                blog_contents = blog_soup.find(class_="content_wrapper").find_all('p')
                text_content = h.handle(''.join(str(blog_content) for blog_content in blog_contents))
                blog_categories = "Category: " + str([tag.text[1:].title() for tag in blog_soup.find(class_='tags_first_line').find_all('a')]) + "\n\n"
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
                file_path = '/content/moneycontrol_blogs_all.txt'

                # Append the filtered text and the delimiter to the file
                with open(file_path, 'a') as file:
                    file.write(blog_title + blog_date + blog_categories + blog_desc + filtered_text + delimiter)

                print(f"Filtered text from page: {i}, blog: {j+1} has been appended to {file_path}")
                total+=1

                # sleep_time = random.uniform(1, 10)
                # time.sleep(sleep_time)

    page = api +f"page-{i+1}/"
    # sleep_time = random.uniform(5, 10)
    # time.sleep(sleep_time)
    #             break
    #         break
    #     break
    # break
print(f"Total: {total}")