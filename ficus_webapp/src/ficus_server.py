from flask import Flask
import datetime
import json
from datetime import datetime
import news_pull

app = Flask("ficus_server")
env_readings = {}  


@app.route("/time")
def get_time():
    now = datetime.datetime.now()
    resp = {
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'wday': now.weekday(),
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'microsecond': now.microsecond,
        'tzinfo': now.tzinfo,
        'yday' : now.timetuple().tm_yday 
    }
    return resp


@app.route("/news")
def news_feed():
    return news_pull.curate_articles()

@app.route("/env")
@app.route("/env/<fid>/<c>/<h>")
def add_env(fid, c, h):
    env_readings[fid] = (c,h)
    return "0.1"

@app.route("/version")
def server_version():
    return "0.1"