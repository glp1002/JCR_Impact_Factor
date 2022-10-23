-- Nos aseguramos de crear la tabla de cero
DROP TABLE IF EXISTS articulo;
CREATE TABLE articulo ( nombre CHAR(255), revista CHAR(60), ncitas INT, fecha DATE, id INTEGER PRIMARY KEY); 

-- EJEMPLO DE INSERT:
-- INSERT INTO articulo VALUES ('Nombre1','Revista1',10, '22-10-10',0);

-- Se cargan los datos del CSV generado tras hacer web scrapping
LOAD DATA LOCAL INFILE 'scrapping.csv' INTO TABLE articulo fields terminated BY ',';

-- Visualizamos los datos
SELECT * FROM articulo
