DROP INDEX idx;

EXPLAIN select count(*) from orders where status is null;

EXPLAIN select count(*) from orders where status ='Shipped';

CREATE INDEX idx ON orders (status);

EXPLAIN select count(*) from orders where status is null;

EXPLAIN select count(*) from orders where status ='Shipped';

ANALYZE orders (status);

EXPLAIN select count(*) from orders where status ='Paid';

EXPLAIN select count(*) from orders where status ='Processed';