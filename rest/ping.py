from flask import Blueprint

app = Blueprint('ping', __name__,
                url_prefix='/ping')


@app.route('')
def ping():
    return "pong"
