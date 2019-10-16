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