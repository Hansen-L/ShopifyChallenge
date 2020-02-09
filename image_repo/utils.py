from flask import url_for, current_app
from PIL import Image
import secrets, os

def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)  # Get the extention from the picture
    picture_fn = random_hex + f_ext  # Rename the picture with a random hex
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)

    output_size = (300, 300)  # Save the image as 300px wide while preserving aspect ratio
    i = Image.open(picture)
    i.thumbnail(output_size)

    i.save(picture_path)  # Save the image to the static/images directory
    return picture_fn