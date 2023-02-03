-- Database: BBDD

-- Si ya existieran las tablas previamente, se eliminarán
DROP TABLE IF EXISTS revista CASCADE;
DROP TABLE IF EXISTS articulo CASCADE;
DROP TABLE IF EXISTS citas CASCADE;



CREATE TABLE revista (
    nombre CHAR(60) PRIMARY KEY,
    ISSN CHAR(9) UNIQUE NOT NULL,
    pais CHAR(30) NOT NULL,
    fecha INT NOT NULL
);
CREATE TABLE articulo ( 
	nombre CHAR(255) NOT NULL, 
	DOI CHAR(30) PRIMARY KEY,
	revista CHAR(60) REFERENCES revista(nombre), 
	fecha INT NOT NULL
); 
CREATE TABLE citas (
    doi_citante CHAR(30) REFERENCES articulo(DOI),
    doi_citado CHAR(30) REFERENCES articulo(DOI),
    PRIMARY KEY (doi_citante, doi_citado)
);

-- ÍNDICE:
CREATE INDEX nombre_index ON revista (nombre);
-- Ejemplo de uso: 
-- SELECT * FROM revista USE INDEX (nombre_index) WHERE nombre = 'Revista1';


-- OPTIMIZADOR
ANALYZE revista;
ANALYZE articulo;
ANALYZE citas;



-- EJEMPLO DE INSERT:
--INSERT INTO revista VALUES ('Revista1','ISSN1','España', 2020);
--INSERT INTO revista VALUES ('Revista2','ISSN2','España', 2020);
--INSERT INTO articulo VALUES ('Nombre1','10/r23','Revista1', 2020);
--INSERT INTO articulo VALUES ('Nombre2','10/r24','Revista1', 2021);
--INSERT INTO articulo VALUES ('Nombre3','10/r25','Revista2', 2022);
--INSERT INTO citas VALUES ('10/r25','10/r23');
-- Se cargan los datos del CSV generado tras hacer web scrapping
COPY revista FROM 'C:\Users\Public\revistas.csv' DELIMITER ',' CSV Header;

-- Visualizamos los datos
SELECT * FROM revista





