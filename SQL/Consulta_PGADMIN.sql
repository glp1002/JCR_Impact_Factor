-- Database: BBDD

-- Si ya existieran las tablas previamente, se eliminarán
DROP TABLE IF EXISTS revista CASCADE;
DROP TABLE IF EXISTS revista_jcr CASCADE;
DROP TABLE IF EXISTS citas CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS modelos CASCADE;


CREATE TABLE users (
    username VARCHAR(255),
    password VARCHAR(255),
    email VARCHAR(255),
    admin BOOLEAN,
	image BYTEA
);
CREATE TABLE modelos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
	rmse FLOAT,
    modelo BYTEA
);
CREATE TABLE revista (
    nombre CHAR(255) PRIMARY KEY,
    ISSN CHAR(9) UNIQUE NOT NULL,
    categoria CHAR(255) NOT NULL
);
CREATE TABLE revista_jcr(
    nombre CHAR(255),
	fecha INT NOT NULL, 
	JCR FLOAT NOT NULL,
	citas NUMERIC NOT NULL,
	diff FLOAT NOT NULL
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
ANALYZE revista_jcr;

-- Se cargan los datos del CSV generado tras hacer web scrapping
COPY revista(nombre, ISSN, categoria)
FROM 'C:\Users\Public\lista_revistas.csv'
DELIMITER ',' CSV HEADER;

COPY revista_jcr (fecha, nombre, citas, JCR, diff)
FROM 'C:\Users\Public\datos_combinados.csv' DELIMITER ',' CSV HEADER;

INSERT INTO users VALUES ('Pepe', 'password123', 'pepe@example.com', false);
INSERT INTO users VALUES ('Admin', 'p@ssw0rd', 'admin@example.com', true);

SELECT * FROM users



