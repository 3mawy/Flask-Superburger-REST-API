import os
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from models import setup_db, MenuItem, Category, Size, update
from auth import requires_auth

ITEMS_PER_PAGE = 8


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]
    if len(current_items) == 0:
        abort(404)
    return current_items


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/menuitems', methods=["GET"])
    @requires_auth('get:menu_items')
    def get_menu_items(jwt):
        try:
            items = MenuItem.query.order_by(MenuItem.id).all()
            paginated_menu = paginate(request, items)

            return jsonify({
                'success': True,
                'menu_items': paginated_menu,
            })
        except:
            if len(items) or len(paginated_menu) == 0:
                abort(404)
            abort(500)

    @app.route('/menuitems/<int:item_id>', methods=["GET"])
    @requires_auth('get:item_details')
    def get_item_details(jwt, item_id):
        try:
            item = MenuItem.query.filter(MenuItem.id == item_id).one_or_none()

            formated_item = item.format()
            return jsonify({
                'success': True,
                'menu_item': formated_item,
            })
        except:
            if item is None:
                abort(404)
            abort(500)

    @app.route('/menuitems', methods=["POST"])
    @requires_auth('post:menu_item')
    def add_menu_item(jwt):
        try:
            data = request.get_json()

            name = data.get('name', 'Test')
            category = data.get('category', 2)
            description = data.get('description', 'Test')
            ingredients = data.get('ingredients', 'Test')
            active = data.get('active', True)

            if 'item_id' in data:
                item_id = data.get('item_id', )
                item = MenuItem(id=item_id, name=name, category_id=category, description=description,
                                ingredients=ingredients, active=active, )
            else:
                item = MenuItem(name=name, category_id=category, description=description,
                                ingredients=ingredients, active=active, )
            item.insert()
            return jsonify({
                'success': True,
                'new_item': item.format(),
            })
        except:
            abort(500)

    @app.route('/menuitems/<int:item_id>', methods=["DELETE"])
    @requires_auth('delete:menu_item')
    def delete_menu_item(jwt, item_id):
        try:
            item = MenuItem.query.filter(MenuItem.id == item_id).one_or_none()
            item.delete()
            return jsonify({
                'success': True,
                'deleted': item_id,
                'message': 'Question Deleted'
            })
        except:
            if item is None:
                abort(404)
            abort(500)

    @app.route('/categories', methods=["GET"])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            paginated_categories = paginate(request, categories)

            return jsonify({
                'success': True,
                'categories': paginated_categories,
            })
        except:
            if len(categories) or paginated_categories == 0:
                abort(404)
            abort(500)

    @app.route('/categories', methods=["POST"])
    @requires_auth('post:category')
    def add_category(jwt):
        data = request.get_json()
        name = data.get('name', 'TestCategoryName')
        description = data.get('description', 'TestCategoryDesc')
        try:
            category = Category(name=name, description=description)
            category.insert()
            return jsonify({
                'success': True,
                'message': 'Category Added',
            })
        except:
            abort(500)

    @app.route('/categories/<int:category_id>', methods=["PATCH"])
    @requires_auth('patch:category')
    def edit_category(jwt, category_id):
        data = request.get_json()
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()
            if category is None:
                abort(404)
            if 'name' in data:
                name = data.get('name')
            else:
                name = category.name
            if 'description' in data:
                description = data.get('description')
            else:
                description = category.description
            category = Category(name=name, description=description)
            update()
            return jsonify({
                'success': True,
                'edited_item': category.format(),
            })
        except:
            abort(500)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(401)
    def not_authorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "not authorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
