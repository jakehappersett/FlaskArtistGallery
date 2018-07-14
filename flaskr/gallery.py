import os
from flask import current_app, Blueprint, render_template


bp = Blueprint('gallery', __name__, url_prefix='/gallery')


def get_image_paths():
    images = os.listdir(current_app.config['UPLOAD_FOLDER'])
    full = []
    for image in images:
        if image.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']:
                full.append(image)
                # full.append(send_from_directory(current_app.config['UPLOAD_FOLDER'], image))
    return full


@bp.route('/gallery')
def show_gallery():
    files = get_image_paths()
    return render_template('gallery/simpleLightBox.html', files=files)


