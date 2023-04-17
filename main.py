import requests
from bs4 import BeautifulSoup
import csv

def get_page_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    page = requests.get(url, headers=headers)
    print(page.status_code)
    return page.content

def find_word_list(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    word_list = soup.find("ul", {"id": "wordlist"})  # <--- change "text" to div
    rows = word_list.find_all('li')
    for i in rows:
        definitions = i.find('a').text
        tuple = definitions.split(' - ')
        with open('medical_translations.csv', 'a', newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([tuple[0], tuple[1]])
    return 0


url = "https://dict.bioon.com/elite.asp?classid=7&page="
with open('medical_translations.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['English', 'Chinese'])
for i in range(5):
    num = str(i+1)
    url_ = url + num
    with open('medical_translations.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Page ' + num])
    page_html = get_page_html(url_)
    find_word_list(page_html)
