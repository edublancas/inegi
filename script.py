 # -*- coding: utf-8 -*-

#Ghost docs http://ghost-py.readthedocs.org/en/latest/
#Ghost webpage http://jeanphix.me/Ghost.py/
#BS docs http://www.crummy.com/software/BeautifulSoup/bs4/doc/#

from bs4 import BeautifulSoup
from ghost import Ghost
import re, urllib

#Secciones

ghost = Ghost(wait_timeout=20)
url = 'http://www3.inegi.org.mx/sistemas/descarga/?c=200'
ghost.open(url)
soup = BeautifulSoup(ghost.content)

links = soup.find_all("a", { "id" : re.compile("GV_Datos_ctl.._lnkArchivo") })
names = [link.getText() for link in links]
hrefs = [link['href'] for link in links]

print names

section = input('Selecciona una sección: ')

#Subsecciones
ghost.evaluate(hrefs[section], expect_loading=True) #Cargar alguna de las opciones
soup = BeautifulSoup(ghost.content)
links = soup.find_all("a", { "id" : re.compile("GV_Datos_ctl.._lnkArchivo") })
names = [link.getText() for link in links]
hrefs = [link['href'] for link in links]

print names

subsection = input('Selecciona una subsección: ')


#Carga listado de archivos
ghost.evaluate(hrefs[subsection], expect_loading=True) #Cargar alguna de las opciones
soup = BeautifulSoup(ghost.content)
links = soup.find_all("a", { "id" : re.compile("GV_Datos_ctl.._lnkArchivo") })
names = [link.getText() for link in links]
hrefs = [link['href'] for link in links]

#Imprime listado de archivos
print names

urls = []
#Descarga del archivo
for href in hrefs[1:]:
	ghost.evaluate(href, expect_loading=True) #Cargar alguna de las opciones
	soup = BeautifulSoup(ghost.content)
	url = soup.find_all("iframe", { "id" : "iFrameDescarga"})[0]['src']
	urls.append(url)

urls

for i,url in enumerate(urls):
	urllib.urlretrieve(url, names[i+1])
