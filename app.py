from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import string
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Shorts_URL.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

@app.before_first_request
def create_tables():
    db.create_all()

class Urls(db.Model):
    __tablename__ = 'DATAS'
    id_ = db.Column("id_", db.Integer, primary_key=True)
    ORIGINAL_URL = db.Column("long", db.String(),unique=True)
    SHORT_URL = db.Column("short", db.String(10),unique=True)

    def __init__(self, ORIGINAL_URL, short):
        self.ORIGINAL_URL = ORIGINAL_URL
        self.short = short
    def __repr__(self):
        return "original_urls - {} shorten_urls - {} ".format(self.ORIGINAL_URL, self.SHORT_URL)       

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.ascii_letters + string.digits + string.punctuation
    while True:
        rand_letters = (''.join(random.choice(letters) for i in range(6)))
        short_url = Urls.query.filter_by(SHORT_URL=rand_letters).first()
        if not short_url:
            return rand_letters


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]
        found_url = Urls.query.filter_by(ORIGINAL_URL=url_received).first()

        if found_url:
            return redirect(url_for("display_short_url", url=found_url.SHORT_URL))
        else:
            short_url = shorten_url()
            print(short_url)
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template('url_page.html')

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(SHORT_URL=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url doesnt exist</h1>'

@app.route('/display/<url>')
def display_short_url(url):
    return render_template('url_page.html', short_url_display=url)

@app.route('/all_urls')
def display_all():
    return render_template('all_urls.html', vals=Urls.query.all())

@app.route('/history')
def history_get():
    DATAS = Urls.query.all()
    return render_template('history.html', DATAS=DATAS)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
