# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare, break0, niter):

    # TODO: implementar la consulta; asignar nombre 'cc' al contador resultante
    consulta = "SELECT COUNT(DISTINCT username) AS cc\
        FROM customers NATURAL JOIN orders WHERE date_part('year', orderdate)=" + anio + " AND \
        date_part('month', orderdate)=" + mes + " AND totalamount> {};"
    
    consulta_p = "PREPARE getListaCliMes(int) AS\
        SELECT COUNT(DISTINCT username) AS cc FROM customers NATURAL JOIN orders WHERE date_part\
        ('year', orderdate)=" + anio + " AND date_part('month', orderdate)=" + mes + " AND\
        totalamount> $1;"
    
    # TODO: ejecutar la consulta 
    # - mediante PREPARE, EXECUTE, DEALLOCATE si use_prepare es True
    # - mediante db_conn.execute() si es False
    if use_prepare:
        db_conn.execute(consulta_p)

    # Array con resultados de la consulta para cada umbral
    dbr=[]


    for ii in range(niter):

        # TODO: ...
        if use_prepare:
            res = list(db_conn.execute("EXECUTE getListaCliMes("+ str(iumbral) +");"))[0]
        else:
            res = list(db_conn.execute(consulta.format(str(iumbral))))[0]

        # Guardar resultado de la query
        dbr.append({"umbral":iumbral,"contador":res['cc']})

        # TODO: si break0 es True, salir si contador resultante es cero
        if break0 and res['cc'] == 0:
            break

        # Actualizacion de umbral
        iumbral = iumbral + iintervalo

    if use_prepare:
        db_conn.execute("DEALLOCATE getListaCliMes;")            
    
    return dbr

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)
        
    resultproxy.close()  
    
    db_conn.close()  
    
    return a
    
def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()
    
    db_conn.close()  

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}
    
def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):

    db_conn = db_engine.connect()
    # Array de trazas a mostrar en la página
    dbr=[]

    # TODO: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()
    if bFallo:
        append1 = 'Borrando de orderdetail'
        consulta1 = "DELETE FROM orderdetail WHERE orderid IN( SELECT orderid FROM orders WHERE \
            customerid = {})".format(customerid)
        append3 = 'Borrando de orders'
        consulta3 = "DELETE FROM orders WHERE customerid = {}".format(customerid)
        append2 = 'Borrando de customers'
        consulta2 = "DELETE FROM customers WHERE customerid = {}".format(customerid)
    else:
        append1 = 'Borrando de orderdetail'
        consulta1 = "DELETE FROM orderdetail WHERE orderid IN( SELECT orderid FROM orders WHERE \
            customerid = {})".format(customerid)
        append2 = 'Borrando de orders'
        consulta2 = "DELETE FROM orders WHERE customerid = {}".format(customerid)
        append3 = 'Borrando de customers'
        consulta3 = "DELETE FROM customers WHERE customerid = {}".format(customerid)
    
    time.sleep(duerme)


    try:
        # TODO: ejecutar consultas
        if bSQL:
            db_conn.execute('BEGIN;')
            dbr.append(append1)
            db_conn.execute(consulta1)
            if bCommit:
                dbr.append('Commit intermedio')
                db_conn.execute('COMMIT;')
                db_conn.execute('BEGIN;')
            dbr.append(append2)
            db_conn.execute(consulta2)
            dbr.append(append3)
            db_conn.execute(consulta3)
        else:
            ts = db_conn.begin()
            dbr.append(append1)
            db_conn.execute(consulta1)
            if bCommit:
                dbr.append('Commit intermedio')
                ts.commit()
                ts = db_conn.begin()
            dbr.append(append2)
            db_conn.execute(consulta2)
            dbr.append(append3)
            db_conn.execute(consulta3)


    except Exception as e:
        # TODO: deshacer en caso de error
        dbr.append(str(e))
        dbr.append('Haciendo rollback')

        if bSQL:
            db_conn.execute('ROLLBACK;')
        else:
            ts.rollback()
        
        dbr.append('Operación cancelada, usuario se mantiene')

        orders = list(db_conn.execute('SELECT * FROM orderdetail WHERE orderid IN( SELECT orderid FROM orders WHERE customerid = ' + str(customerid) + ') LIMIT 5;'))
        dbr.append('Algunos orderdetails:')
        if len(orders) == 0:
            dbr.append('No hay detalles')
        else:
            for o in orders:
                dbr.append(o)

    else:
        # TODO: confirmar cambios si todo va bien
        dbr.append('Todo bien, commit')
        if bSQL:
            db_conn.execute('COMMIT;')
        else:
            ts.commit()
    
    db_conn.close()
    return dbr

