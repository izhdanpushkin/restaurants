from flask import Flask, url_for, render_template, redirect, request, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine

Session = sessionmaker(bind = engine)
sess = Session()

app = Flask(__name__)
app.secret_key = 'meow'

#JSON requests handling
@app.route('/restaurant/JSON')
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = sess.query(Restaurant).all()
    return jsonify(Restaurants = [e.serialize for e in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def menuJSON(restaurant_id):
    items = sess.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
    return jsonify(MenuItems = [e.serialize for e in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    item = sess.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id, MenuItem.id == menu_id).first()
    return jsonify(MenuItem = item.serialize)

@app.route('/')
@app.route('/restaurant')
@app.route('/restaurants')
def showRestaurants():
    # return 'This page will show all my restaurants'
    restaurants = sess.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new', methods = ['GET', 'POST'])
def newRestaurant():
    # return 'This page will be for making a new restaurant'
    if request.method == 'POST':
        newRest = Restaurant(name = request.form['name'])
        sess.add(newRest)
        sess.commit()
        flash('New restaurant created')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    # return 'This page will be for editing restaraunt {}'.format(restaurant_id)
    restaurant = sess.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if request.method == 'POST':
        editRest = restaurant
        editRest.name = request.form['name']
        sess.add(editRest)
        sess.commit()
        flash('Restaurant successfully edited')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    # return 'This page will be for deleting restaraunt {}'.format(restaurant_id)
    restaurant = sess.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if request.method == 'POST':
        sess.delete(restaurant)
        sess.commit()
        flash('Restaurant successfully deleted')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    # return 'This page is the menu for restaurant {}'.format(restaurant_id)
    restaurant = sess.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    items = sess.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    # return 'This page is for making a new menu item for restaurant {}'.format(restaurant_id)
    restaurant = sess.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if request.method == 'POST':
        newMI = MenuItem(name = request.form['name'],
            price = request.form['price'],
            description = request.form['description'],
            course = request.form['course'],
            restaurant_id = restaurant.id)
        sess.add(newMI)
        sess.commit()
        flash('Menu item created')
        return redirect(url_for('showMenu', restaurant_id = restaurant.id))
    else:
        return render_template('newmenuitem.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # return 'This page is for editing menu item {} for restaurant {}'.format(menu_id, restaurant_id)
    restaurant = sess.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    item = sess.query(MenuItem).filter(MenuItem.restaurant_id == restaurant.id, MenuItem.id == menu_id).first()
    if not item:
        return redirect(url_for('showMenu', restaurant_id = restaurant.id))
    if request.method == 'POST':
        editMI = item
        if request.form['name']:
            editMI.name = request.form['name']
        if request.form['price']:
            editMI.price = request.form['price']
        if request.form['description']:
            editMI.description = request.form['description']
        if request.form['course']:
            editMI.course = request.form['course']
        sess.add(editMI)
        sess.commit()
        flash('Menu item successfully edited')
        return redirect(url_for('showMenu', restaurant_id = restaurant.id))
    else:
        return render_template('editmenuitem.html', restaurant = restaurant, item = item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # return 'This page is for deleting menu item {}'.format(menu_id)
    restaurant = sess.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    item = sess.query(MenuItem).filter(MenuItem.restaurant_id == restaurant.id, MenuItem.id == menu_id).first()
    if not item:
        return redirect(url_for('showMenu', restaurant_id = restaurant.id))
    if request.method == 'POST':
        sess.delete(item)
        sess.commit()
        flash('Menu item successfully deleted')
        return redirect(url_for('showMenu', restaurant_id = restaurant.id))
    else:
        return render_template('deletemenuitem.html', restaurant = restaurant, item = item)


if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)