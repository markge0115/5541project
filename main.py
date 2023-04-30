import requests
from bs4 import BeautifulSoup
import csv
import re

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
        english, chinese = definitions.split(' - ')
        # english = english.split(',')
        english = re.split(',|，|;', english)
        # chinese = chinese.split(',')
        chinese = re.split(',|，|;', chinese)
        with open('data/medical_translations.csv', 'a', newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)
            for i in english:
                for j in chinese:
                    writer.writerow([i, j])
    return 0

def get_n_pages(url):
    page_html = get_page_html(url)
    soup = BeautifulSoup(page_html, 'html.parser')
    # the text we want is nested in a structure: <div class="seasonnav"><h5> text <h5/></div>
    nav = soup.find('div', {'class': 'seasonnav'})
    # text should be in the form "<n> pages with <x> words"
    text = nav.h5.text
    numbers = re.findall(r'\d+', text)
    return int(numbers[0])


url = "https://dict.bioon.com/elite.asp?classid="
classids = [1,2,4,5,6,7,8,9,
            10,11,13,14,15,16,17,18,
            20,21,23,24,25,26,27, 
            32,36,60,61,                
            110,111,112,113,114,115,116,
            121,133]
url_page_suffix = "&page="

with open('data/medical_translations.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['English', 'Chinese'])

for classid in classids:
    classid_str = str(classid)
    url_no_page = url + classid_str + url_page_suffix
    n_pages = get_n_pages(url_no_page)

    for i in range(n_pages):
        num = str(i+1)
        url_ = url + classid_str + url_page_suffix + num
        with open('data/medical_translations.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # writer.writerow(['Page ' + num])
        page_html = get_page_html(url_)
        find_word_list(page_html)
