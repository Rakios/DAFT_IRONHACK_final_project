<img src="https://bit.ly/2VnXWr2" alt="Ironhack Logo" width="100"/>

# P2P Stastic
*Alberto Suarez*

*DAFT México Enero 2021*

## Content
- [Project Description](#project-description)
- [Alcance](#alcance)
- [Pasos del Proyectos ](#pasos-del-proyecto)

## Project Description
Proyecto final del  Data analytics Bootcamp, Full time (enero 2021)  de Ironhack Mexico.

El objetivo de este proyecto es la consolidación de todas las técnicas de web scraping para obtener información de Apis o páginas web de mercados P2P de criptomonedas, después de la extracción se aplicó un proceso de limpieza de datos y finalmente mostraremos la información de interés en un dashboard creado con el micro-framework Flask

## Alcance
Para la temática de este proyecto escogí páginas de venta y compra P2P de criptomonedas: 
- Limite mi búsqueda a solo páginas de criptomonedas con mercado P2P en Venezuela y solo tome las ventas y compras de Bitcoin

<img src="https://upload.wikimedia.org/wikipedia/commons/c/c5/Bitcoin_logo.svg" alt="bitcoin Logo" width="100"/>


## Pasos del Proyecto

###  Extracción

- Se obtuvieron 3 paginas para el análisis: Localbitcoin, Localcryptos y Binance
- En cada página se realizó un scraping a su sección de ofertas de ventas y compras,  utilizando técnicas de web scraping distintas: 
    - Localbitcoin, se extrajo la información utilizando su API.
    - Localcrytos, se extrajo la información con http request y luego se filtró con beautifulsoup
    - Binance, se definió una serie de funciones con Selenium para la extracción de los datos en sus distintas secciones
- La extracción de datos se automatizo para que se ejecutara cada 5 min, y se extrajo información durante una semana para generar un dataset inicial con el cual trabajar.


###  Limpieza
- Se aplicaron procedimientos básicos de limpieza de datos para obtener solo la información útil.
- Se generó un dataframe con la lista de string limpios, y se agregaron algunas columnas adicionales para identificar el origen de los datos, el tipo de oferta y la moneda ofertada.
- Se unifico la información de las 3 páginas en un solo dataset estandarizando la información.

###  Dashboard
- Con la información obtenida, se decidió mostrarla en un dashboard creado desde 0 usando el micro-framework Flask
- La página se llamó P2P Stastic y se generaron visualizaciones para enfatizar algunas métricas de interés sobre los datos

    <img src="https://github.com/Rakios/DAFT_IRONHACK_final_project/blob/main/img/1.PNG" alt="" width="600"/>

- Se filtró la data por página y se generó una sección especializada para cada página, donde se muestran:
    - Graficas de interés 

        <img src="https://github.com/Rakios/DAFT_IRONHACK_final_project/blob/main/img/2.PNG" alt="" width="600"/>

    - Los registros en forma de tabla paginados y correspondientes a esas páginas, con posibilidad de descargarlo.

        <img src="https://github.com/Rakios/DAFT_IRONHACK_final_project/blob/main/img/3.PNG" alt="" width="600"/>

- Por último, se implementó un API básico, para la extracción de los datos en formato JSON por parte de terceros.

    <img src="https://github.com/Rakios/DAFT_IRONHACK_final_project/blob/main/img/4.PNG"  alt=""  width="600"/>
<img src="https://github.com/Rakios/DAFT_IRONHACK_final_project/blob/main/img/5.PNG" alt="" width="600"/>

