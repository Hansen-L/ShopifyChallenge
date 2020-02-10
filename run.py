from image_repo import create_app, db
from image_repo.models import Images
from flask import render_template, url_for, flash, redirect, request
from image_repo.models import Images
from image_repo.utils import save_picture, delete_picture, save_pictures_zip
from image_repo.forms import UploadPictureForm
import os

app = create_app()


@app.route("/", methods=['GET', 'POST'])
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    # To-do: Upload pictures using a zip file
    form = UploadPictureForm()
    if form.validate_on_submit():
        if form.pictures.data:
            for file in form.pictures.data:
                f_ext = os.path.splitext(file.filename)[1]  # Get the extension of the uploaded file
                if f_ext == '.zip':
                    save_pictures_zip(file)
                else:  # If the files are png or jpg
                    save_picture(file)  # Saves the picture to the server and returns the filepath
            db.session.commit()
            flash('Image(s) uploaded!', 'success')
    return render_template('upload.html', title='Upload Images', form=form)


@app.route("/gallery", methods=['GET','POST'])
def gallery():
    # To-do: Option between viewing your own pictures vs all available pictures
    images = Images.query.all()
    if request.method == "POST":  # If we select images for deletion
        for image_id in request.form.getlist("images"):
            print(image_id)
            delete_picture(image_id)
        db.session.commit()
        return redirect(url_for('gallery'))  # Need this to avoid a 404 error after POST.
    return render_template('gallery.html', images=images)


@app.route("/delete/<file_id>")
def delete(file_id):
    # To-do: Check if image author is the current user
    delete_picture(file_id)
    db.session.commit()
    flash('Your image has been deleted!', 'success')
    return redirect(url_for('gallery'))


@app.route("/delete/all")
def delete_all():
    images = Images.query.all()
    if images:
        for image in images:
            delete_picture(image.id)
        db.session.commit()
        flash('All images have been deleted!', 'success')
    return redirect(url_for('gallery'))


if __name__=='__main__':
    app.run(debug=True)