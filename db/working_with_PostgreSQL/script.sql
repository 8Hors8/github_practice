-- Создание базы
--CREATE DATABASE db_homework ;

CREATE TABLE IF NOT EXISTS genres (
  id SERIAL NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (id))

