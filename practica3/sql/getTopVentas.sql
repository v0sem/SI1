CREATE OR REPLACE FUNCTION getTopVentas(INTEGER)
RETURNS TABLE(
    ANO TEXT,
    PELICULA VARCHAR,
    VENTAS INT
) AS $$
DECLARE
    counter record;
    anio ALIAS FOR $1;
BEGIN
    CREATE TABLE temporal (
        ANO TEXT,
        PELICULA VARCHAR,
        VENTAS INT
    );

    FOR counter IN anio..date_part('year', CURRENT_DATE)
    LOOP
        INSERT INTO temporal (
            SELECT DISTINCT imdb_movies.year, imdb_movies.movietitle, sales
            FROM inventory
            INNER JOIN products USING(prod_id)
            INNER JOIN imdb_movies USING(movieid)
            WHERE CAST(RIGHT(imdb_movies.year, 4) AS INTEGER) = counter
            ORDER BY sales DESC LIMIT 1
        );
    END LOOP;
    
    RETURN QUERY(
        SELECT * FROM temporal
    );
    DROP TABLE temporal;

END;

$$ LANGUAGE plpgsql;

SELECT getTopVentas(2003);