import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, MenuItem, Category

default_path = 'postgres://postgres:0153@localhost:5432/capstone_test'
database_path = os.getenv('TEST_DATABASE_URL', default_path)
auth = os.getenv('AUTHORIZATION_BEARER')
test_id = 525
test_delete_id = 772


class SuperTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        self.new_category = {
            'name': 'test name',
            'description': 'from test'
        }
        self.new_menuitem = {
            'item_id': test_id,
            'name': 'test name',
            'category': 1,
            'description': 'test name',
            'ingredients': 'test name',
            'active': True
        }
        self.to_be_deleted = {
            'item_id': test_delete_id,
            'name': 'test delete name',
            'category': 1,
            'description': 'test name',
            'ingredients': 'test name',
            'active': True
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.client().post('/menuitems', json=self.to_be_deleted, headers={'Authorization': auth})

    def tearDown(self):
        """Executed after reach test"""
        self.client().delete('/menuitems/' + str(test_delete_id), headers={'Authorization': auth})
        self.client().delete('/menuitems/' + str(test_id), headers={'Authorization': auth})
        pass

    def test_add_category(self):
        res = self.client().post('/categories', json=self.new_category, headers={'Authorization': auth})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Category Added')

    def test_401_invalid_auth_add_category(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'not authorized')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['categories'])

    def test_404_beyond_valid_page_categories(self):
        res = self.client().get('/categories?page=400', headers={'Authorization': auth})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_edit_category(self):
        res = self.client().patch('/categories/1', json={'name': 'new name'}, headers={'Authorization': auth})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['edited_item'])

    def test_404_edit_category_does_not_exist(self):
        res = self.client().get('/category/400', json={'name': 'new name'}, headers={'Authorization': auth})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_add_menu_item(self):
        res = self.client().post('/menuitems', json=self.new_menuitem, headers={'Authorization': auth})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['new_item'])

    def test_401_invalid_auth_add_MenuItem(self):
        res = self.client().post('/menuitems')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'not authorized')

    def test_get_menu_items(self):
        res = self.client().get('/menuitems', headers={'Authorization': auth})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['menu_items'])

    def test_404_beyond_valid_page_menu_item(self):
        res = self.client().get('/menuitems?page=400', headers={'Authorization': auth})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_get_menu_item(self, x=test_id):
        self.client().post('/menuitems', json=self.new_menuitem, headers={'Authorization': auth})

        res = self.client().get('/menuitems/' + str(x), headers={'Authorization': auth})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['menu_item'])

    def test_404_get_menu_item_does_not_exist(self):
        res = self.client().get('/menuitems/400', headers={'Authorization': auth})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_menu_item(self, x=test_delete_id):
        res = self.client().delete('/menuitems/' + str(x), headers={'Authorization': auth})
        data = json.loads(res.data)
        question = MenuItem.query.get(x)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Question Deleted')
        self.assertEqual(data['deleted'], x)
        self.assertIsNone(question)

    def test_404_delete_menu_item_does_not_exist(self):
        res = self.client().delete('/menuitems/400', headers={'Authorization': auth})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')


if __name__ == "__main__":
    unittest.main()
