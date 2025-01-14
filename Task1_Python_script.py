# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7

import os
import requests
import re
from bs4 import BeautifulSoup  # Code here - Import BeautifulSoup library

# Code ends here

# Function to get the HTML source text of the Medium article
def get_page():
    global url

    # Code here - Ask the user to input "Enter url of a medium article: " and collect it in url
    url = input("Enter url of a medium article: ").strip()
    # Code ends here

    # Handling possible error
    if not re.match(r'https?://medium.com/', url):
        print('Please enter a valid website, or make sure it is a medium article')
        sys.exit(1)

    # Code here - Call get method in requests object, pass url and collect it in res
    res = requests.get(url)
    # Code ends here

    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

# Function to remove all the HTML tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>": "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub(r'\<(.*?)\>', '', text)
    return text

# Function to collect the text content from the parsed HTML
def collect_text(soup):
    text = f'url: {url}\n\n'
    
    # Find the main article body based on class names or other unique attributes
    article_body = soup.find_all('p', class_="pw-post-body-paragraph")
    
    if not article_body:
        print("Could not find article content. Ensure the script is scraping the right section.")
        return ""

    # Extract text from each paragraph
    for para in article_body:
        text += f"{para.text.strip()}\n\n"

    return text

# Function to save the file in the current directory
def save_file(text):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    name = url.split("/")[-1]
    print(name)
    fname = f'scraped_articles/{name}.txt'

    # Code here - write a file using with (2 lines)
    with open(fname, 'w', encoding='utf-8') as file:
        file.write(text)
    # Code ends here

    print(f'File saved in directory {fname}')


if __name__ == '__main__':
    text = collect_text(get_page())
    save_file(text)
    # Instructions to Run this python code
    # Give url as https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7