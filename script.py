 # -*- coding: utf-8 -*-

#Ghost docs http://ghost-py.readthedocs.org/en/latest/
#Ghost webpage http://jeanphix.me/Ghost.py/
#BS docs http://www.crummy.com/software/BeautifulSoup/bs4/doc/#

from bs4 import BeautifulSoup
from ghost import Ghost
import re, urllib

#Generate table for options
def printOptions(ops):
	rows = [str(idx)+'\t'+dic["name"]+'\t'+dic["type"] for idx,dic in enumerate(ops)]
	for row in rows:
		print row

#Print file names
def printFilenames(filenames):
	for name in filenames:
		print name

#Get names and URLs from file listing
def getNamesAndUrlsFromSoup(soup):
	links = soup.find_all("a", { "id" : re.compile("GV_Datos_ctl.._lnkArchivo") })
	names = [link.getText() for link in links]
	urls = [link['href'] for link in links]
	rows = soup.find_all("tr", { "class" : "TdCenso"})
	types = [list(row.children)[3].string for row in rows]
	#return {'names':names, 'urls':urls, 'types':types}
	return [{"name":a[0], "url":a[1], "type":a[2]} for a in zip(names,urls,types)]

#Open INEGI massive download website
ghost = Ghost(wait_timeout=20)
url = 'http://www3.inegi.org.mx/sistemas/descarga/'
ghost.open(url)
soup = BeautifulSoup(ghost.content)

#Parse sections
res_sections = getNamesAndUrlsFromSoup(soup)
#Print sections
printOptions(res_sections)

#Ask for a section number
section = input('Selecciona una sección: ')
#Check if value is valid
while not section in range(len(res_sections)):
	section = input('Opción incorrecta. Selecciona una sección: ')

#Scrape subsections
ghost.evaluate(res_sections['urls'][section], expect_loading=True) #Cargar alguna de las opciones
soup = BeautifulSoup(ghost.content)
res_subsections = getNamesAndUrlsFromSoup(soup)

#Print subsections
printOptions(res_subsections['names'])

subsection = input('Selecciona una subsección: ')
#Check if value is valid
while not subsection in range(len(res_subsections)):
	subsection = input('Opción incorrecta. Selecciona una subsección: ')


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
