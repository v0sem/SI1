CREATE OR REPLACE FUNCTION trigUpdOrders() RETURNS TRIGGER AS $$

BEGIN

    IF(TG_OP = 'INSERT' OR TG_OP = 'DELETE' OR TG_OP = 'UPDATE') THEN
        UPDATE orders SET netamount = NULL;
        UPDATE orders SET totalamount = NULL;
    ELSE
        RETURN NULL;
    END IF;

    PERFORM setOrderAmount();
    RETURN NULL;

END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS updOrders ON orderdetail;
CREATE TRIGGER updOrders AFTER DELETE OR INSERT OR UPDATE ON orderdetail
FOR EACH ROW EXECUTE PROCEDURE trigUpdOrders();
