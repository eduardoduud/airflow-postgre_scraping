from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import os
import csv

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}


driver = webdriver.Chrome(options=chrome_options)

driver.get("http://books.toscrape.com/catalogue/page-1.html")

page_content = driver.page_source

site = BeautifulSoup(page_content, "html.parser")

dadoslivros=[]
i=0
while(i<49):
    livros = site.findAll('li', attrs={'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

    for livro in livros:
        page_content = driver.page_source
        site = BeautifulSoup(page_content, "html.parser")
     
        nome = livro.find('h3').text
        preco = livro.find('p', attrs={'class': 'price_color'}).text
        estoque = livro.find('p', attrs={'class': 'instock availability'}).text.strip()

        nota=0
        if(livro.find('p', attrs={'class': 'star-rating One'})):
            nota + 1
        elif(livro.find('p', attrs={'class': 'star-rating Two'})):
            nota + 2
        elif(livro.find('p', attrs={'class': 'star-rating Three'})):
            nota + 3
        elif(livro.find('p', attrs={'class': 'star-rating Four'})):
            nota + 4
        else: nota + 5
        
        dadoslivros.append([nome, preco, nota, estoque])
    
    i += 1
    print(i)
    next = driver.find_element(By.CLASS_NAME, 'next a').click()

dados = pd.DataFrame(dadoslivros, columns=['Nome', 'Preço', 'Nota', 'Estoque'])
dados.to_csv('./dadoslivros.csv', index=False)

cmd = 'chmod 777 dadoslivros.csv'
os.system(cmd)

conn = psycopg2.connect(database="airflow",
                        user='airflow', password='airflow', 
                        host='host.docker.internal', port='5432'
)
  
conn.autocommit = True
cursor = conn.cursor()
  
with open('dadoslivros.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        cursor.execute(
        "INSERT INTO livros VALUES (%s, %s, %s, %s)",
        row
    )

conn.commit()
conn.close()