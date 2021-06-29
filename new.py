from bs4 import BeautifulSoup
import requests
import csv

CSV = 'kivano.csv'
HOST = 'www.kivano.kg/'
URL = 'https://www.kivano.kg/planshety'

HEADERS = {
    'Accept' : 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, verify=False, params=params)
    return r

def planshets_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Description', 'Price', 'Link'])
        for item in items:
            writer.writerow([item['name'], item['description'], item['price'], item['link']])

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'item product_listbox oh')
    planshets_list = []
    for item in items:
        try:
            planshets_list.append({
                'name' : item.find('div', class_ = 'listbox_title oh').get_text(strip=True),
                'description' : item.find('div', class_ = 'product_text pull-left').get_text(strip=True),
                'price' : item.find('div', class_ = 'listbox_price text-center').get_text(strip=True),
                'link' : HOST + item.find('div', class_ = 'listbox_title oh').find('a').get('href'),
            })
        except:
            pass
    return planshets_list

def parse():
    PAGENATOR = input ('Enter value : ')
    PAGENATOR = int(PAGENATOR.strip())
    html = get_html(URL)
    if html.status_code == 200:
        planshets_list = []
        for page in range(1, PAGENATOR):
            print (f'Page {page} is parsed')
            html = get_html(URL, params={'page' : page})
            planshets_list.extend(get_content(html.text))
        planshets_save(planshets_list, CSV)
        print ('Parsed')
        return planshets_list
    else:
        print ('Error, not parsed')



parse()