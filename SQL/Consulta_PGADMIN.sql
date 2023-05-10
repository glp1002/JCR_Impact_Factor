-- Database: BBDD

-- Si ya existieran las tablas previamente, se eliminarán
DROP TABLE IF EXISTS revista CASCADE;
DROP TABLE IF EXISTS articulo CASCADE;
DROP TABLE IF EXISTS citas CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS modelos CASCADE;


CREATE TABLE users (
    username VARCHAR(255),
    password VARCHAR(255),
    email VARCHAR(255),
    admin BOOLEAN
);
CREATE TABLE modelos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
	rmse FLOAT,
    modelo BYTEA
);
CREATE TABLE revista (
    nombre CHAR(60) PRIMARY KEY,
    ISSN CHAR(9) UNIQUE NOT NULL,
    categoria CHAR(255) NOT NULL,
    fecha INT NOT NULL
);
CREATE TABLE articulo ( 
	nombre CHAR(255) NOT NULL, 
	DOI CHAR(30) PRIMARY KEY,
	revista CHAR(60) REFERENCES revista(nombre), 
	ncitas INT NOT NULL,
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
ANALYZE users;


-- EJEMPLO DE INSERT:
INSERT INTO revista VALUES ('Revista1','ISSN1','IA', 2020);
INSERT INTO revista VALUES ('Revista2','ISSN2','DS', 2020);
INSERT INTO articulo VALUES ('Nombre1','10/r23','Revista1', 500, 2020);
INSERT INTO articulo VALUES ('Nombre2','10/r24','Revista1', 100, 2021);
INSERT INTO articulo VALUES ('Nombre3','10/r25','Revista2', 30, 2023);
INSERT INTO citas VALUES ('10/r25','10/r23');
INSERT INTO users VALUES ('Pepe', 'password123', 'pepe@example.com', false);
INSERT INTO users VALUES ('Peter', 'p@ssw0rd', 'peter@example.com', true);

-- Se cargan los datos del CSV generado tras hacer web scrapping
--COPY revista FROM 'C:\Users\Public\revistas.csv' DELIMITER ',' CSV Header;

-- Visualizamos los datos
-- SELECT * FROM revista
-- SELECT * FROM articulo
-- SELECT * FROM citas
-- SELECT * FROM users




