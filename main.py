import google.oauth2.id_token
from flask import Flask, render_template, request, redirect
from google.auth.transport import requests
from google.cloud import datastore

app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()


@app.route('/')
def root():
    return render_template('index.html')


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


@app.route('/all_cars')
def allCars():
    result = None
    query = datastore_client.query(kind='Vehicules')
    result = query.fetch()
    return render_template('all_cars.html', cars_list=result)


@app.route('/add_car')
def addCar():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except ValueError as exc:
            error_message = str(exc)

    return render_template('add_car.html', user_data=claims, error_message=error_message)


def createCar(name, manufacturer, year, battery, wltp, cost, power):
    entity_key = datastore_client.key('Vehicules')
    entity = datastore.Entity(key=entity_key)
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


@app.route('/put_car', methods=['POST'])
def putCar():
    id_token = request.cookies.get("token")
    claims = None
    user_info = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            createCar(
                request.form['name'], request.form['manufacturer'], request.form['year'], request.form['battery'], request.form['wltp'], request.form['cost'], request.form['power'])

        except ValueError as exc:
            error_message = str(exc)

    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
