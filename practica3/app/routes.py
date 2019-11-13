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

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    return render_template('index.html', title = "Home", movies=catalogue['peliculas'], user=session.get('usuario'))


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
    for dirs in os.listdir('usuarios/'):
        if str(request.form.get('username')) == dirs:
            f = open('usuarios/' + dirs + '/datos.dat')
            valuser = f.readline()
            valpass = f.readline()
            f.close()
            valpass = valpass.strip()
            if md5(str(request.form.get('password')).encode()).hexdigest() == valpass:
                session['usuario'] = valuser.strip()
                session.modified=True
            break

    return redirect(url_for('index'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_path = 'usuarios/' + str(request.form.get('username'))

        # Create folder for users
        try:
            os.mkdir('usuarios/')
        except:
            pass
        
        try:
            os.mkdir(user_path)
            f = open(user_path + '/datos.dat', "w")
            f.write(str(request.form.get('username')) + '\n')
            f.write(md5(str(request.form.get('password')).encode()).hexdigest() + '\n')
            f.write(str(request.form.get('email')) + '\n')
            f.write(str(request.form.get('ccnumber')) + '\n')
            f.write(str(random.randint(0,100)))
            f.close()
            return redirect(url_for('index'))
        except FileExistsError:
            print (request.referrer, file=sys.stderr)
            flash('Name is already taken')
            session.modified=True
            return redirect(url_for('register'))
    return render_template('register.html', title="Register")

@app.route('/add_cart', methods=['POST'])
def add_cart():
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
                
    pelicula = request.form.get('id')

    result = None
    for movie in catalogue['peliculas']:
        print(str(movie['id']) + ' > ' + str(pelicula))
        if int(movie['id']) == int(pelicula):
            result = movie
            break

    try:
        session['cart'].append(result)
    except:
        session['cart'] = []
        session['cart'].append(result)
    
    session.modified = True

    return redirect(url_for('index'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    money_total = 0

    if 'cart' in session:
        for movie in session.get('cart'):
            money_total += movie['precio'] 

    prev_val = []

    if request.method == 'POST':
        valuser = session['usuario']
        for dirs in os.listdir('usuarios/'):
            if valuser == dirs:
                f = open('usuarios/' + valuser + '/datos.dat', "r")
                for i in range(0,4):
                    prev_val.append(f.readline())
                money = f.readline()
                f.close()
                money.strip()
                if float(money) < money_total:
                    flash('Not enough money')
                    session['cart'] = []
                    return render_template('cart.html', title="Checkout", total=money_total, movies=session.get('cart'), user=session.get('usuario'))
                else:
                    f = open('usuarios/' + valuser + '/datos.dat', "w")
                    try:
                        h_data = open('usuarios/' + valuser + '/historial.json', 'r').read()
                        data = json.loads(h_data)
                    except (FileNotFoundError, json.decoder.JSONDecodeError):
                        open('usuarios/' + valuser + '/historial.json', 'w')
                        data = {}
                        data['compras'] = []

                    cart = session.get('cart')
                    
                    peliculas = []
                    for movie in cart:
                        peliculas.append({
                            'title': movie['titulo'],
                            'valor': movie['precio']
                        })
                    
                    data['compras'].append({
                        'peliculas': peliculas,
                        'fecha': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
                    with open('usuarios/' + valuser + '/historial.json', 'w') as outfile:
                        json.dump(data, outfile)
                    for i in range(0,4):
                        f.write(prev_val[i])
                    f.write(str(float(money) - money_total))
                    session['cart'] = []
                    f.close()
                    return redirect(url_for('index'))

    return render_template('cart.html', title="Checkout", total=money_total, movies=session.get('cart'), user=session.get('usuario'))


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
