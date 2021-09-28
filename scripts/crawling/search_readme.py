import sqlite3
import time
import requests
from bs4 import BeautifulSoup


startRow = 25685+30299
conn = sqlite3.connect('./data/repos.db')
c = conn.cursor()
c.execute('SELECT url FROM repos WHERE rowid > '+str(startRow))
coluna_url = c.fetchall()
c.close()
#Gerando e fazendo conexão com DB
#database = 'readme.db'  
con = sqlite3.connect('./data/readme.db')

#Gerando a tabela readme
con.execute('''
    CREATE TABLE IF NOT EXISTS readme_table(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        url_repository TEXT,
        readme_element TEXT);
    ''')
count = 1
tamanho = len(coluna_url)
inic = 0
fim = 200
erro=True
while count < tamanho:
    for link in coluna_url[inic:fim]:
        print(link)
        while erro:
            print("Tentando conectar em ",link)
            try:
                page = requests.get(link[0])
                erro=False
            except:
                erro=True
                print("Erro ao conectar!")
            time.sleep(2)
        erro=True
        print(page.status_code)
        soup = BeautifulSoup(page.content,'html.parser')
        try:
            tag_article = soup.find_all('article', class_='markdown-body entry-content container-lg')[0].get_text()
        except IndexError:
            tag_article = 'Null'
        con.execute("""INSERT INTO readme_table(url_repository,readme_element)
                               VALUES(?,?)""",(str(link[0]),tag_article,))
        con.commit()
        time.sleep(2) 
    count += 200
    inic += 200
    fim += 200
    print('=' * 10)
    time.sleep(10)
con.close()
