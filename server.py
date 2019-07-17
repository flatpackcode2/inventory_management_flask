import peeweedbevolve
from flask import Flask, render_template, request, redirect, flash, url_for
from models import db, Store, Warehouse
app = Flask(__name__)

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/store/<id>')
def store_show(id):
    return render_template('store.html', store_id=id)

@app.route('/stores')
def store_show():
    stores = Store.select()
    warehouses = Warehouse.select()
    return render_template('stores.html', stores=stores, warehouses = warehouses)

@app.route('/store_form', methods=['POST'])
def store_form():
    name=request.form.get('store_name')
    s = Store(name=name)

    if s.save():
        # flash("Successfully saved!") #Set flash for another time. Uses secret key: https://flask.palletsprojects.com/en/1.0.x/quickstart/#sessions
        return redirect(url_for('store'))
    else:
        return render_template('store.html', name=name)

@app.route('/warehouse')
def warehouse():
    query = Store.select()
    return render_template('warehouse.html', stores = query )

@app.route('/warehouse_create', methods=[ "POST"])
def warehouse_create():
    location = request.form.get('warehouse_location')
    store_id = request.form.get('store_id')

    store =Store.get(Store.id == store_id)
    w = Warehouse(location=location, store=store)

    if w.save():
        return redirect(url_for('warehouse'))
    else:
        return render_template('warehouse.html')

if __name__ == '__main__':
    app.run()