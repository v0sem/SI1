SELECT DISTINCT email, orderid FROM customers NATURAL JOIN orders WHERE 
    date_part('year', orderdate)=2016 AND date_part('month', orderdate)=05 AND totalamount>250;