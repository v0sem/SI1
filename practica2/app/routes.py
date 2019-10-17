#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, flash
import json
import os
import sys
from hashlib import md5
import random

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

    id = request.form.get('id')

    movie = None
    for m in catalogue['peliculas']:
        if m['id'] == id:
            movie = m
            break

    return render_template('movie_det.html', title=m.get('titulo'), movie=movie, user=session.get('usuario'))


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
        try:
            os.mkdir("NEPE")
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

@app.route('/get_cart', methods=['GET'])
def get_cart():
    return str(session['cart'])