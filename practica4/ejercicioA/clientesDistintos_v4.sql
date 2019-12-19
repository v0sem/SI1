CREATE INDEX i_total ON orders (orderdate, totalamount);

EXPLAIN SELECT COUNT(DISTINCT username) FROM customers NATURAL JOIN orders WHERE 
    date_part('year', orderdate)=2015 AND date_part('month', orderdate)=04 AND totalamount>100;

DROP INDEX i_total;