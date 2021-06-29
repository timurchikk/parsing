from bs4 import BeautifulSoup
import requests

def save():
    with open ('kivanophones.txt', 'a') as file:
        file.write (f"Name : {comp['name']}, Price : {comp['price']}, Desription : {comp['description']}")

def parse():
    URL = 'https://www.kivano.kg/mobilnye-telefony'
    HEADERS = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }

    response = requests.get(URL, HEADERS, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_ = 'item product_listbox oh')
    comps = []

    for item in items:
        try:
            comps.append({
                'name' : item.find('div', class_ = 'listbox_title oh').get_text(strip=True),
                'price' : item.find('div', class_ = 'motive_box pull-right').get_text(strip=True),
                'description' : item.find('div', class_ = 'product_text pull-left').get_text(strip=True)
            })
        except:
            pass


    global comp
    for comp in comps:
        print (f"Name : {comp['name']}, Price : {comp['price']}, Desription : {comp['description']}")
        save()
parse()