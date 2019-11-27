CREATE OR REPLACE FUNCTION trigUpdInventory() RETURNS TRIGGER AS $$

DECLARE
    product record;
BEGIN
 
CREATE TABLE tempo(
    prod_id INTEGER
);

INSERT INTO tempo
    SELECT prod_id AS product FROM orderdetail WHERE orderdetail.orderid = new.orderid;

IF (new.status = 'Paid') THEN
    UPDATE
        inventory
    SET
        sales = sales + orderdetail.quantity,
        stock = stock - orderdetail.quantity
    FROM
        orderdetail, tempo
    WHERE
        orderdetail.prod_id = tempo.prod_id;

    INSERT INTO alertas (orderid) 
        SELECT orderid FROM inventory NATURAL JOIN orderdetail, tempo WHERE (inventory.stock = 0 AND inventory.prod_id=tempo.prod_id AND orderid=new.orderid);

END IF;

DROP TABLE tempo;

RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS updInventory ON orders;
CREATE TRIGGER updInventory AFTER UPDATE ON orders
FOR EACH ROW EXECUTE PROCEDURE trigUpdInventory();