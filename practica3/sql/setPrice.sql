UPDATE orderdetail
SET
    price = products.price * pow(1.02, (date_part('year', CURRENT_DATE) - date_part('year', orders.orderdate)))
FROM 
    products, orders
WHERE
    orderdetail.prod_id = products.prod_id and orderdetail.orderid = orders.orderid;