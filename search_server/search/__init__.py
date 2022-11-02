

import flask
import search

app = flask.Flask(__name__)
app.config.from_object('search.config')

import search.views
import search.model