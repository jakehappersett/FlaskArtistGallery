import os
from flask import Flask, url_for


def create_app(test_config=None):
    # create flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.root_path, 'static'),
        ALLOWED_EXTENSIONS=set(['jpg', 'jpeg', 'gif', 'png'])

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

    @app.route('/hello')
    def hello():
        return "hello"

    from . import upload
    # TODO : make upload folder dynamic and editable at runtime
    # upload_folder = upload.create_dir('/home/jake/images')
    app.register_blueprint(upload.bp)

    from . import gallery
    app.register_blueprint(gallery.bp)

    # from . import db
    # db.init_app(app)
    #
    # from . import auth
    # app.register_blueprint(auth.bp)
    #
    # from . import blog
    # app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')

    return app

