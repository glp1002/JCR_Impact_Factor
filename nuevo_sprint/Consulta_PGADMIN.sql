-- Database: BBDD

-- Si ya existieran las tablas previemente, se eliminarán
DROP TABLE IF EXISTS articulo;

CREATE TABLE articulo ( 
	nombre CHAR(255), 
	DOI CHAR(30) PRIMARY KEY,
	revista CHAR(60), 
	ncitas INT, 
	fecha INT
); 

-- EJEMPLO DE INSERT:
-- INSERT INTO articulo VALUES (0,'Nombre1','Revista1',10, 2020);

-- Se cargan los datos del CSV generado tras hacer web scrapping
COPY articulo FROM '.\BBDD3.csv' DELIMITER ',' CSV Header;

-- Visualizamos los datos
SELECT * FROM articulo
