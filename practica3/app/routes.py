#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, flash
import json
import os
import sys
from hashlib import md5
import random
import datetime
from app import app
from app import database

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    top = database.topventas()
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    return render_template('index.html', title = "Home", movies=catalogue['peliculas'], top=top, user=session.get('usuario'))


@app.route('/search', methods=['POST'])
def search():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    # Get movies with search
    results = []
    for movie in catalogue['peliculas']:
        if request.form.get('search_content').lower() in movie['titulo'].lower():
            results.append(movie)
            
    return render_template('search.html', title = "Search results", movies=results, user=session.get('usuario'))

@app.route('/category', methods=['POST'])
def category():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    # Get movies with search
    results = []
    for movie in catalogue['peliculas']:
        if request.form.get('category') == movie['categoria']:
            results.append(movie)
            
    return render_template('category.html', category=request.form.get('category'), title = "Search results", movies=results, user=session.get('usuario'))
    

@app.route('/movie_det', methods=['POST'])
def details():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    title = request.form.get('title')

    movie = None
    for m in catalogue['peliculas']:
        if m['titulo'] == title:
            movie = m
            break

    return render_template('movie_det.html', movie=movie, user=session.get('usuario'))


@app.route('/login', methods=['POST'])
def login():
    user = database.authenticate(request.form.get('email'), request.form.get('password'))
    if user != 'Something is broken':
        session['usuario'] = user[0]
        session['custid'] = user[1]
        session.modified=True         

    return redirect(url_for('index'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        if database.register(request.form.get('email'), request.form.get('password'), username=request.form.get('username'),
                                creditcard=request.form.get('ccnumber')) == 'Something is broken':
            print (request.referrer, file=sys.stderr)
            flash('Email already in use')
            session.modified=True
            return redirect(url_for('register'))
    return render_template('register.html', title="Register")

@app.route('/add_cart', methods=['POST'])
def add_cart(): 
    pelicula = request.form.get('id')

    if 'cart' not in session:
        session['cart'] = database.newcarrito()
        return redirect(url_for('index'))

    database.orderdetail(pelicula, session['cart'])
    session.modified = True

    return redirect(url_for('index'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():

    if 'cart' not in session or session['cart'] == 'Something is broken':
        session['cart'] = database.newcarrito()

    comprado=False
    movies=[]
    money_total=0
    print(session.get('cart'))

    for t in database.getcarrito(session['cart']):
        movies.append(
            {
                'titulo': t[0],
                'precio': t[1],
                'cantidad': t[2],
                'prodid': t[3],
            }
        )
        money_total += t[1]

    if request.method == 'POST':
        if database.comprar(session['cart'], session['custid']) != 'Something is broken':
            session['cart'] = database.newcarrito()
            comprado=True
        flash('Algo ha ido mal, vuelve a intentar')

    return render_template('cart.html', compra=comprado, title="Checkout", total=money_total, movies=movies, user=session.get('usuario'))


@app.route('/historial', methods=['GET', 'POST'])
def historial():
    if request.method == 'GET':
        user = session.get('usuario')
        user_path = 'usuarios/' + str(user)

        if 'historial.json' in os.listdir(user_path):
            historial_data = open(user_path + '/historial.json', 'r').read()
            try:
                historial = json.loads(historial_data)
            except json.decoder.JSONDecodeError:
                historial = {}
                historial['compras'] = []

        else:
            historial_data = open(user_path + '/historial.json', 'w')
            historial = {}
            historial['compras'] = []

        f = open(user_path + '/datos.dat', 'r')
        for i in range(0,4):
            f.readline()
        money = f.readline()
        f.close()
        money.strip()
    
    else:
        prev_val = []
        f = open('usuarios/' + session.get('usuario') + '/datos.dat', "r")
        for i in range(0,4):
            prev_val.append(f.readline())
        money = f.readline()
        f.close()
        money.strip()

        f = open('usuarios/' + session.get('usuario') + '/datos.dat', "w")
        for i in range(0,4):
            f.write(prev_val[i])    
        f.write(str(float(money) + float(request.form.get('dinero'))))
        f.close()
        return redirect(url_for('historial'))

    return render_template('historial.html', historial=historial['compras'], money=money, title='Historial', user=session.get('usuario'))


@app.route('/increment', methods=['GET', 'POST'])
def increment():
    return str(random.randint(1, 100))

@app.route('/delete', methods=['POST',])
def delete():
    orderid = session.get('cart')
    prodid = request.form.get('prod_id')

    database.deleteorderdet(prodid, orderid)

    return redirect(url_for('cart'))