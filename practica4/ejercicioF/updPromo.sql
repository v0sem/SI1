ALTER TABLE customers
    ADD COLUMN promo integer NOT NULL default 0;


CREATE
OR REPLACE FUNCTION updPromo () RETURNS TRIGGER as $$ 
BEGIN
    UPDATE orderdetail 
        SET price = products.price*orderdetail.quantity*(1 - CAST(NEW.promo AS NUMERIC) / CAST(100 AS NUMERIC))
        FROM products, orders
        WHERE products.prod_id=orderdetail.prod_id
            AND orderdetail.orderid = orders.orderid
            AND orders.status IS NULL
            AND orders.customerid = NEW.customerid;

    PERFORM pg_sleep(1);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updPromoTrig 
AFTER
    UPDATE of promo ON customers FOR EACH ROW
    EXECUTE PROCEDURE updPromo();