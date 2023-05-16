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

-- Se cargan los datos del CSV generado tras hacer web scrapping
--COPY revista FROM 'C:\Users\Public\revistas.csv' DELIMITER ',' CSV Header;


-- EJEMPLO DE INSERT:
-- INSERT para la tabla "revista"
INSERT INTO revista (nombre, ISSN, categoria, fecha) VALUES
    ('Revista A', 'ISSN111', 'Categoria A', 2020),
    ('Revista B', 'ISSN222', 'Categoria B', 2019),
    ('Revista C', 'ISSN333', 'Categoria C', 2021),
    ('Revista D', 'ISSN444', 'Categoria A', 2022);

-- INSERT para la tabla "articulo"
INSERT INTO articulo (nombre, DOI, revista, ncitas, fecha) VALUES
    ('Articulo 1', 'DOI111', 'Revista A', 10, 2020),
    ('Articulo 2', 'DOI222', 'Revista A', 5, 2021),
    ('Articulo 3', 'DOI333', 'Revista B', 8, 2022),
    ('Articulo 4', 'DOI444', 'Revista C', 12, 2022),
    ('Articulo 5', 'DOI555', 'Revista C', 3, 2023),
    ('Articulo 6', 'DOI666', 'Revista D', 15, 2023);

-- INSERT para la tabla "citas"
INSERT INTO citas (doi_citante, doi_citado) VALUES
    ('DOI222', 'DOI111'),
    ('DOI222', 'DOI333'),
    ('DOI333', 'DOI111'),
    ('DOI666', 'DOI444');

-- INSERT para la tabla "users"
INSERT INTO users VALUES ('Pepe', 'password123', 'pepe@example.com', false);
INSERT INTO users VALUES ('Peter', 'p@ssw0rd', 'peter@example.com', true);

-- Visualizamos los datos
-- SELECT * FROM revista
-- SELECT * FROM articulo
-- SELECT * FROM citas
-- SELECT * FROM users




