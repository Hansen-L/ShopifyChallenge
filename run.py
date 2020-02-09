from image_repo import create_app, db
from image_repo.models import Images
from flask import render_template, url_for, flash, redirect, request
from image_repo.models import Images
from image_repo.utils import save_picture
from image_repo.forms import UploadPictureForm
import os

app = create_app()

@app.route("/", methods=['GET', 'POST'])
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    # To-do: Upload pictures using a zip file
    form = UploadPictureForm()
    if form.validate_on_submit():
        for picture in form.pictures.data:
            picture_file = save_picture(picture)  # Saves the picture and returns the filepath
            image = Images(image_file=picture_file)
            db.session.add(image)
            db.session.commit()
        if form.pictures.data:
            flash('Images uploaded!', 'success')
    return render_template('upload.html', title='Upload Images', form=form)


@app.route("/gallery", methods=['GET'])
def gallery():
    # To-do: Option between viewing your own pictures vs all available pictures
    images = Images.query.all()
    return render_template('gallery.html', images=images)

@app.route("/delete/<file_id>")
def delete(file_id):
    # To-do: Check if image author is the current user
    image = Images.query.get_or_404(file_id)
    filepath = url_for('static', filename='images/' + image.image_file)
    filepath = os.getcwd() + '/image_repo/' + filepath
    os.remove(filepath)
    db.session.delete(image)
    db.session.commit()
    flash('Your image has been deleted!', 'success')
    return redirect(url_for('gallery'))

@app.route("/delete/all")
def delete_all():
    images = Images.query.all()
    if images:
        for image in images:
            filepath = url_for('static', filename='images/' + image.image_file)
            filepath = os.getcwd() + '/image_repo/' + filepath
            os.remove(filepath)
            db.session.delete(image)
        db.session.commit()
        flash('All images have been deleted!', 'success')
    return redirect(url_for('gallery'))


if __name__=='__main__':
    app.run(debug=True)