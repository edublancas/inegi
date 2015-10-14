#Descarga masiva del INEGI
Este programa permite descargar archivos de la sección de [Descarga Masiva del INEGI](http://www3.inegi.org.mx/sistemas/descarga/).

Archivos disponibles para descarga:

* Censo de escuelas, maestros y alumnos de educación básica y especial (CEMABE) 
* Directorio Estadístico Nacional de Unidades Económicas (DENUE) 
* Censos económicos
* Censos y conteos de población y vivienda
* Encuestas en establecimientos
    * Encuesta mensual de la industria manufacturera   
* Encuestas en hogares
    * Encuesta nacional de ocupación y empleo
* PIB y sistema de cuentas nacionales de México
* Registros administrativos
    * Accidentes de tránsito terrestre en zonas urbanas y suburbanas
    * Estadísticas de Vehículos de Motor Registrados
    * Finanzas públicas estatales y municipales
    * Industria minerometalúrgica
    * Judiciales en materia penal
    * Natalidad, mortalidad y nupcialidad
    * Relaciones laborales de jurisdicción laboral
    
##Descargando archivos sin correr el script

En el repositorio se encuentran disponibles archivos de texto con links directos para obtener estudios completos del INEGI. Cada estudio se actualiza en periodos diferentes, para asegurar que cuenta con la última versión use el script.

##Dependencias

Para poder correr el script es necesario tener instalado lo siguiente:

* Python 2.7
* Beautiful Soup
* [Ghost](https://github.com/jeanphix/Ghost.py)

##Ejemplo de uso

Para correr el script:

`python inegi.py`

El programa permite moverse a través de los menús que tiene la página del INEGI. Después de listar los recursos disponibles, el programa pedirá al usuario seleccionar alguno, dependiendo del tipo de recurso seleccionado el programa tomará acciones diferentes:

* Menú: el programa desplegará las nuevas opciones
* Regresar: el programa regresará al folder anterior
* Archivo: la descarga comenzará automáticamente (el programa también puede obtener el link directo y enviarlo a un archivo de texto, ver la siguiente sección)
* Folder: descargará todos los archivos dentro del mismo
* Descargar todo: descargará todos los recursos disponibles en el listado actual

###Enviando links a un archivo de texto

Aunque es posible descargar archivos usando el programa directamente, no es recomendable hacerlo cuando se quieren descargar muchos archivos (ej. todos los archivos estatales del DENUE), para ello, es posible enviar a un archivo de texto las ligas directas a los recursos, para que puedan ser descargados con un programa especializado (ej. [jDownloader](http://jdownloader.org/))

Para indicar al programa que envíe los links a un archivo de texto:

`python inegi.py /path/al/archivo/urls.txt`

##Trabajo hecho

* Listar todos los documentos de la página de descarga masiva
* Poder desplazarse por los menús de la página
* Descargar folders con archivos para un estado completo
* Descargar archivos de manera individual
* Opción para enviar links a un archivo de texto en vez de descargarlos (en caso de querer usar algún gestor de descargas)
* Poder descargar estudios completos (ej. las 33 carpetas del DENUE)

##Trabajo pendiente

* Crear un binario para poder correr el script sin dependencias
* Mejorar la impresión del menú
* Imprimir el path en el que está el usuario

##Bugs

* Cuando se hace una descarga masiva, en algunas ocasiones el programa lanza un error de timeout