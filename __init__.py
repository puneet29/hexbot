import math
import os
import random
import sys
import time
import urllib

import cv2
import numpy as np
import requests
from flask import Flask, redirect, render_template, session, url_for

from unsplash_creds import get_creds

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

hexbot_base = "https://api.noopschallenge.com/hexbot"
COUNT = 25
url, client_id = get_creds()


# def colorDistance(c1, c2):
# This function slows down the process
# r_mean = (c1[0] + c2[0]) // 2
# r = c1[0] - c2[0]
# g = c1[1] - c2[1]
# b = c1[2] - c2[2]
# distance = math.sqrt((((512+r_mean)*r*r) >> 8) + 4 *
#                      g*g + (((767-r_mean)*b*b) >> 8))
# return(distance)

# Fast but not accurate
def colorDistance(c1, c2):
    r = c1[0] - c2[0]
    g = c1[1] - c2[1]
    b = c1[2] - c2[2]
    distance = math.sqrt(30 * r**(2) + 59 * g**(2) + 11 * b**(2))
    return(distance)


def getClosestColor(color, pallete):
    closest = pallete[0]
    min_dist = colorDistance(color, closest)
    for c in pallete:
        dist = colorDistance(color, c)
        if(dist < min_dist):
            # To add noise
            if(random.randint(0, 255) % 2):
                closest = c
                min_dist = dist
    return(closest)


def makeColorPallete(colors):
    pallete = []
    for color in colors:
        pallete.append([int(color['value'][1:3], 16), int(
            color['value'][3:5], 16), int(color['value'][5:7], 16)])
    return(pallete)


def style(path):
    req = urllib.request.Request(path, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(req).read()

    img = np.asarray(bytearray(webpage), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    r = requests.get(hexbot_base, params={'count': COUNT})
    pallete = makeColorPallete(r.json()['colors'])

    height, width, channels = img.shape
    final_img = np.zeros((height, width, channels), dtype=np.uint8)

    for i in range(width):
        for j in range(height):
            col = getClosestColor(img[j][i], pallete)
            cv2.circle(final_img, (i, j), 3, col)
        print(i/width)
    return(final_img)


@app.route('/')
def homepage():
    path = requests.get(url, params={'client_id': client_id}).json()[
        'urls']['small']
    session['path'] = path
    return(render_template('index.html', path=path, styled=False))


@app.route('/pointillize/')
def pointillize():
    if(not 'path' in session):
        return(redirect(url_for('homepage')))

    stylized_image = style(session['path'])
    stylized_path = 'image/'+time.ctime().replace(' ', '_') + '.jpg'
    cv2.imwrite('static/' + stylized_path, stylized_image)
    return(render_template('index.html', path=url_for('static', filename=stylized_path), styled=True))


if __name__ == "__main__":
    app.run(debug=True)
