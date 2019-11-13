ALTER TABLE imdb_actormovies
ADD PRIMARY KEY (actorid, movieid);

/*Delete duplicate primary keys*/
WITH cte AS (
    SELECT 
        prod_id, 
        orderid, 
        ROW_NUMBER() OVER (
            PARTITION BY 
                prod_id,
                orderid
            ORDER BY
                prod_id,
                orderid
        ) row_num
     FROM 
        orderdetail
)

DELETE FROM orderdetail
WHERE (orderid, prod_id) IN (SELECT orderid, prod_id FROM cte WHERE row_num > 1);

ALTER TABLE orderdetail
ADD PRIMARY KEY (orderid, prod_id);

ALTER TABLE imdb_actormovies
ADD FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid);

ALTER TABLE imdb_actormovies
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

ALTER TABLE orderdetail
ADD FOREIGN KEY (orderid) REFERENCES orders(orderid);

ALTER TABLE orderdetail
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id);

ALTER TABLE orders
ADD FOREIGN KEY (customerid) REFERENCES customers(customerid);

ALTER TABLE inventory
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id);