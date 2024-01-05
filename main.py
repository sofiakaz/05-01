import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

#serp-item

headers_generator = Headers(os='win', browser='chrome')

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_generator.generate())
html_data = response.text

soup = BeautifulSoup(html_data, 'lxml')

# Find all elements with class 'vacancy-serp-item'
announcement_list = soup.find_all('div', {'class': 'serp-item'})

vacancies = []

for announcement in announcement_list:
    city_tag = announcement.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    city = city_tag.text.strip()

    link_tag = announcement.find('a', {'class': 'serp-item__title'})
    link = link_tag['href']

    vacancy_response = requests.get(link, headers=headers_generator.generate())
    vacancy_html = vacancy_response.text
    soup_v = BeautifulSoup(vacancy_html, 'lxml')

    key_skills = soup_v.find_all('span', {'class': 'bloko-tag__section bloko-tag__section_text'})
    key_skills_list = [skill.text.strip() for skill in key_skills]

    price_tag = announcement.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if price_tag:
        price = price_tag.text.strip().replace('NNBSP', ' ')
    else:
        price = None

    company_tag = announcement.find('div', {'class': 'vacancy-serp-item__meta-info-company'})
    company = company_tag.text.strip().replace('\xa0', ' ')

    if (city.startswith("Москва") or city.startswith('Санкт-Петербург')) and (any(word.startswith(('Flask', 'Django')) for word in key_skills_list)):

        vacancies.append({
            'link': link,
            'salary': price,
            'company': company,
            'city': city
        })

with open('vacancies.json', 'w', encoding='utf-8') as json_file:
    json.dump(vacancies, json_file, ensure_ascii=False, indent=4)




