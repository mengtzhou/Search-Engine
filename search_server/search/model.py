
import search
import sqlite3
import flask

def get_db():
    
    if 'sqlite_db' not in flask.g:
        db_filename = search.app.config['DATABASE']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db

@search.app.teardown_appcontext
def close_db(error):
    
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()


