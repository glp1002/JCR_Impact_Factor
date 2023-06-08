# JCR_Impact_Factor


## Descripción:
_Repositorio para el TFG sobre la estimación del factor de impacto de las publicaciones científicas._

## Participantes:
* Virginia Ahedo García
* Álvar Arnaiz González
* Gadea Lucas Pérez

## Contenido:
En esta carpeta se almacena el código necesario para el cálculo del JCR.
El contenido de esta sección es el siguiente:
* __listas_jcr__: Contiene los listados normalizados de JCR extraidos de Clarivate.
* __datos_extraidos__: Se trata de los resultados extraídos a través de Crossref.
* __calcJCR.py__: En este programa de Python se calcula el JCR y los ficheros resultantes (que se almacenarán en el mismo directorio). A saber:
    * __diagrama_cajas.py__
    * __jcr_esperado.csv__: JCR de Clarivate
    * __jcr_obtenido.csv__: JCR de Crossref
    * __diferencias.csv__: Diferencias entre los dos anteriores
    * __ranking.csv__: Ranking de revistas en función del JCR de Crossref 
