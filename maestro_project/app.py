import sqlite3
import pandas as pd
import numpy as np
import ast
from web_search import *
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

meta = pd.read_csv("sents_meta.csv")
sents = pd.read_csv("parsed_sents.csv")
sents = sents.applymap(lambda x: ast.literal_eval(x))
words = pd.read_csv("morph_info.csv")

def get_users(res, offset=0, per_page=10):
    return res[offset: offset + per_page]


@app.route('/', methods=('GET','POST'))
def index():

    if request.method == 'POST':
        data = request.form['query']
        return redirect(url_for('search2', query=data))

    else:
        html = render_template('create.html', pagination=None)
        return html

@app.route('/search2/<query>', methods=['GET', 'POST'])
def search2(query):

    if request.method == 'POST':
        data = request.form['query']
        return redirect(url_for('search2', query=data))

    results = search(query, sents, words, meta)
    page, per_page, offset = get_page_args(page_parameter='page',
                                    per_page_parameter='per_page')
    total = len(results)
    pagination_users = get_users(results, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    html = render_template('create.html',
                            page=page,
                            query=query,
                            items=pagination_users,
                            per_page=10,
                            pagination=pagination)
    return html


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)



app.run()
