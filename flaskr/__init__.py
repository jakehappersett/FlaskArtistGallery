import os
from flask import Flask, render_template


def create_app(test_config=None):
    # create flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.root_path, 'static'),
        ALLOWED_EXTENSIONS=set(['jpg', 'jpeg', 'gif', 'png']),
        USERNAME='lex',
        PASSWORD='lex'

    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    from . import upload
    app.register_blueprint(upload.bp)

    from . import gallery
    app.register_blueprint(gallery.bp)
    app.add_url_rule('/', endpoint='index')

    return app
