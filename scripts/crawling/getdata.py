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
#fork_url = []
url_fork = []


# , 'Iot', 'Internet of things', 'Internet das coisas'


class Repository:
    def __init__(self,forks, url_fork, last_update_source, last_update_fork, commits_behind):
        

        #self.source_project_url = source_project_url
        self.forks = forks
        self.url_fork = url_fork
        self.last_update_source = last_update_source
        self.last_update_fork = last_update_fork
        self.commits_behind = commits_behind

def insert_data(q):
    q = q.replace(" ", "_")
    conn = sqlite3.connect('data/final_list_' + q + '.bd')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS repository(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        forks int,
        url_fork varchar(240),
        last_update_source varchar(240),
        last_update_fork varchar(240),
        commits_behind varchar(240)
    );
    ''')

    time.sleep(1)

    for repo in repositoryArray:
        print(repo.link)
        cursor.execute('''
            INSERT INTO repository ( forks, url_fork, last_update_source, last_update_fork, commits_behind)
             VALUES (?,?,?,?,?)
            ''', (repo.forks, repo.url_fork, repo.last_update_source, repo.last_update_fork, repo.commits_behind))

        conn.commit()

    conn.close()

    del repo

def get_data(urls):
    for url in urls:
        chrome.get(url)
        time.sleep(3)
       
        print(url)
        print('-----------')

        try:
            last_update_source = chrome.find_elements_by_css_selector('a[href*="commit"] > relative-time')[0].text
        except NoSuchElementException:
            last_update_source = 'None' 
        except IndexError:
            last_update_source = 'None'

        
        print(last_update_source)
        print('-----------')
        
        try:
            forks = chrome.find_elements_by_css_selector('a[href*="members"] > strong')[0].text
        except NoSuchElementException:
            forks = 'None'
        except IndexError:
            forks = 'None'

        print(forks)
        print('-----------')
        
        try:
            
            fork_element = chrome.find_element_by_css_selector('a[href*="members"] > strong')
            fork_element.click()
            
        except ElementNotInteractableException:
            fork_element.click()

        
        time.sleep(3)

        class_repo = chrome.find_elements_by_class_name("repo")
        for repo in class_repo:
            tag_a = repo.find_elements_by_css_selector('a')[2]
            link_fork = tag_a.get_attribute('href')
            url_fork.append(link_fork)

    del url_fork[0]     
    print(url_fork)
    print('-----------')

    for page_fork in url_fork:
        print('fork')
        chrome.get(page_fork)
        print("\n--- Searching for " + page_fork + " ---\n")
        time.sleep(3)
        try:
            last_update_fork = chrome.find_elements_by_css_selector('a[href*="commit"] > relative-time')[0].text
        except NoSuchElementException:
            last_update_fork = 'None' 
        except IndexError:
            last_update_fork= 'None'

       
        print(last_update_fork)
        print('-----------')
        

        try:
            commits_behind= chrome.find_elements_by_css_selector('div[class="d-flex flex-auto"]')[0].text
        except NoSuchElementException:
            commits_behind = 'None'
        except IndexError:
            commits_behind = 'None'
            

        print(commits_behind)
        print('-----------')

        time.sleep(3)

    repositoryArray.append(
        Repository(last_update_source, forks, url_fork,last_update_fork, commits_behind))
    url_fork.clear()
    
    time.sleep(5)
       
    


options = Options()
# options.add_argument('--headless')
#chrome = webdriver.Chrome(executable_path='./driver/chromedriver', options=options)
chrome = webdriver.Chrome(ChromeDriverManager().install())
wait = ui.WebDriverWait(chrome,10)


for q in search:
    print('init')
    #chrome.get(q.replace(" ", "+"))
    chrome.get('https://github.com/search?q=\"' + q.replace(" ", "+") + '\"')
    print("\n--- Searching for " + q + " ---\n")

    time.sleep(3)

    urls.append(q)
    #print(urls)
    
    get_data(urls)
    del repositoryArray
    del urls
    urls = []
    repositoryArray = []