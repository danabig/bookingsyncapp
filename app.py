import json
import pdb
import os
import requests
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_from_directory
from werkzeug.utils import secure_filename

from bookingsynclord.tools.CredentialManager import CredentialManager
from utils import get_rental_by_name, ensure_rental_entity_with_nightly_rates_managed_externally, \
    updateNightlyRates, load_csv_data

app = Flask(__name__)
app.secret_key = 'super secret key'
APP_BASE_PATH = '/Users/danabigadol/bookingsync-tapioca'
UPLOAD_FOLDER = APP_BASE_PATH + '/static/uploads'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

from bookingsynclord.BookingSyncAPI import BookingSyncAPI
from bookingsynclord.constants import CLIENT_ID, ACCESS_TOKEN, CLIENT_SECRET, REFRESH_TOKEN, TEST_RENTAL_NAME, \
    TEST_RENTAL_NAMES, REQUEST_TOKEN_URL, REDIRECT_URI

ALLOWED_EXTENSIONS = ['txt', 'csv']

booking_sync_api = None#BookingSyncAPI(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN)
result_data = {} # need db in order to keep it, maybe use local storage
bookings = []
rentals = []


class ReusableForm(Form):
    value = TextField('Value:', validators=[validators.required()])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def updateLocalData():
    res = booking_sync_api.rentals_store.list_json()
    result_data['rentals'] = res['rentals']
    rentals = result_data['rentals']
    for rental_name in TEST_RENTAL_NAMES:
        test_rental = get_rental_by_name(rentals, rental_name)
        print test_rental['name']
        ensure_rental_entity_with_nightly_rates_managed_externally(booking_sync_api, test_rental, True)
    print 'data fetch completed successfully'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route("/", methods=['GET', 'POST'])
def submit():
    print 'submit'
    form = ReusableForm(request.form)

    if len(form.errors) > 0:
        print form.errors

    if request.method == 'POST':
        value = request.form['value']
        print value

        if form.validate():
            # Save the comment here.
            flash('Searching ' + value)
        else:
            flash('All the form fields are required. ')

        result_data['rental'] = booking_sync_api.rentals_store.list_json(filters={ 'fields': value })
        print json.dumps(result_data)#, indent=4, sort_keys=True)
    else:
        if booking_sync_api is None:
            return redirect(url_for('authorize'))

        if len(rentals) == 0 or len(bookings) == 0:
            updateLocalData()

    return render_template('search.html', form=form)


@app.route("/file_upload/", methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            loaded_data = load_csv_data(result_data['rentals'], file)
            for single_data in loaded_data:
                updateNightlyRates(booking_sync_api, single_data)
        return redirect(request.url)
            # filename = secure_filename(file.filename)
            # result_data['upload_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # file.save(result_data['upload_file_path'])
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    if request.method == 'GET':
        return render_template('file_upload.html')


@app.route("/rental_by_id/<string:id>/")
def rental_by_id(id):
    result_data['booking'] = booking_sync_api.rentals_store.get(int(id))
    print 'bookings loaded'
    return render_template('test.html')


@app.route("/ping_booking/")
def ping():
    result_data['rental'] = booking_sync_api.rentals_store.list_json()
    print 'rentals loaded'
    return render_template('test.html')


@app.route("/hello/<string:name>/")
def hello(name):
    return render_template(
        'test.html', name=name)


@app.route("/authorize/", methods=['GET', 'POST'])
def authorize():
    if request.method == 'POST':
        form = ReusableForm(request.form)
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        client_code = request.form['client_code']
        print client_id, client_secret, client_code
        print '------------------------------------'
        access_token, refresh_token = CredentialManager.generate_first_token(client_id,client_secret,client_code)
        print access_token,refresh_token
        booking_sync_api = BookingSyncAPI(client_id, client_secret, access_token, refresh_token)
        updateLocalData()
        return redirect(url_for('file_upload'))
    else:
        return render_template('authorization.html', authorization_url=CredentialManager.generate_authorize_url('{client_id}'))


if __name__ == "__main__":
    # sess.init_app(app)
    app.run(host='0.0.0.0', port=8080)