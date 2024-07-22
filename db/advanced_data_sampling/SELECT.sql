--Задание №2
--1)
SELECT "name"
 FROM tracks
WHERE duration = (
	SELECT MAX(duration) 
	 FROM tracks);

SELECT "name"
 FROM tracks
ORDER BY duration DESC 
LIMIT 1;

--2)
SELECT "name"
 FROM tracks 
WHERE duration > 3.5 * 60;

--3)
SELECT "name"
 FROM collection
WHERE EXTRACT(YEAR FROM "year") BETWEEN '2019' AND '2020';

--4)
SELECT "name"
 FROM performers
WHERE "name" ~ '^[[:alpha:]]+$';

--5)
SELECT "name"
 FROM tracks
WHERE "name" ILIKE '%мой%'
 
--Задание №3
 
 --1)
SELECT g.name AS genre_name, COUNT(p.id) AS performer_count
 FROM genres AS g
INNER JOIN performers_genres AS pg ON g.id = pg.id_genres
INNER JOIN performers AS p ON pg.id_performers = p.id
GROUP BY g.name
ORDER BY performer_count DESC;

--2)
SELECT COUNT(*) AS track_count
FROM tracks AS t
INNER JOIN albums AS a ON t.id_albums = a.id
WHERE EXTRACT(YEAR FROM a."year") BETWEEN 2019 AND 2020;

--3)
SELECT a.name AS album_name,
       AVG(t.duration) AS average_track_duration
FROM albums AS a
INNER JOIN tracks AS t ON a.id = t.id_albums
GROUP BY a.name
ORDER BY album_name;

--4)
SELECT DISTINCT p.name AS performer_name
FROM performers AS p
LEFT JOIN performers_albums AS pa ON p.id = pa.id_performers
LEFT JOIN albums a ON pa.id_albums = a.id AND EXTRACT(YEAR FROM a."year") = 2020
WHERE a.id IS NULL;

--5)
SELECT DISTINCT c.name AS collection_name
FROM collection AS c
JOIN tracks_collection AS tc ON c.id = tc.id_collection
JOIN tracks AS t ON tc.id_tracks = t.id
JOIN albums AS a ON t.id_albums = a.id
JOIN performers_albums AS pa ON a.id = pa.id_albums
JOIN performers AS p ON pa.id_performers = p.id
WHERE p.name = 'Король и шут';

--Задание №4

--1)
SELECT DISTINCT a.name AS album_name
FROM albums AS a
JOIN performers_albums AS pa ON a.id = pa.id_albums
JOIN performers AS p ON pa.id_performers = p.id
JOIN performers_genres AS pg ON p.id = pg.id_performers
JOIN genres AS g ON pg.id_genres = g.id
GROUP BY a.id, a.name
HAVING COUNT(DISTINCT g.id) > 1;

--2)
SELECT name
FROM tracks
WHERE id NOT IN (
    SELECT DISTINCT id_tracks
    FROM tracks_collection
);

--3)
SELECT DISTINCT p.name AS performer_name
FROM performers AS p
JOIN performers_albums AS pa ON p.id = pa.id_performers
JOIN albums AS a ON pa.id_albums = a.id
JOIN tracks AS t ON a.id = t.id_albums
WHERE t.duration = (
    SELECT MIN(duration)
    FROM tracks
);

--4)
SELECT a.name AS album_name
FROM albums AS a
WHERE (
    SELECT COUNT(*)
    FROM tracks AS t
    WHERE t.id_albums = a.id
) = (
    SELECT MIN(track_count)
    FROM (
        SELECT COUNT(*) AS track_count
        FROM tracks
        GROUP BY id_albums
    ) AS album_tracks_count
);

