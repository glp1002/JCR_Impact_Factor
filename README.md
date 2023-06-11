# JCR_Impact_Factor

🔗 **Página web**: https://paperrank.herokuapp.com/

![Logo de Paperrank](./web_application/paperrank/static/images/logo_bl.png)

## Índice
1. [Descripción](#descripción) ✍ 
2. [Participantes](#participantes) 👨‍👩‍👧 
3. [Contenido](#contenido) 📦 
4. [Instrucciones para el lanzamiento en local](#instrucciones-para-el-lanzamiento-en-local) 👨‍💻
5. [Licencia](#licencia) ⚖ 

## Descripción 
_El presente proyecto se centra en la extracción de datos bibliográficos con el fin de calcular y predecir el Factor de Impacto. Esta métrica se utiliza para evaluar la importancia de una revista en un campo científico determinado. Se mide a través de la frecuencia con la que los artículos de la misma han sido citados en un año específico. Se trata de un criterio importante en la evaluación de la calidad del trabajo científico y puede ser de gran ayuda en la selección de la revista adecuada para publicar un nuevo trabajo._

_Se extraen los datos históricos disponibles en la web (tales como Google Scholar, Crossref, Web of Science, Scopus...) empleando técnicas de web scrapping sobre las distintas fuentes. Estos datos se utilizan como entradas para los algoritmos de aprendizaje automático, que serán supervisados y se utilizarán para estimar el valor del Índice de Impacto de las revistas indexadas en el JCR (Journal Citation Reports)._

_El producto final es una aplicación web accesible y de fácil uso para la comunidad científica, que permita predecir la importancia de las revistas científicas en tiempo real._

## Participantes 
* Virginia Ahedo García (tutora)
* Álvar Arnaiz González (co-tutor)
* Gadea Lucas Pérez (alumna: glp1002@alu.ubu.es)

## Contenido 
Carpetas:
* calculate_jcr: contiene los módulos necesarios para el cálculo del JCR
* data_extraction: contiene los modelos desarrollados para la fase de extracción de datos
* doc: contiene la documentación del proyecto (memoria y anexos) en formato LaTex y PDF
* prediction_models: contiene los modelos de aprendizaje automático de predicción del JCR
* web_application/paperrank: contiene el código y los recursos de la aplicación web

Ficheros:
* LICENSE: licencia _GNU General Public License_ en formato Markdown
* Procfile: fichero de configuración de Heroku. Contiene los comandos iniciales para la ejecución de la aplicación
* requirements.txt: fichero de requisitos (utilidades y librerías)
* runtime.txt: fichero para indicar a Heroku la versión de Python que se está usando.
* README.md: fichero actual

## Instrucciones para el lanzamiento en local 
Durante la etapa de desarrollo, se deberá lanzar la aplicación de forma local en el servidor de Flask. Los pasos a seguir son los siguientes:

### Instalación de Flask y dependencias
Una vez configurado el entorno virtual (si se ha decidido utilizar uno), el siguiente paso es instalar Flask y las dependencias necesarias para la ejecución de la aplicación. Será preciso navegar hasta la carpeta raíz del proyecto. Después, se deberá seguir los siguientes pasos:
* Ejecutar el siguiente comando para instalar las dependencias especificadas en el archivo requirements.txt (se recomienda usar la versión de Python 3.11 para asegurar la compatibilidad de veriones con los requerimentos):
```pip install -r requirements.txt```
* En la carpeta web_application/paperrank hay dos ficheros de procesamiento por lotes, uno para Windows y otro para Linux.
  - En Windows: ```win_start.cmd```
  - En Linux: ```./lin_start.sh```
* El servidor se abrirá en http://localhost:5000.

### Base de datos
Para poder ejecutar la aplicación en local, será necesario crear una base de datos PostgreSQL y conectarla al código de la aplicación.
* Descargar e instalar PostgreSQL desde el sitio web oficial: https://www.postgresql.org/download/.
* Seguir las instrucciones de instalación para su sistema operativo específico.
* Durante la instalación, será necesario asegurarse de recordar la contraseña del usuario «postgres», ya que será necesaria más adelante.
* Abrir un terminal y comprobar que el servidor PostgreSQL esté en funcionamiento.
* Ejecutar el siguiente comando para acceder a la interfaz de línea de comandos de PostgreSQL:
```psql -U postgres```
* Se solicitará la contraseña del usuario _postgres_.
* Una vez en la interfaz de PostgreSQL, ejecutar el siguiente comando para crear una nueva base de datos:
``` CREATE DATABASE nombre_basedatos; ```
* Se puede verificar que la base de datos se haya creado correctamente ejecutando el comando ```\l```, que mostrará una lista de todas las bases de datos disponibles.

Después, bastará con descomentar en el fichero de configuración de la aplicación (app.py) la opción para conectar con la base de datos local e incluir ahí las credenciales de la base de datos nueva.


## Licencia
⚖ [The GNU General Public License](https://www.gnu.org/licenses/)

</br>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-purple.svg)](https://www.gnu.org/licenses/gpl-3.0)

---

<div align="center">
  <p align="center" style="font-size:0.8em">Proyecto financiado con una Beca de Colaboración del Ministerio de Educación y Formación Profesional</p>
</div>
