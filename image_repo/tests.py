from image_repo import create_app, db
from image_repo.models import Images
from image_repo.utils import save_picture, delete_picture, save_pictures_zip
from image_repo.forms import UploadPictureForm
import os
import unittest

class TestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_upload_single_image(self):
        i = Images(image_file='test.jpg')
        with self.app.app_context():
            db.session.add(i)
            db.session.commit()
            assert Images.query.get(1).image_file == 'test.jpg'

    def test_upload_multiple_images(self):
