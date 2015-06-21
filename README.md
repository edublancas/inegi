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


##Dependencias

Para poder correr el script es necesario tener instalado lo siguiente:

* Python 2.7
* Beautiful Soup
* Ghost

##Trabajo hecho

* Listar todos los documentos de la página de descarga masiva
* Poder desplazarse por los menús de la página
* Descargar folders con archivos para un estado completo
* Descargar archivos de manera individual
* Opción para enviar links a un archivo de texto en vez de descargarlos (en caso de querer usar algún gestor de descargas)

##Trabajo pendiente

* Poder descargar estudios completos (ej. las 33 carpetas del DENUE)
* Crear un binario para poder correr el script sin dependencias
* Mejorar la impresión del menú
* Imprimir el path en el que está el usuario