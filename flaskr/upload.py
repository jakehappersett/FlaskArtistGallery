import os
from flask import current_app, Blueprint, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename


bp = Blueprint('upload', __name__, url_prefix='/upload')


def create_dir(imagePath):
    """
    Search for image directory,
    if it does not exist create it

    :return: directory path
    """

    if not (os.path.isdir(imagePath)):
        os.makedirs(imagePath)

    return imagePath


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check to see if the post request has the file part
        if 'file' not in request.files:
            flash('No File selected')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('File needs a valid name')
        if file.filename in os.listdir(current_app.config['UPLOAD_FOLDER']):
            flash('File ' + file.filename + ' already uploaded')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash(filename + ' saved')
            # return redirect(url_for('.uploaded_file', filename=filename))
            return redirect(url_for('gallery.show_gallery'))
        else:
            flash('File extension not supported - tell Jake about this and he will fix it')
    return render_template('upload/upload.html')


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


