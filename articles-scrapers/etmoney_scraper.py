import html2text
import requests
from bs4 import BeautifulSoup
import time
import random
import re

def clean_text(text):
    # Replace newlines within sentences with a space
    if "|" not in text:
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Replace single newlines with spaces
    return text

# Filter out paragraphs containing any of the words or phrases
def contains_any(text, words_list):
    return any(word in text for word in words_list)

words_to_remove = ['ET Money', 'etmoney']

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True

api = "https://www.etmoney.com/learn/mutual-funds/"
page = api

for i in range(1, 29):
    response = requests.get(page)
    response_content = response.content
    # Parse the HTML content
    soup = BeautifulSoup(response_content, 'html.parser')
    # Find all elements with class 'post-list_body'
    posts = soup.find_all(class_='post-list_body')
    for j, post in enumerate(posts):
        h2_tag = post.find('h2', class_='entry-title')
        if h2_tag:
            a_tag = h2_tag.find('a')
            if a_tag:
                post_link = a_tag.get('href')
                blog_response = requests.get(post_link)
                blog_page = blog_response.content
                blog_soup = BeautifulSoup(blog_page, 'html.parser')
                blog_title = "Title: " + blog_soup.find(class_='entry-title').text + "\n\n"
                tags_class = blog_soup.find(class_="tag-cards_list")
                tags = tags_class.find_all('a')
                tags_list = [tag.text for tag in tags]
                blog_categories = "Category: " + str(tags_list) + "\n\n"
                blog_content = blog_soup.find_all(class_='entry-content')[0]

                text_content = h.handle(str(blog_content))

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
                file_path = '/content/etmoney_blogs.txt'

                # Append the filtered text and the delimiter to the file
                with open(file_path, 'a') as file:
                    file.write(blog_title + blog_categories + filtered_text + delimiter)

                print(f"Filtered text from page: {i}, blog: {j+1} has been appended to {file_path}")

                sleep_time = random.uniform(5, 10)
                time.sleep(sleep_time)
    page = api +f"page/{i+1}/"
    sleep_time = random.uniform(5, 10)
    time.sleep(sleep_time)
    #             break
    #         break
    #     break
    # break