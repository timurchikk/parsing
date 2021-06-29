from bs4 import BeautifulSoup
import requests
import csv

CSV = 'minfin.csv'
HOST = 'www.minfin.kg/ru/'
URL = 'http://www.minfin.kg/ru/novosti/mamlekettik-karyz/gosudarstvennyy-dolg'
HEADERS = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, verify=False, params=params)
    return r

def news_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Day of publication', 'News', 'Link'])
        for item in items:
            writer.writerow([item['date'], item['title'], item['link']])

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'news')
    news_list = []
    for item in items:
        try:
            news_list.append({
                'date': item.find('div', class_ = 'news_date').get_text(strip=True),
                'title': item.find('div', class_ = 'news_name').get_text(strip=True),
                'link': HOST +  item.find('div', class_ = 'news_name').find('a').get('href'),
            })
        except:
            pass
    return news_list
    

def parse():
    PAGENATOR = input ('Коли - во страниц : ')
    PAGENATOR = int(PAGENATOR.strip())
    html = get_html(URL)
    if html.status_code == 200:
        news_list = []
        for page in range (1, PAGENATOR):
            print (f'Page {page} parsed')
            html = get_html(URL, params={'page':page})
            news_list.extend(get_content(html.text))
        news_save(news_list, CSV)
        print ('Parsed')
        return news_list
    else:
        print ('error')

    


parse()
