CREATE OR REPLACE FUNCTION getTopMonths(prod integer, imp integer)
RETURNS TABLE(ano INTEGER, mes INTEGER, importe NUMERIC, productos BIGINT) AS $$

DECLARE

BEGIN

    return query(
        SELECT 
            * 
        FROM
            (SELECT cast(date_part('year', orderdate) AS INTEGER), cast(date_part('month', orderdate) AS INTEGER), SUM(totalamount) AS tot, SUM(quantity) AS quan FROM 
                orders
            NATURAL JOIN
                orderdetail
            GROUP BY
                date_part('year', orderdate), date_part('month', orderdate)
            ORDER BY
                date_part('year', orderdate), date_part('month', orderdate)) AS mand
        WHERE
            tot >= prod OR quan >= imp
    );

END;

$$ LANGUAGE plpgsql;

SELECT * FROM getTopMonths(2500000, 1000000);