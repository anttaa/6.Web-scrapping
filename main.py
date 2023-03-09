import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

HOST = "https://hh.ru/search/vacancy"
VACANCY = f"{HOST}?text=python&area=1&area=2"


def get_headers():
    return Headers(browser="firefox", os="win").generate()


def get_text(url):
    return requests.get(url, headers=get_headers()).text


def main():
    result = {"vacancies": []}
    html = get_text(f"{VACANCY}")
    soup = BeautifulSoup(html, features="html5lib")
    vacancies = soup.find_all(class_="serp-item") #.find_all("article")
    for item in vacancies:
        a = item.find(class_='serp-item__title')
        title = a.text
        price = item.find(class_='bloko-header-section-3').text
        if 'django' in title.lower() and 'flask' in title.lower() and 'usd' in price.lower():
            result['vacancies'].append({
                "link": a['href'],
                "price": price,
                "company": item.find(class_='bloko-link bloko-link_kind-tertiary').text,
                "town": item.find(attrs={'data-qa':'vacancy-serp__vacancy-address'}).text
            })
    return result


if __name__ == '__main__':
    result = main()
    with open('json_data.json', 'w') as f:
        json.dump(result, f)
