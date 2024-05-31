""" Test file for admin view functions. Created by Emmanuel. """
import os
import tempfile
import unittest

from flask_testing import TestCase
from app import app, db
from models import User
import bcrypt

# Set the environment variable for testing
os.environ['FLASK_ENV'] = 'testing'


class TestAdminViews(TestCase):

    # Method to create the Flask app with test configuration
    def create_app(self):
        # Create a temporary file for the database
        self.db_fd, self.db_path = tempfile.mkstemp()
        # Set Flask app config for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
        return app

    # Method to set up the test database
    def setUp(self):
        db.create_all()

        # Create a test admin user
        admin_password = bcrypt.hashpw(b"admin_password", bcrypt.gensalt())
        self.admin = User(
            email="admin@example.com",
            first_name="Admin",
            surname="User",
            password=admin_password,
            role='admin',
            dob="1990-01-01",
            address="Test Address",
            phone="1234567890"
        )
        # Add and commit the test admin user to the database
        db.session.add(self.admin)
        db.session.commit()

    # Method to tear down the test database
    def tearDown(self):
        db.session.remove()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    # Test accessing the admin account page without logging in
    def test_access_admin_account_without_login(self):
        response = self.client.get('/admin_account')
        self.assertRedirects(response, '/login?next=%2Fadmin_account')

    # Test accessing the admin account page with a non-admin user
    def test_access_admin_account_with_user_role(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="user@example.com",
                password="user_password"
            ), follow_redirects=True)

            response = self.client.get('/admin_account')
            self.assertEqual(response.status_code, 403)

    # Test accessing the admin account page with an admin user
    def test_access_admin_account(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="admin@example.com",
                password="admin_password"
            ), follow_redirects=True)

            response = self.client.get('/admin_account')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Admin Account Details', response.data)

    # Test accessing the create admin account page without logging in
    def test_access_create_admin_account_without_login(self):
        response = self.client.get('/create_admin_account')
        self.assertRedirects(response, '/login?next=%2Fcreate_admin_account')

    # Test accessing the create admin account page with a non-admin user
    def test_access_create_admin_account_with_user_role(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="user@example.com",
                password="user_password"
            ), follow_redirects=True)

            response = self.client.get('/create_admin_account')
            self.assertEqual(response.status_code, 403)

    # Test accessing the create admin account page with an admin user
    def test_access_create_admin_account(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="admin@example.com",
                password="admin_password"
            ), follow_redirects=True)

            response = self.client.get('/create_admin_account')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Create Admin Account', response.data)

    # Test creating an admin account with valid data
    def test_create_admin_account_with_valid_data(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="admin@example.com",
                password="admin_password"
            ), follow_redirects=True)

            response = self.client.post('/create_admin_account', data=dict(
                email="newadmin@example.com",
                first_name="New",
                last_name="Admin",
                password="new_admin_password",
                dob="1990-01-01",
                address="Test Address",
                phone="1234567890"
            ), follow_redirects=True)
            self.assertIn(b'New Admin added successfully', response.data)

    # Test creating an admin account with invalid data (duplicate email)
    def test_create_admin_account_with_invalid_data(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="admin@example.com",
                password="admin_password"
            ), follow_redirects=True)

            response = self.client.post('/create_admin_account', data=dict(
                email="admin@example.com",  # Duplicate email
                first_name="New",
                last_name="Admin",
                password="new_admin_password",
                dob="1990-01-01",
                address="Test Address",
                phone="1234567890"
            ), follow_redirects=True)
            self.assertIn(b'Email address already exists', response.data)

    # Test accessing account overview page without logging in
    def test_access_account_overview_without_login(self):
        response = self.client.get('/account_overview/1')
        self.assertRedirects(response, '/login?next=%2Faccount_overview%2F1')

    # Test accessing account overview page with a non-admin user
    def test_access_account_overview_with_user_role(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="user@example.com",
                password="user_password"
            ), follow_redirects=True)

            response = self.client.get('/account_overview/1')
            self.assertEqual(response.status_code, 403)

    # Test accessing account overview page for a nonexistent user
    def test_access_account_overview_for_nonexistent_user(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="admin@example.com",
                password="admin_password"
            ), follow_redirects=True)

            response = self.client.get('/account_overview/999')
            self.assertEqual(response.status_code, 404)

    # Test accessing account overview page with an admin user
    def test_access_account_overview(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="admin@example.com",
                password="admin_password"
            ), follow_redirects=True)

            response = self.client.get('/account_overview/1')
            self.assertEqual(response.status_code, 302)
            self.assertIn(b'Account Overview', response.data)

    # Test deleting a user with an admin user
    def test_delete_user(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="admin@example.com",
                password="admin_password"
            ), follow_redirects=True)

            response = self.client.post('/delete_user/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'User successfully deleted', response.data)

    # Test deleting a nonexistent user
    def test_delete_user_with_nonexistent_user_id(self):
        with self.client:
            self.client.post('/login', data=dict(
                email="admin@example.com",
                password="admin_password"
            ), follow_redirects=True)

            response = self.client.post('/delete_user/999', follow_redirects=True)
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
