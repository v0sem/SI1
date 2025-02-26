# Práctica 4

Autores:
   
   * Pablo Sánchez Redondo
   * Antonio Solana Vera

## Ejercicio A

    a. Ver en ejercicioA/clientesDistintos.sql
    b. QUERY PLAN Sin index
---
```
 Aggregate  (cost=5636.23..5636.24 rows=2 width=118)
   ->  Sort  (cost=5636.23..5636.24 rows=2 width=118)
         Sort Key: customers.username
         ->  Gather  (cost=1000.28..5636.22 rows=2 width=118)
               Workers Planned: 1
               ->  Nested Loop  (cost=0.29..4636.02 rows=1 width=118)
                     ->  Parallel Seq Scan on orders  (cost=0.00..4627.72 rows=1 width=4)
                           Filter: ((totalamount > '100'::numeric) AND (date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))
                     ->  Index Scan using customers_pkey on customers  (cost=0.29..8.30 rows=1 width=122)
                           Index Cond: (customerid = orders.customerid)
```
    c. QUERY PLAN Index en orderdate
---
```
 Aggregate  (cost=5636.23..5636.24 rows=2 width=118)
   ->  Sort  (cost=5636.23..5636.24 rows=2 width=118)
         Sort Key: customers.username
         ->  Gather  (cost=1000.28..5636.22 rows=2 width=118)
               Workers Planned: 1
               ->  Nested Loop  (cost=0.29..4636.02 rows=1 width=118)
                     ->  Parallel Seq Scan on orders  (cost=0.00..4627.72 rows=1 width=4)
                           Filter: ((totalamount > '100'::numeric) AND (date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))
                     ->  Index Scan using customers_pkey on customers  (cost=0.29..8.30 rows=1 width=122)
                           Index Cond: (customerid = orders.customerid)

```
    QUERY PLAN Index en totalamount
---
```
 Aggregate  (cost=4496.93..4496.94 rows=2 width=118)
   ->  Sort  (cost=4496.93..4496.94 rows=2 width=118)
         Sort Key: customers.username
         ->  Nested Loop  (cost=1127.18..4496.92 rows=2 width=118)
               ->  Bitmap Heap Scan on orders  (cost=1126.90..4480.32 rows=2 width=4)
                     Recheck Cond: (totalamount > '100'::numeric)
                     Filter: ((date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))
                     ->  Bitmap Index Scan on i_total  (cost=0.00..1126.90 rows=60597 width=0)
                           Index Cond: (totalamount > '100'::numeric)
               ->  Index Scan using customers_pkey on customers  (cost=0.29..8.30 rows=1 width=122)
                     Index Cond: (customerid = orders.customerid)
```
    QUERY PLAN index en ambas columnas
---

```
 Aggregate  (cost=5636.23..5636.24 rows=2 width=118)
   ->  Sort  (cost=5636.23..5636.24 rows=2 width=118)
         Sort Key: customers.username
         ->  Gather  (cost=1000.28..5636.22 rows=2 width=118)
               Workers Planned: 1
               ->  Nested Loop  (cost=0.29..4636.02 rows=1 width=118)
                     ->  Parallel Seq Scan on orders  (cost=0.00..4627.72 rows=1 width=4)
                           Filter: ((totalamount > '100'::numeric) AND (date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))
                     ->  Index Scan using customers_pkey on customers  (cost=0.29..8.30 rows=1 width=122)
                           Index Cond: (customerid = orders.customerid)


```

    e. De todos los índices creados se puede ver que el índice en totalamount es el más óptimo. Lo que significa que el índice en orderdate no ayuda en la optimización de la consulta. El necesario es el índice en totalamount.



