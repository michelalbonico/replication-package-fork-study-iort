from ast import Index
import sqlite3
from click import echo
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
import contextlib
#from selenium.webdriver.common.by import By

## Install Chrome Driver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#
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
page_fork = []


# Final_List

class Repository:
    def __init__(self,project_url, last_update_source, forks, url_fork, last_update_fork, commits_behind):
        
        self.project_url = project_url
        self.last_update_source = last_update_source
        self.forks = forks
        self.url_fork = url_fork
        self.last_update_fork = last_update_fork
        self.commits_behind = commits_behind

def insert_data():
    conn = sqlite3.connect('/home/estagio/Área de Trabalho/dataBaseSqLite/finalList.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS repository(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        source_project_url varchar(240),
        last_update_source varchar(240),
        forks int,
        url_fork varchar(240),
        last_update_fork varchar(240),
        commits_behind varchar(240)
    );
    ''')

    time.sleep(1)
    print('Tabela criada com sucesso.')
    for repo in repositoryArray:
        #print(repo.link)
        cursor.execute('''
            INSERT INTO repository (source_project_url, last_update_source, forks, url_fork, last_update_fork, commits_behind)
             VALUES (?,?,?,?,?,?)
            ''', (repo.project_url, repo.last_update_source, repo.forks, repo.url_fork, repo.last_update_fork, repo.commits_behind))
        conn.commit()
    conn.close()
    del repo

def get_data(urls):
    for url in urls:
        chrome.get(url)
        time.sleep(2)
        #print(url)
        #print('-----------')
        try:
            last_update_source = chrome.find_elements_by_css_selector('a[href*="commit"] > relative-time')[0].text
        except NoSuchElementException:
            last_update_source = 'None' 
        except IndexError:
            last_update_source = 'None'
        #print(last_update_source)
        #print('-----------')
        try:
            forks = chrome.find_elements_by_css_selector('a[href*="members"] > strong')[0].text
        except NoSuchElementException:
            forks = 'None'
        except IndexError:
            forks = 'None'
        #print(forks)
        #print('-----------')
        time.sleep(1)
        try:
            fork_element = chrome.find_element_by_css_selector('a[href*="members"] > strong')
            time.sleep(2)
            fork_element.click()
        except ElementNotInteractableException:
            fork_element.click()
        time.sleep(2)
        class_repo = chrome.find_elements_by_class_name("repo")
        for repo in class_repo:
            tag_a = repo.find_elements_by_css_selector('a')[2]
            link_fork = tag_a.get_attribute('href')
            page_fork.append(link_fork)
    if page_fork == []:
        url_fork = 'None'    
        last_update_fork = 'None'
        commits_behind = 'None'
        repositoryArray.append(
            Repository(project_url, last_update_source, forks, url_fork, last_update_fork, commits_behind))
      
    else:
        del page_fork[0]     
        #print(page_fork)
        #print('-----------')
        for url_fork in page_fork:
            #print('fork')
            chrome.get(url_fork)
            #print("\n--- Searching for " + url_fork + " ---\n")
            time.sleep(2)
            try:
                last_update_fork = chrome.find_elements_by_css_selector('a[href*="commit"] > relative-time')[0].text
            except NoSuchElementException:
                last_update_fork = 'None' 
            except IndexError:
                last_update_fork= 'None'
            #print(last_update_fork)
            #print('-----------')
            try:
                commits_behind= chrome.find_elements_by_css_selector('div[class="d-flex flex-auto"]')[0].text
            except NoSuchElementException:
                commits_behind = 'None'
            except IndexError:
                commits_behind = 'None'
            #print(commits_behind)
            #print('-----------')
            time.sleep(1)
            repositoryArray.append(
                Repository(project_url, last_update_source, forks, url_fork, last_update_fork, commits_behind))
        page_fork.clear()
        time.sleep(5)

options = Options()
# options.add_argument('--headless')
#chrome = webdriver.Chrome(executable_path='./driver/chromedriver', options=options)
chrome = webdriver.Chrome(ChromeDriverManager().install())
wait = ui.WebDriverWait(chrome,10)

for project_url in search:
    print('init')
    #chrome.get('https://chrome.com/search?project_url=\"' + project_url.replace(" ", "+") + '\"')
    chrome.get(project_url.replace(" ", "+"))
    print("\n--- Searching for " + project_url + " ---\n")
    time.sleep(3)
    urls.append(project_url)
    #print(urls)
    get_data(urls)
    insert_data()
    del repositoryArray
    del urls
    urls = []
    repositoryArray = []