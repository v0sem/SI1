CREATE OR REPLACE FUNCTION
setOrderAmount()
RETURNS void AS $$
DECLARE
    det record;
BEGIN
    FOR det IN (SELECT orderid, SUM(price * quantity) as net 
                    FROM orderdetail GROUP BY orderid)
    LOOP
        UPDATE 
            orders 
        SET
            netamount = det.net,
            totalamount = det.net + det.net * (orders.tax*0.01)
        WHERE det.orderid = orders.orderid AND 
            (orders.netamount IS NULL OR orders.totalamount IS NULL);
    END LOOP;
END;

$$ LANGUAGE plpgsql;

SELECT setOrderAmount();