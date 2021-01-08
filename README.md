# Super Burger Api

Super Burger is a local fastfood restauraunt located in Egypt, Suez, We are developing this website to make the ordering proccess easier, have a better represintation of menu data with images and full description and more features 
This API will be connected to a react frontend and a mobile application
All backend code follows PEP8 style guidelines. 

- Local ENV, Hosted by default at http://127.0.0.1:5000/
- Hosted LIVE at https://superburger-suez.herokuapp.com/
- Authentication: Auth0 JWT, auth login samples can be found in the "auth0 credentials.md" file

##Getting Started

### Installing Dependencies

#### Virtual Enviornment

python3 -m virtualenv env   
source env/bin/activate

#### PIP Dependencies
 
pip3 install -r requirements.txt

#### Run The App

. setup.sh  
flask run 

### Setup Auth0 

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:menu_items`
    - `get:item_details`
    - `post:menu_item`
    - `delete:menu_item`
    - `post:category`
    - `patch:category`
6. Create new roles for:
    - Admin
        - can perform all actions
    - Cashier
        - can `get:menu_items`
        - can `get:item_details`
        - can `post:menu_item`
        - can `post:category`
    - User
        - can `get:menu_items`
        - can `get:item_details`
7. Test the endpoints with [Postman](https://getpostman.com). 
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`


### Testing
To run the tests, run

```
dropdb capstone_test
createdb capstone_test
python3 test_app.py
```

##API Reference

Can be fount at the "APIReference.md" file

##Deployment

heroku create <name_of_your_app>

note `add the env variables at "setup.sh" to heroku's Config Vars`

git remote add heroku <heroku_git_url>.

heroku addons:create heroku-postgresql:hobby-dev --app <name_of_your_app>

heroku config --app <name_of_your_app>

heroku git:remote -a <name_of_your_app>

git push heroku main

heroku run python3 manage.py db upgrade --app <name_of_your_app>


