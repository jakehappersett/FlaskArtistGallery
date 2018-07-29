import os
from flask import current_app, Blueprint, render_template, send_from_directory
from collections import deque


bp = Blueprint('gallery', __name__, url_prefix='/gallery')


def get_image_paths():
    #todo: convert to dictionary that stores type based on folder input
    images = os.listdir(current_app.config['UPLOAD_FOLDER'])
    full = []
    for image in images:
        if image.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']:
                full.append(image)
                # full.append(send_from_directory(current_app.config['UPLOAD_FOLDER'], image))
    return full


@bp.route('/')
def show_gallery():
    files = get_image_paths()
    row_slice = int(len(files) / 4) + (len(files) % 4 > 0)  # added to round up
    return render_template('gallery/gallery.html', files=files, row_slice=row_slice)


@bp.route('/<path:filename>')
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)