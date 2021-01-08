#API Reference 

## Error Handling

Errors are returned as JSON objects in the following format:

    {
        "success": False,
        "error": 404,
        "messege": "Not Found"
    }

The Api will return three error types on failed requests:

- 401: not authorized
- 403: forbidden
- 404: resource not found
- 422: unprocessable
- 500: internal server error

## Api Endpoints

	
### GET '/menuitems'

- description
    - returns a list of menuitems, success value, total items value
    - the result is paginated with 10 items a page, include a request argument of the page's number starting from 1 '?page=1'
    - requires auth `get:menu_items`


- sample request: curl http://127.0.0.1:5000/menuitems -H "Authorization: Bearer <jwt-access_token>"
  
		{
		    "menu_items": [
			{
			    "active": true,
			    "category": 1,
			    "description": "test name",
			    "id": 1,
			    "ingredients": "test name",
			    "name": "test name"
			},
			{
			    "active": true,
			    "category": 1,
			    "description": "test name",
			    "id": 2,
			    "ingredients": "test name",
			    "name": "test name"
			}

		    ],
		    "success": true,
		    "total_items": 2
		}
		
### GET '/menuitems/<item-id>'

- description
    - returns a menuitem by id, success value
    - requires auth `get:item_details`

- sample request: curl http://127.0.0.1:5000/menuitems/2 -H "Authorization: Bearer <jwt-access_token>"
  
		{
		    "menu_item": {
			"active": true,
			"category": 1,
			"description": "test name",
			"id": 2,
			"ingredients": "test name",
			"name": "test name"
		    },
		    "success": true
		}
### POST '/menuitems'

- description
    - adds a new menu item to the database, returns the created menu item, success value
    - requires auth `post:menu_item`
    
- sample request: curl -X POST http://127.0.0.1:5000/menuitems -H "Content-Type: application/json" -H "Authorization: Bearer <jwt-access_token>" -d '{"name": "test name","category": 1,"description": "test name","ingredients": "test name","active": true}'
  
		{
		    "new_item": {
			"active": true,
			"category": 1,
			"description": "test name",
			"id": 88,
			"ingredients": "test name",
			"name": "test name"
		    },
		    "success": true
		}
		
### DELETE '/menuitems/<item_id>'

- description
    - deletes a menu item with a given ID if it exists, returns the id of the deleted item, success value, and a message
    - requires auth `delete:menu_item`
    
- sample request: curl -X DELETE http://127.0.0.1:5000/menuitems/2 -H "Authorization: Bearer <jwt-access_token>"
  
        {
          "deleted": 2, 
          "message": "Question Deleted", 
          "success": true
        }

### GET '/categories'

- description
  - Fetches a list of categories, success value, total categories
  - the result is paginated with 10 categories a page, include a request argument of the page's number starting from 1 '?page=1'

- sample request: curl http://127.0.0.1:5000/categories

		{
		    "categories": [
			{
			    "id": 1,
			    "name": "drink"
			},
			{
			    "id": 2,
			    "name": "chicken"
			},
			{
			    "id": 3,
			    "name": "beef"
			}
		    ],
		    "success": true,
		    "total_categories": 3
		}

### POST '/categories'

- description
    - adds a new category to the database, returns a message, success value
    - requires auth `post:category`
- sample request: curl -X POST http://127.0.0.1:5000/categories -H "Content-Type: application/json" -H "Authorization: Bearer <jwt-access_token>" -d '{"name": "test name", "description":"desc"}'
  
		{
		    "message": "Category Added",
		    "success": true
		}

### PATCH '/categories/<cat-id>'

- description
    - edit an existing category, returns the edited category, success value
    - requires auth `patch:category`
- sample request: curl -X PATCH http://127.0.0.1:5000/categories -H "Content-Type: application/json" -H "Authorization: Bearer <jwt-access_token>" -d '{"name": "test name", "description":"desc"}'
  
		{
		    "edited_category": {
			"description": "TestCategory",
			"id": 2,
			"name": "ll"
		    },
		    "success": true
		}
