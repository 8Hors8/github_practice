

CREATE TABLE IF NOT EXISTS genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Создание таблицы performers
CREATE TABLE IF NOT EXISTS performers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(45) NOT NULL
);

-- Создание таблицы albums
CREATE TABLE IF NOT EXISTS albums (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    year DATE NOT NULL,
    CONSTRAINT chk_year CHECK (year >= '1990-01-01')
);

-- Создание таблицы tracks
CREATE TABLE IF NOT EXISTS tracks (
    id SERIAL PRIMARY KEY,
    id_albums INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    duration INT NOT NULL CHECK (duration > 100),
    CONSTRAINT fk_albums
        FOREIGN KEY (id_albums)
        REFERENCES albums (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Создание таблицы collection
CREATE TABLE IF NOT EXISTS collection (
    id SERIAL PRIMARY KEY,
    name VARCHAR(45) NOT NULL,
    year DATE NOT NULL,
	CONSTRAINT chk_year CHECK (year >= '1990-01-01')
);

-- Создание таблицы performers_genres
CREATE TABLE IF NOT EXISTS performers_genres (
    id SERIAL PRIMARY KEY,
    id_performers INT NOT NULL,
    id_genres INT NOT NULL,
    CONSTRAINT fk_performers
        FOREIGN KEY (id_performers)
        REFERENCES performers (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_genres
        FOREIGN KEY (id_genres)
        REFERENCES genres (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Создание таблицы performers_albums
CREATE TABLE IF NOT EXISTS performers_albums (
    id SERIAL PRIMARY KEY,
    id_performers INT NOT NULL,
    id_albums INT NOT NULL,
    CONSTRAINT fk_performers_pa
        FOREIGN KEY (id_performers)
        REFERENCES performers (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_albums_pa
        FOREIGN KEY (id_albums)
        REFERENCES albums (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Создание таблицы tracks_collection
CREATE TABLE IF NOT EXISTS tracks_collection (
    id SERIAL PRIMARY KEY,
    id_collection INT NOT NULL,
    id_tracks INT NOT NULL,
    CONSTRAINT fk_collection_tc
        FOREIGN KEY (id_collection)
        REFERENCES collection (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_tracks_tc
        FOREIGN KEY (id_tracks)
        REFERENCES tracks (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

