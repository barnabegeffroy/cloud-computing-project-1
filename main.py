import google.oauth2.id_token
from flask import Flask, render_template, request, redirect, url_for
from google.auth.transport import requests
from google.cloud import datastore

app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', message=request.args.get('message'), status=request.args.get('status'))


@app.route('/login')
def login():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('login.html', user_data=claims, error_message=error_message)


@app.route('/find_cars')
def findCars():
    return render_template('find_cars.html')


@app.route('/add_car', methods=['GET'])
def addCar():
    return render_template('add_car.html', message=request.args.get('message'), status=request.args.get('status'))


def createCar(name, manufacturer, year, battery, wltp, cost, power):
    id = abs(hash(name + manufacturer + year))
    entity_key = datastore_client.key(
        'Vehicles', id)
    if datastore_client.get(entity_key):
        return None
    entity = datastore.Entity(entity_key)
    entity.update({
        'name': name,
        'manufacturer': manufacturer,
        'year': year,
        'battery': battery,
        'wltp': wltp,
        'cost': cost,
        'power': power,
    })
    datastore_client.put(entity)
    return id


@ app.route('/put_car', methods=['POST'])
def putCar():
    id_token = request.cookies.get("token")
    message = None
    status = None
    if id_token:
        try:
            id = createCar(
                request.form['name'], request.form['manufacturer'], request.form['year'], request.form['battery'], request.form['wltp'], request.form['cost'], request.form['power'])
            if id == None:
                message = "You can't add this vehicle, it already exists !"
                status = "error"
            else:
                message = "The vehicle has been added succesfully !"
                status = "success"
                return redirect(url_for('.carInfo', id=id, message=message, status=status))
        except ValueError as exc:
            error_message = str(exc)
    else:
        message = "You can't add a vehicul without being logged in"
        status = "error"

    return redirect(url_for('.addCar', message=message, status=status))


@ app.route('/search_cars', methods=['GET'])
def searchCars():
    result = None
    query = datastore_client.query(kind='Vehicles')

    if request.args.get('name') != '':
        query.add_filter('name', '=', request.args.get('name'))

    if request.args.get('manufacturer') != '':
        query.add_filter('manufacturer', '=', request.args.get('manufacturer'))

    if request.args.get('min_year' != ''):
        query.add_filter('year', '>=', request.args.get('min_year'))

    if request.args.get('max_year') != '':
        query.add_filter('year', '<=', request.args.get('max_year'))

    if request.args.get('min_battery') != '':
        query.add_filter('battery', '>=', request.args.get('min_battery'))

    if request.args.get('max_battery') != '':
        query.add_filter('battery', '<=', request.args.get('max_battery'))

    if request.args.get('min_wltp') != '':
        query.add_filter('wltp', '>=', request.args.get('min_wltp'))

    if request.args.get('max_wltp') != '':
        query.add_filter('wltp', '<=', request.args.get('max_wltp'))

    if request.args.get('min_cost') != '':
        query.add_filter('cost', '>=', request.args.get('min_cost'))

    if request.args.get('max_cost') != '':
        query.add_filter('cost', '<=', request.args.get('max_cost'))

    if request.args.get('min_power') != '':
        query.add_filter('power', '>=', request.args.get('min_power'))

    if request.args.get('max_power') != '':
        query.add_filter('power', '<=', request.args.get('max_power'))

    result = query.fetch()

    return render_template('result.html', cars_list=result)


def findCar(id):
    entity_key = datastore_client.key('Vehicles', id)
    entity = datastore_client.get(entity_key)
    return entity


@ app.route('/car_info/<int:id>', methods=['GET'])
def carInfo(id):
    car = findCar(id)
    if car:
        return render_template('car.html', car=car, message=request.args.get('message'), status=request.args.get('status'))
    else:
        return redirect(url_for('.root', message="This car does not exist", status="error"))


def deleteCarsById(id):
    entity_key = datastore_client.key('Vehicles', id)
    datastore_client.delete(entity_key)


@ app.route('/delete_car', methods=['POST'])
def deleteCar():
    id_token = request.cookies.get("token")
    message = None
    status = None
    if id_token:
        try:
            deleteCarsById(int(request.form['car_id_delete']))
            message = "Vehicle has been deleted !"
            status = "success"
        except ValueError as exc:
            error_message = str(exc)
    else:
        message = "You must log in to delete a vehicle"
        status = "error"
    return redirect(url_for('.root', message=message, status=status))


def updateCarInfo(id, new_name, new_manufacturer, new_year, new_battery, new_wltp, new_cost, new_power):
    entity_key = datastore_client.key('Vehicles', id)
    entity = datastore.Entity(key=entity_key)
    entity.update({
        'name': new_name,
        'manufacturer': new_manufacturer,
        'year': new_year,
        'battery': new_battery,
        'wltp': new_wltp,
        'cost': new_cost,
        'power': new_power,
    })
    datastore_client.put(entity)


@ app.route('/edit_car', methods=['POST'])
def editCar():
    id_token = request.cookies.get("token")
    message = None
    status = None
    car_id = int(request.form['car_id_update'])
    if id_token:
        if request.form['new_name'] == request.form['current_name'] and request.form['new_manufacturer'] == request.form['current_manufacturer'] and request.form['new_year'] == request.form['current_year']:
            updateCarInfo(car_id, request.form['new_name'], request.form['new_manufacturer'], request.form['new_year'],
                          request.form['new_battery'], request.form['new_wltp'], request.form['new_cost'], request.form['new_power'])
            message = "Vehicle has been updated !"
            status = "success"

        else:
            new_car_id = createCar(request.form['new_name'], request.form['new_manufacturer'], request.form['new_year'],
                                   request.form['new_battery'], request.form['new_wltp'], request.form['new_cost'], request.form['new_power'])
            if car_id:
                deleteCarsById(car_id)
                car_id = new_car_id
                message = "Vehicle has been updated !"
                status = "success"
            else:
                message = "The information you wish to add corresponds to an existing vehicle"
                status = "error"
    else:
        message = "You must log in to update a vehicle"
        status = "error"
    return redirect(url_for('.carInfo', id=car_id, message=message, status=status))


@ app.route('/compare')
def compare():
    result = None
    query = datastore_client.query(kind='Vehicles')
    result = query.fetch()
    return render_template('compare.html', cars_list=result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
