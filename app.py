from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import flash, jsonify

# IMPORTS FOR CRUD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, User, engine

# IMPORTS FOR USER LOGIN SESSION
from flask import session as login_session
import random
import string

# IMPORTS FOR TALKING TO GOOGLE SERVERS
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read()
    )['web']['client_id']

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app.secret_key = 'secret'


# gets all items
@app.route('/')
@app.route('/catalog/')
def allItems():
    session = DBSession()
    all_items = session.query(Item).order_by((Item.id).desc())
    if 'username' in login_session:
        return render_template(
            'authcatalog.html', all_items=all_items)
    else:
        return render_template(
            'catalog.html', all_items=all_items)


# adds a new item
@app.route('/catalog/new/', methods=['GET', 'POST'])
def addItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['desc']
        category = request.form['category']
        user_id = login_session['user_id']
        session = DBSession()
        new_item = Item(
            name=name,
            description=description,
            category=category,
            user_id=user_id)

        session.add(new_item)
        session.commit()
        return redirect(url_for('allItems'))
    else:
        return render_template('new.html')


# edits an item
@app.route('/catalog/<int:item_id>/edit/', methods=['POST', 'GET'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')

    session = DBSession()
    item_changing = session.query(Item).filter_by(id=item_id).one()
    if item_changing.user_id != login_session['user_id']:
        output = "you are unauthorized to edit this item"
        return output
    if request.method == 'POST':
        item_changing.name = request.form['name']
        item_changing.description = request.form['desc']
        item_changing.category = request.form['category']
        session.add(item_changing)
        session.commit()
        return redirect(url_for('viewItem', item_id=item_id))
    else:
        return render_template('edit.html', item=item_changing)


# deletes an item
@app.route('/catalog/<int:item_id>/delete/', methods=['POST', 'GET'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = DBSession()
    item_deleting = session.query(Item).filter_by(
        id=item_id).one()
    if item_deleting.user_id != login_session['user_id']:
        output = "you are unauthorized to delete this item"
        return output
    if request.method == 'POST':
        session.delete(item_deleting)
        session.commit()
        return redirect(url_for('get%s' % item_deleting.category))
    else:
        return render_template('delete.html', item=item_deleting)


# gets an item
@app.route('/catalog/<int:item_id>/item/')
def viewItem(item_id):
    session = DBSession()
    item = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return render_template('publicitem.html', item=item)
    if item.user_id != login_session['user_id']:
        return render_template('publicitem.html', item=item)
    return render_template('item.html', item=item)


# gets all items in the electronics category
@app.route('/catalog/electronics/')
def getElectronics():
    session = DBSession()
    cat_name = 'Electronics'
    category = session.query(Item).filter_by(
        category=cat_name).all()
    return render_template(
        'category.html',
        category=category,
        cat_name=cat_name
        )


# gets all items in the groceries category
@app.route('/catalog/groceries/')
def getGroceries():
    session = DBSession()
    cat_name = 'Groceries'
    category = session.query(Item).filter_by(
        category=cat_name).all()
    return render_template(
        'category.html',
        category=category,
        cat_name=cat_name
        )


# gets all items in the clothing category
@app.route('/catalog/clothing/')
def getClothing():
    session = DBSession()
    cat_name = 'Clothing'
    category = session.query(Item).filter_by(
        category=cat_name).all()
    return render_template(
        'category.html',
        category=category,
        cat_name=cat_name
        )


# gets all items in the footwear category
@app.route('/catalog/footwear/')
def getFootwear():
    session = DBSession()
    cat_name = 'Footwear'
    category = session.query(Item).filter_by(
        category=cat_name).all()
    return render_template(
        'category.html',
        category=category,
        cat_name=cat_name
        )


# gets all items in the astronomy category
@app.route('/catalog/astronomy/')
def getAstronomy():
    session = DBSession()
    cat_name = 'Astronomy'
    category = session.query(Item).filter_by(
        category=cat_name).all()

    return render_template(
        'category.html',
        category=category,
        cat_name=cat_name
        )


# login route that takes you to the fine google button
@app.route('/login')
def login():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
            ) for x in xrange(32)
        )
    login_session['state'] = state

    return render_template(
        'login.html',
        state=login_session['state'],
        CLIENT_ID=CLIENT_ID
        )


# google login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets(
            'client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'),
            401
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token
        )
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    result = json.loads(response)
    # If there was an error
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # verify that the access token is used for the intended user
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user Id doesn't match given user Id."),
            401
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    # check if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_google_id = login_session.get('google_id')
    if stored_credentials is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected'),
            200
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access-token'] = access_token
    login_session['google_id'] = google_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo/"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # set login sessions
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # check if user exists, creates new user if not
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome '
    output += login_session['username']
    output += '</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '">'
    return output


# disconnect a connected user
@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('access-token')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected'),
            401
            )
        response.headers['Content-Type'] = 'application/json'
        return response
    # execute HTTP GET request to revoke current token
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token

    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # reset user session
        del login_session['access-token']
        del login_session['google_id']
        del login_session['user_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return redirect(url_for('allItems'))
    else:
        # reset user session
        del login_session['access-token']
        del login_session['google_id']
        del login_session['user_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
            json.dumps('Failed to revoke user.. session already expired'),
            400
            )
        response.headers['Content-Type'] = 'application/json'
        return response


# Helper functions

# creates new user
def createUser(login_session):
    session = DBSession()
    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
        )

    session.add(new_user)
    session.commit()

    user = session.query(User).filter_by(
        email=login_session['email']).one()
    return user.id


# gets user information
def getUserInfo(user_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


# gets user id
def getUserId(email):
    try:
        session = DBSession()
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON ENDPOINTS
@app.route('/catalog/<int:item_id>/item/JSON')
# get a specific item in json format
def getItemJSON(item_id):
    session = DBSession()
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=[item.serialize])


# all items in json format
@app.route('/catalog/JSON')
def getAllItemJSON():
    session = DBSession()
    all_items = session.query(Item).order_by((Item.id).desc())
    return jsonify(all_items=[item.serialize for item in all_items])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
