import os
import sys
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


def register(email, password, firstname=None, lastname=None, address1=None, address2=None, city=None, 
             state=None, zip=None, country=None, region=None,
             phone=None, creditcardtype=None, creditcard=None, creditcardexpiration=None,
             username=None, age=None, income=None, gender=None):
    
    try:
        db_conn=None
        db_conn=db_engine.connect()

        ins = insert(db_user, values=[{
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
