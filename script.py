 # -*- coding: utf-8 -*-

#Ghost docs http://ghost-py.readthedocs.org/en/latest/
#Ghost webpage http://jeanphix.me/Ghost.py/
#BS docs http://www.crummy.com/software/BeautifulSoup/bs4/doc/#

from bs4 import BeautifulSoup
from ghost import Ghost
import re, urllib

def printOptions(ops):
	rows = [str(idx)+'\t'+s for idx,s in enumerate(ops)]
	for row in rows:
		print row

def printFilenames(filenames):
	for name in filenames:
		print name

def getNamesAndUrlsFromSoup(soup):
	links = soup.find_all("a", { "id" : re.compile("GV_Datos_ctl.._lnkArchivo") })
	names = [link.getText() for link in links]
	urls = [link['href'] for link in links]
	return {'names':names, 'urls':urls}


#Secciones
ghost = Ghost(wait_timeout=20)
url = 'http://www3.inegi.org.mx/sistemas/descarga/?c=200'
ghost.open(url)
soup = BeautifulSoup(ghost.content)
res_sections = getNamesAndUrlsFromSoup(soup)

printOptions(res_sections['names'])
section = input('Selecciona una sección: ')

#Subsecciones
ghost.evaluate(res_sections['urls'][section], expect_loading=True) #Cargar alguna de las opciones
soup = BeautifulSoup(ghost.content)
res_subsections = getNamesAndUrlsFromSoup(soup)

printOptions(res_subsections['names'])
subsection = input('Selecciona una subsección: ')


#Carga listado de archivos
ghost.evaluate(res_subsections['urls'][subsection], expect_loading=True) #Cargar alguna de las opciones
soup = BeautifulSoup(ghost.content)
res_files = getNamesAndUrlsFromSoup(soup)

#Imprime listado de archivos
print 'Descargando...'
printFilenames(res_files['names'][1:])

urls = []
#Descarga del archivo
for href in res_files['urls'][1:]:
	ghost.evaluate(href, expect_loading=True) #Cargar alguna de las opciones
	soup = BeautifulSoup(ghost.content)
	url = soup.find_all("iframe", { "id" : "iFrameDescarga"})[0]['src']
	urls.append(url)

for i,url in enumerate(urls):
	urllib.urlretrieve(url, res_files['names'][i+1])
