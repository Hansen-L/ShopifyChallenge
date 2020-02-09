from image_repo import create_app, db
from image_repo.models import Images
from flask import render_template, url_for, flash, redirect, request
from image_repo.models import Images
from image_repo.utils import save_picture
from image_repo.forms import UploadPictureForm

app = create_app()

@app.route("/", methods=['GET', 'POST'])
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    form = UploadPictureForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)  # Saves the picture and returns the filepath
        image = Images(image_file=picture_file)
        db.session.add(image)
        db.session.commit()
        flash('Images uploaded!', 'success')
    return render_template('upload.html', title='Upload Images', form=form)
# @app.route("/", methods=['POST'])


@app.route("/gallery", methods=['GET'])
def gallery():
    images = Images.query.all()
    # for image in images:
        # print(url_for('static',filename='images/' + image.image_file))
    # print(images)
    # print( url_for('static', filename='images/ba204e0f0a11ba93.jpg') )
    return render_template('gallery.html', images=images)


if __name__=='__main__':
    app.run(debug=True)