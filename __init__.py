import os
import time

import requests
from flask import Flask, render_template, session, url_for
from PIL import Image

from unsplash_creds import get_creds

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

hexbot_base = "https://api.noopschallenge.com/hexbot"


def style(path):
    img = Image.open(path)
    pixels = list(img.convert('RGBA').getdata())


@app.route('/')
def homepage():
    # image = requests.get(url, params={'client_id': client_id}).json()[
    #     'urls']['small']
    path = url_for('static', filename='image/img.jpg')
    session['path'] = path
    return(render_template('index.html', path=path))


@app.route('/pointillize/')
def pointillize():
    stylized_image = style(session['path'])
    stylized_path = 'stylized/' + time.ctime().replace(' ', '_') + '.jpg'
    stylized_image.save(stylized_path)
    return(render_template('index.html', path=stylized_path))


if __name__ == "__main__":
    url, client_id = get_creds()
    app.run(debug=True)
