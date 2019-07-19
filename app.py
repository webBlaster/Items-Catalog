from flask import Flask, render_template, url_for
from flask import request, redirect, flash, jsonify

# IMPORTS FOR CRUD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, engine

# IMPORTS FOR USER LOGIN SESSION
from flask import session as login_session
import random, string

# IMPORTS FOR TALKING TO GOOGLE SERVERS
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

app.secret_key = 'secret'
# gets all items
@app.route('/')
@app.route('/catalog/')
def allItems():
    session = DBSession()
    all_items = session.query(Item).all()
    return render_template('catalog.html', all_items = all_items)


# adds a new item
@app.route('/catalog/new/', methods = ['GET', 'POST'])
def addItem():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['desc']
        category = request.form['category']
        session = DBSession()
        new_item = Item(name = name, description = description, category = category )
        session.add(new_item)
        session.commit()
        return redirect(url_for('allItems'))
    else:
        return render_template('new.html')


# edits an item
@app.route('/catalog/<int:item_id>/edit/', methods=['POST', 'GET'])
def editItem(item_id):
    session = DBSession()
    item_changing = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
        item_changing.name = request.form['name']
        item_changing.description = request.form['desc']
        item_changing.category = request.form['category']
        session.add(item_changing)
        session.commit()
        return redirect(url_for('viewItem', item_id = item_id))
    else:
        return render_template('edit.html', item = item_changing)


# deletes an item
@app.route('/catalog/<int:item_id>/delete/', methods=['POST', 'GET'])
def deleteItem(item_id):
    session = DBSession()
    item_deleting = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(item_deleting)
        session.commit()
        return redirect(url_for('get%s' % item_deleting.category))
    else:
        return render_template('delete.html', item = item_deleting)


# gets an item
@app.route('/catalog/<int:item_id>/item/')
def viewItem(item_id):
    session = DBSession()
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('item.html', item = item)


# gets all items in the electronics category
@app.route('/catalog/electronics/')
def getElectronics():
    session = DBSession()
    cat_name = 'Electronics'
    category = session.query(Item).filter_by(category = cat_name).all()
    return render_template('category.html', category = category, cat_name = cat_name)


# gets all items in the groceries category
@app.route('/catalog/groceries/')
def getGroceries():
    session = DBSession()
    cat_name = 'Groceries'
    category = session.query(Item).filter_by(category = cat_name).all()
    return render_template('category.html', category = category, cat_name = cat_name)


# gets all items in the clothing category
@app.route('/catalog/clothing/')
def getClothing():
    session = DBSession()
    cat_name = 'Clothing'
    category = session.query(Item).filter_by(category = cat_name).all()
    return render_template('category.html', category = category, cat_name = cat_name)


# gets all items in the footwear category
@app.route('/catalog/footwear/')
def getFootwear():
    session = DBSession()
    cat_name = 'Footwear'
    category = session.query(Item).filter_by(category = cat_name).all()
    return render_template('category.html', category = category, cat_name = cat_name)


# gets all items in the astronomy category
@app.route('/catalog/astronomy/')
def getAstronomy():
    session = DBSession()
    cat_name = 'Astronomy'
    category = session.query(Item).filter_by(category = cat_name).all()
    return render_template('category.html', category = category, cat_name = cat_name)


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.
    digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state = login_session['state'], CLIENT_ID = CLIENT_ID)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    string_response = response.decode('utf-8')
    result = json.loads(string_response)
    # If there was an error
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # verify that the access token is used for the intended user
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user Id doesn't match given user Id."), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    # check if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_google_id = login_session.get('google_id')
    if stored_credentials is not None and google_id == stored_google_id:
        response = make_response(json.dumps('Current user is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
            
    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['google_id'] = google_id

    #Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo/"
    params = {'access_token': access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome'
    output += login_session['username']
    output += '</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '">'
    return output
@app.route('/logout')
def logout():
    del login_session['credentials']
    del login_session['google_id']
    del login_session['username']
    del login_session['picture']
    output = 'logout successful'
    return output