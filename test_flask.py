from unittest import TestCase

from app import app
from models import db, User, Post

# Use a test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2118@localhost/blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors
app.config['TESTING'] = True

# Cancel Flask DebugToolbar

app.config['DEBUG_TB_HOSTS'] = ['don’t-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
	"""Tests for User Views"""

	def setUp(self):
		"""Add sample user"""

		# Post.query.delete()
		# User.query.delete()
		
		user = User(first_name = 'John', last_name = 'Smith', image_url = 'https://cdn.pixabay.com/photo/2014/04/03/11/08/american-football-311817_960_720.png')
		db.session.add(user)
		db.session.commit()

	def tearDown(self):
		"""Clear transactions"""

		db.session.rollback()

	def test_show_users(self):
		with app.test_client() as client:
			resp = client.get('/users')
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn('John', html)

	def test_show_user_info(self):
		with app.test_client() as client:
			resp = client.get(f"/users")
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn('John Smith', html)

	def test_add_new_user(self):
		with app.test_client() as client:
			new_user = {"first_name": "Bob", "last_name": "Test", "image_url": "https://cdn.pixabay.com/photo/2018/01/06/23/25/snow-3066167_960_720.jpg"}
			resp = client.post("/users/new", data=new_user, follow_redirects=True)
			html = resp.get_data(as_text=True)
			
			self.assertEqual(resp.status_code, 200)
			self.assertIn('Bob Test', html)

	def test_delete_user(self):
		with app.test_client() as client:
			resp = client.get(f"/users")

			self.assertEqual(resp.status_code, 200)


class PostViewsTestCase(TestCase):
	"""Tests for Post Views"""
	def setUp(self):
		"""Add sample user"""

		# Post.query.delete()
		# User.query.delete()
		
		user = User(first_name = 'John', last_name = 'Smith', image_url = 'https://cdn.pixabay.com/photo/2014/04/03/11/08/american-football-311817_960_720.png')
		db.session.add(user)
		db.session.commit()

		"""Add sample post"""

		Post.query.delete()
		
   		# user = User.query.get_or_404(user_id)
		post = Post(title= 'Test Post Title', content ='Testing the post content', user_id=1)

		db.session.add(post)
		db.session.commit()


	def tearDown(self):
		"""Clear transactions"""

		db.session.rollback()

	def test_show_post(self):
		with app.test_client() as client:
			resp = client.get('/posts/2')
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn('John', html)
			self.assertIn('Test Post', html)

	def test_delete_post(self):
		with app.test_client() as client:
			resp = client.get("/users/1")
			
			self.assertEqual(resp.status_code, 200)