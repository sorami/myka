import os
from random import choice

import sqlite3
from flask import Flask, request, g, url_for, abort, render_template, flash


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'myka.db'),
    SECRET_KEY='development key',
))
app.config.from_envvar('MYKA_SETTINGS', silent=True)


@app.route('/')
def show_title():
    db = get_db()
    lang = choice(["my", "ka"])
    cur = db.execute("select * from titles where lang = '{}' order by random()".format(lang));
    title = cur.fetchone()
    return render_template('show_question.html', title=title)

@app.route('/answer', methods=['POST'])
def show_answer():
    title_id = request.form["id"]
    answer = request.form["action"]

    db = get_db()
    cur = db.execute("select lang, text from titles where id = {}".format(title_id));
    lang, text = cur.fetchone()[0:2];
    correct = (lang == answer)

    if lang == "my":
        lang_msg = "Burmese (my)"
    else:
        lang_msg = "Georgian (ka)"

    return render_template('show_answer.html',
                            text=text, lang=lang, correct=correct, lang_msg=lang_msg)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')
