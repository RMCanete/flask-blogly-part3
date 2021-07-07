
from unittest import TestCase

from app import app
from models import db, User

# Use a test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2118@localhost/blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
	"""Tests for model for Users"""
	
	def setUp(self):
		"""Add sample user"""

		User.query.delete()
		
	def tearDown(self):
		"""Clear transactions"""

		db.session.rollback()
	
	def test_full_name(self):
		user = User(first_name = 'John', last_name = 'Smith', image_url = 'https://cdn.pixabay.com/photo/2014/04/03/11/08/american-football-311817_960_720.png')
		db.session.add(user)
		db.session.commit()
		
		full_name = user.full_name
		self.assertEqual(full_name, "John Smith")	
