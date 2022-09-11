import json
import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.119 Mobile Safari/537.36'
}


# Получение html страницы на компьютер
def get_html(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers, verify=False)

    with open('index1.html', 'w', encoding="utf-8") as file:
        file.write(response.text)


# Получение ссылок на профили всех преподавателей
def get_articles_urls(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers, verify=False)

    soup = BeautifulSoup(response.text, 'lxml')

    articles_urls = soup.find_all(href=re.compile("/company/personal/user/"))

    articles_urls_list = []
    for au in articles_urls:
        art_url = au.get('href')
        articles_urls_list.append(art_url)

    with open('articles_urls.txt', 'w') as file:
        for url in articles_urls_list:
            file.write(f'https://sibsutis.ru{url}\n')
    print('Ссылки на преподавателей были успешно получены!')


# Получение выбранных данных с преподавателя
def get_data(file_path):
    with open(file_path) as file:
        urls_list = [line.strip() for line in file.readlines()]

    s = requests.Session()

    result_list = []
    count = 1
    for url in urls_list:
        get_data_with_selenium(url, count)
        with open(f"html_pages/index_selenium_{count}.html", encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")

        try:
            fio = soup.find('div', class_='head_wrap').find('h1').text.strip()
        except Exception as ex:
            fio = '-'

        try:
            phone = soup.find('a', href=re.compile("callto:")).text.strip()
        except Exception as ex:
            phone = '-'

        try:
            email = soup.find('a', href=re.compile("mailto")).text.strip()
        except Exception as ex:
            email = '-'

        departments_list = []
        try:
            departments = soup.find_all('a', href=re.compile("/students/info/studpoisk/structure/"))
        except Exception as ex:
            departments = '-'
        for department in departments:
            department_text = department.text
            departments_list.append(department_text)
        departments_list = (", ".join(departments_list))
        # print(f'фио:{fio}\nтелефон:{phone}\nemail:{email}\nдепартамент:{departments_list}\n')

        result_list.append(
            {
                'fio': fio,
                'phone': phone,
                'email': email,
                'departments': departments_list,
                'url': url
            }
        )
        print(f'Преподаватель №{count} обработан!')
        count = count + 1
        time.sleep(4)
    with open('result.json', 'w') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
    print('Все данные успешно добавлены!')


# Получение html страницы с помощью selenium для загрузки дополнительных данных
def get_data_with_selenium(url, count):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(
        executable_path="D:/учёба/4 курс/диплом/My_Bot/parser/chromedriver",
        chrome_options=chrome_options
    )
    driver.get(url=url)
    time.sleep(4)

    with open(f"html_pages/index_selenium_{count}.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    driver.close()
    driver.quit()


def main():
    get_articles_urls('https://sibsutis.ru/students/info/studpoisk/preppoisk/?SHOWALL_1=1')
    get_data('articles_urls.txt')


if __name__ == '__main__':
    main()
