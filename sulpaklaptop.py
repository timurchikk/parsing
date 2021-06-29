from bs4 import BeautifulSoup
import requests

def save():
    with open('sulpakparse.txt', 'a') as file:
        file.writelines(f"Naming : {comp['title']}, Price : {comp['price']}, Link : {comp['link']}\n")

def parse():
    URL = 'https://www.sulpak.kg/f/noutbuki'
    HEADERS = {
        'Accept' : 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

    response =  requests.get(URL, headers = HEADERS, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_= 'goods-tiles')
    comps = []

    for i in items:
        try:
            comps.append({
                'title' : i.find('h3', class_ = 'title').get_text(strip=True),
                'price' : i.find('div', class_ = 'price').get_text(strip=True),
                'link' : URL + i.find('div', class_ = 'product-container-right-side').find('a').get('href'),
            })
        except:
            pass
    global comp
    for comp in comps:
        print (f"Naming : {comp['title']}, Price : {comp['price']}, Link : {comp['link']}\n")
        save()


parse()