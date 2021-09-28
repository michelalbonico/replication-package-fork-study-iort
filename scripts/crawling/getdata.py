import sqlite3
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
import contextlib

## Install Chrome Driver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


## Reading Keywords
search = []
f = open("keywords", "r")
for line in f:
  print("Keyword: ", line)
  search.append(line)
##

repositoryArray = []
next_exists = False
urls = []


# , 'Iot', 'Internet of things', 'Internet das coisas'


class Repository:
    def __init__(self, username, name, link, about, description, contributors, languages, stars, last_updated, commits, issues_open, issues_closed):
        self.username = username
        self.name = name
        self.link = link
        self.about = about
        self.description = description
        self.contributors = contributors
        self.languages = languages
        self.stars = stars
        self.last_updated = last_updated
        self.commits = commits
        self.issues_open = issues_open
        self.issues_closed = issues_closed

def insert_data(q):
    q = q.replace(" ", "_")
    conn = sqlite3.connect('data/snowballing_' + q + '.bd')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS repository(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username varchar(240),
        name varchar(240),
        link varchar(240),
        about varchar(240),
        description varchar(240),
        contributors varchar(240),
        languages varchar(540),
        stars varchar(240),
        last_updated varchar(240),
        commits int,
        issues_open int,
        issues_closed int
    );
    ''')
    time.sleep(1)
    for repo in repositoryArray:
        print(repo.link)
        cursor.execute('''
            INSERT INTO repository (username, name, link, about, description, contributors, languages, stars, last_updated, commits, issues_open, issues_closed)
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (repo.username, repo.name, repo.link, repo.about, repo.description, repo.contributors, repo.languages,
                  repo.stars, repo.last_updated, repo.commits, repo.issues_open, repo.issues_closed))

        conn.commit()

    conn.close()

    del repo

def get_data(urls):
    for url in urls:
        chrome.get(url)
        time.sleep(5)
        print('-----------')
        print(url)

        try:
            #author
            username = chrome.find_elements_by_css_selector('a[rel="author"]')[0].text
        except NoSuchElementException:
            username = 'None'

        try:
            name = chrome.find_elements_by_css_selector('strong[itemprop="name"]')[0].text
        except NoSuchElementException:
            name = 'None'

        try:
            about = chrome.find_elements_by_css_selector('.BorderGrid > .BorderGrid-row > div > p')[0].text
        except NoSuchElementException:
            about = 'None'
        except IndexError:
            about = 'None'

        try:
            description = chrome.find_elements_by_css_selector('article[itemprop="text"]')[0].text
        except NoSuchElementException:
            description = 'None'
        except IndexError:
            description = 'None'

        try:
            contributors = chrome.find_elements_by_css_selector('a[href*="contributors"] > span')[0].text
        except NoSuchElementException:
            contributors = 'None'
        except IndexError:
            contributors = 'None'

        try:
            languages = ""
            languages_element = chrome.find_elements_by_css_selector('a[data-ga-click="Repository, language stats search click, location:repo overview"]')
            for lang in languages_element:
                languages += lang.text
            if languages == "":
                languages = 'None'
        except NoSuchElementException:
            languages = 'None'
        except IndexError:
            languages = 'None'

        try:
            stars = chrome.find_elements_by_css_selector('a[href*="stargazers"')[0].text
        except NoSuchElementException:
            stars = 'None'
        except IndexError:
            stars = 'None'

        try:
            last_updated = chrome.find_elements_by_css_selector('a[href*="commit"] > relative-time')[0].text
        except NoSuchElementException:
            last_updated = 'None'
        except IndexError:
            last_updated = 'None'

        try:
            commits = chrome.find_elements_by_css_selector('a[href*="commits"] > span > strong')[0].text
        except NoSuchElementException:
            commits = 'None'
        except IndexError:
            commits = 'None'

        try:
            issues_element = chrome.find_elements_by_css_selector('[href*="issues"]')
            issues_element[0].click()

            issues_open = chrome.find_elements_by_css_selector('a[data-ga-click="Issues, Table state, Open"]')[0].text
            issues_closed = chrome.find_elements_by_css_selector('a[data-ga-click="Issues, Table state, Closed"]')[0].text

        except ElementNotInteractableException:
            issues_element.click()

            issues_open = chrome.find_elements_by_css_selector('a[data-ga-click="Issues, Table state, Open"]')[0].text
            issues_closed = chrome.find_elements_by_css_selector('a[data-ga-click="Issues, Table state, Closed"]')[0].text
        except NoSuchElementException:
            issues_open = '0 open'
            issues_closed = '0 closed'
        except IndexError:
            issues_open = '0 open'
            issues_closed = '0 closed'

        repositoryArray.append(
            Repository(username, name, url, about, description, contributors, languages, stars, last_updated, commits,
                       issues_open, issues_closed))

        time.sleep(10)


options = Options()
# options.add_argument('--headless')
#chrome = webdriver.Chrome(executable_path='./driver/chromedriver', options=options)
chrome = webdriver.Chrome(ChromeDriverManager().install())
wait = ui.WebDriverWait(chrome,10)

for q in search:
    print('init')
    chrome.get('https://github.com/search?q=\"' + q.replace(" ", "+") + '\"')
    print("\n--- Searching for " + q + " ---\n")
    time.sleep(5)

    html_list = chrome.find_element_by_class_name("repo-list")
    items = html_list.find_elements_by_tag_name("li")

    for item in items:
        first_div = item.find_element_by_class_name("mt-n1")
        second_div = first_div.find_element_by_class_name("f4")
        tag_a = second_div.find_element_by_class_name("v-align-middle")
        link = tag_a.get_attribute("href")
        urls.append(link)
        print(urls)

    try:
        next_page = chrome.find_element_by_class_name('next_page')
        next_page_class = next_page.get_attribute('class')
        if 'disable' in next_page_class:
            next_exists = False
        else:
            next_exists = True
        print(next_exists)
    except NoSuchElementException:
        print('None')

    while next_exists:
        try:
            next_page.click()
            time.sleep(5)
            html_list = wait.until(lambda driver: chrome.find_element_by_class_name("repo-list"))
            items = wait.until(lambda driver: html_list.find_elements_by_tag_name("li"))
            time.sleep(1)
            for item in items:
                first_div = wait.until(lambda driver: item.find_element_by_class_name("mt-n1"))
                second_div = wait.until(lambda driver: first_div.find_element_by_class_name("f4"))
                tag_a = wait.until(lambda driver: second_div.find_element_by_class_name("v-align-middle"))
                link = tag_a.get_attribute("href")
                urls.append(link)
                print(urls)
                next_page = wait.until(lambda driver: chrome.find_element_by_class_name('next_page'))
                next_page_class = wait.until(lambda driver: next_page.get_attribute('class'))
                if 'disable' in next_page_class:
                    next_exists = False
                    print('disable')
                else:
                    next_exists = True
        except NoSuchElementException:
            print('None')
    get_data(urls)
    insert_data(q)
    del repositoryArray
    del urls
    urls = []
    repositoryArray = []
