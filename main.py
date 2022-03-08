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
    id_token = request.cookies.get("token")
    error_message = None
    claims = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            query = datastore_client.query(kind='Vehicules')
            result = query.fetch()
        except ValueError as exc:
            error_message = str(exc)

    return render_template('all_cars.html', user_data=claims, error_message=error_message, cars_list=result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
