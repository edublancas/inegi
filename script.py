 # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from ghost import Ghost
import re, urllib, sys

#Generate table for options
def printOptions(ops):
    rows = [str(idx)+'\t'+dic["name"]+('/' if dic["type"]=='menu' else 
         " "+dic["type"]) for idx,dic in enumerate(ops)]
    for row in rows:
        print row

#Print file names
def printFilenames(ops):
    #Skip back button if exists
    if res_files[0]["type"]=="back":
        res_files.pop(0)

    filenames = [dic["name"] for dic in ops]
    for name in filenames:
        print name

def findOptionType(op):
    p = re.compile('\[[0-9]{2}')
    type = None
    if op["type"]=="Dir" and p.match(op["name"]):
        type = "folder"
    elif op["type"]=="Dir":
        type = "menu"
    elif op["type"]==u'\xa0':
        type = "back"
    else:
        type = "file"
    return {"name":op["name"], "url":op["url"], "type":type}

def scrapeFileDirectLinks(files):
    urls = []
    #Descarga del archivo
    for href in [dic["url"] for dic in files]:
        ghost.evaluate(href, expect_loading=True) #Cargar alguna de las opciones
        soup = BeautifulSoup(ghost.content)
        url = soup.find_all("iframe", { "id" : "iFrameDescarga"})[0]['src']
        urls.append(url)
    return urls

def getFiles(res_files):
    #Skip back button if exists
    if res_files[0]["type"]=="back":
        res_files.pop(0)

    urls = scrapeFileDirectLinks(res_files)
    names = [dic["name"] for dic in res_files]
    if (sys.argv[1]):
        text_file = open(sys.argv[1], "aw+")
        for url in urls:
            text_file.write(url+"\n")
        text_file.close()
    else:
        for i,url in enumerate(urls):
            urllib.urlretrieve(url, names[i])


#Get names, URLs and types from list
def getNamesAndUrlsFromSoup(soup):
    links = soup.find_all("a", { "id" : re.compile("GV_Datos_ctl.._lnkArchivo") })
    names = [link.getText() for link in links]
    urls = [link['href'] for link in links]
    rows = soup.find_all("tr", { "class" : "TdCenso"})
    types = [list(row.children)[3].string for row in rows]
    #There are four types of options:
    #1 - Menu (more options) - menu
    #2 - Directory (Folder full of files) - dir
    #3 - File Single file - file
    #4 - Link back - back
    #Based on the name and the type, classify options
    dic = [{"name":a[0], "url":a[1], "type":a[2]} for a in zip(names,urls,types)]
    dic = [findOptionType(op) for op in dic]
    return dic

def bulkDownloadAvailable(res_sections):
    types = [dic["type"] for dic in res_sections]
    if "menu" in types:
        return False
    else:
        return True

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
section = int(raw_input('Selecciona una opción: '))
#Check if value is valid
while not section in range(len(res_sections)):
    section = int(raw_input('Opción incorrecta. Selecciona una sección: '))

selection = res_sections[int(section)]["type"]

continue_ = True

while continue_:
    #Check type of selection menu/folder with files
    #If menu, load new page and print listings
    if selection == "menu" or selection == "back":
        #Scrape sections
        ghost.evaluate(res_sections[int(section)]['url'], expect_loading=True) #Cargar alguna de las opciones
        soup = BeautifulSoup(ghost.content)
        res_sections = getNamesAndUrlsFromSoup(soup)

        #Check if bulk download is available
        canBulkDownload = bulkDownloadAvailable(res_sections)
        if canBulkDownload:
            res_sections.append({"name":"Descargar todo", "url":"", "type":"bulk"})

        #Print sections
        printOptions(res_sections)
        section = int(raw_input('Selecciona una subsección: '))
        #Check if value is valid
        while not section in range(len(res_sections)):
            section = int(raw_input('Opción incorrecta. Selecciona una subsección: '))
        selection = res_sections[int(section)]["type"]
    #If folder, download all the files
    elif selection=="folder":
        #Load file listing
        ghost.evaluate(res_sections[int(section)]['url'], expect_loading=True) #Cargar alguna de las opciones
        soup = BeautifulSoup(ghost.content)
        res_files = getNamesAndUrlsFromSoup(soup)
        #Imprime listado de archivos
        print 'Descargando...'
        printFilenames(res_files)
        getFiles(res_files)
        answer = raw_input('¿Continuar ejecución? (y/n): ').lower()
        while not (answer=="y" or answer=="n"):
            answer = raw_input('¿Continuar ejecución? (y/n): ')
        if answer=="y":
            continue_ = True
            #Simulate click on back button
            selection = "back"
            section = 0
        else:
            continue_ = False
    #If file, download single file
    elif selection=="file":
        res_files = getNamesAndUrlsFromSoup(soup)
        selected_file =  res_files[int(section)]
        print 'Descargando...'
        printFilenames([selected_file])
        getFiles([selected_file])
        answer = raw_input('¿Continuar ejecución? (y/n): ').lower()
        while not (answer=="y" or answer=="n"):
            answer = raw_input('¿Continuar ejecución? (y/n): ')
        if answer=="y":
            continue_ = True
            #Simulate click on back button
            selection = "back"
            section = 0
        else:
            continue_ = False
    elif selection=="bulk":
        print "Iniciando descarga masiva..."
        res_resources = getNamesAndUrlsFromSoup(soup)
        for resource in res_resources:
            if resource["type"] == "folder":
                ghost.evaluate(resource['url'], expect_loading=True)
                soup = BeautifulSoup(ghost.content)
                res_files = getNamesAndUrlsFromSoup(soup)
                #Imprime listado de archivos
                print 'Descargando...'
                printFilenames(res_files)
                getFiles(res_files)
                #Simulate back button
                ghost.evaluate(res_resources[0]['url'], expect_loading=True)
            elif resource["type"] == "file":
                #res_files = getNamesAndUrlsFromSoup(soup)
                #selected_file =  res_files[int(section)]
                print 'Descargando...'
                #printFilenames([selected_file])
                #getFiles([selected_file])
            else:
                print "Unknown resources. Skipping."

        answer = raw_input('¿Continuar ejecución? (y/n): ').lower()
        while not (answer=="y" or answer=="n"):
            answer = raw_input('¿Continuar ejecución? (y/n): ')
        if answer=="y":
            continue_ = True
            #Simulate click on back button
            selection = "back"
            section = 0
        else:
            continue_ = False
    else:
        print "Unkwown option"
        continue_ = False