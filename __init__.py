import os

import urllib3

import route

urllib3.disable_warnings()
from flask import Flask
import logging
import config

project_root_path = os.getcwd()  # 项目根目录
config.init()

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)

route.init(app)

logging.basicConfig()
