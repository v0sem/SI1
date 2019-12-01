import os
import sys
import datetime
import traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select, insert

# configurar el motor de sqlalchemy
db_engine = create_engine(
    "postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# cargar una tabla
db_table_movies = Table('imdb_movies', db_meta,
                        autoload=True, autoload_with=db_engine)
db_user = Table('customers', db_meta, autoload=True, autoload_with=db_engine)

def topventas():
    db_conn=db_engine.connect()
    res = db_conn.execute("SELECT pelicula FROM getTopVentas(%s)", str(datetime.datetime.now().year - 15)) 
    db_conn.close()
    return list(res) 



def register(email, password, firstname=None, lastname=None, address1=None, address2=None, city=None, 
             state=None, zip=None, country=None, region=None,
             phone=None, creditcardtype=None, creditcard=None, creditcardexpiration=None,
             username=None, age=None, income=None, gender=None):
    
    try:
        db_conn=None
        db_conn=db_engine.connect()

        ins = insert(db_user, values=[{
            'customerid':db_conn.execute("SELECT max(customerid) FROM customers").fetchone()[0] + 1,
            'firstname':firstname,
            'lastname':lastname,
            'address1':address1,
            'address2':address2,
            'city':city,
            'state':state,
            'zip':zip,
            'country':country,
            'region':region,
            'email':email,
            'phone':phone,
            'creditcardtype':creditcardtype,
            'creditcard':creditcard,
            'creditcardexpiration':creditcardexpiration,
            'username':username,
            'password':password,
            'age':age,
            'income':income,
            'gender':gender,
        }])
        db_conn.execute(ins)
        db_conn.close()
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    
    return

def authenticate(email, password):

    try:
        db_conn=None
        db_conn=db_engine.connect()
        user = db_conn.execute("SELECT username FROM customers WHERE email=%s AND password=%s", (email, password))
        name = list(user)[0][0]
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    return name

def newcarrito():
    try:
        db_conn=db_engine.connect()
        db_conn.execute("INSERT INTO orders (orderid, orderdate, netamount, tax, totalamount) values((SELECT max(orderid) FROM orders) + 1,CURRENT_DATE,0,0,0)")
        res = db_conn.execute("SELECT max(orderid) FROM orders")
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    return list(res)[0][0]

def getcarrito(orderid):
    try:
        db_conn=db_engine.connect()
        print("helloo", orderid)
        res = db_conn.execute("SELECT movietitle, orderdetail.price, quantity, orderdetail.prod_id FROM orderdetail INNER JOIN products ON orderdetail.prod_id=products.prod_id INNER JOIN imdb_movies ON products.movieid=imdb_movies.movieid WHERE orderid=%s", 
                                (str(orderid)))
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    return list(res)

def orderdetail(prodid, orderid):
    try:
        print("hello", orderid)
        db_conn=db_engine.connect()
        check = db_conn.execute("SELECT quantity FROm orderdetail WHERE orderid=%s AND prod_id=%s",
                                (str(orderid), str(prodid)))
        lista = list(check)
        quant = len(lista)
        print(quant)
        if quant == 0:
            db_conn.execute("INSERT INTO orderdetail (orderid, prod_id, price, quantity) values(%s,%s,(SELECT price FROM products WHERE prod_id=%s),1)", 
                        (str(orderid), str(prodid), str(prodid)))
        else:
            price = db_conn.execute("SELECT price FROM products WHERE prod_id=%s", (str(prodid)))
            db_conn.execute("UPDATE orderdetail SET quantity=%s, price=%s WHERE orderid=%s AND prod_id=%s",
                            (str(lista[0][0] + 1), str(list(price)[0][0] * (lista[0][0] + 1)), str(orderid), str(prodid)))
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    return

def comprar(orderid):
    try:
        db_conn=db_engine.connect()
        db_conn.execute("UPDATE orders SET status='Paid' WHERE orderid=%s", (str(orderid)))
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    return

def deleteorderdet(prodid, orderid):
    try:
        db_conn=db_engine.connect()
        db_conn.execute("DELETE FROM orderdetail WHERE orderid=%s AND prod_id=%s", (str(orderid), str(prodid)))
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    return