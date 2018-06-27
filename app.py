import json
import pdb
import os
import requests
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.contrib.cache import SimpleCache
# from flask.ext.cache import Cache

from bookingsynclord.tools.CredentialManager import CredentialManager
from utils import get_rental_by_name, ensure_rental_entity_with_nightly_rates_managed_externally, \
    updateNightlyRates, load_csv_data, updateLocalData

app = Flask(__name__)
global cache
cache = SimpleCache()
# cache = Cache(app,config={'CACHE_TYPE': 'simple'})
app.secret_key = 'super     secret key'
APP_BASE_PATH = '/Users/danabigadol/bookingsync-tapioca'
UPLOAD_FOLDER = APP_BASE_PATH + '/static/uploads'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

from bookingsynclord.BookingSyncAPI import BookingSyncAPI
from bookingsynclord.constants import CLIENT_ID, ACCESS_TOKEN, CLIENT_SECRET, REFRESH_TOKEN, TEST_RENTAL_NAME, \
    TEST_RENTAL_NAMES, REQUEST_TOKEN_URL, REDIRECT_URI, RENTALS_CACHE, CACHE_TIMEOUT, API_CACHE

ALLOWED_EXTENSIONS = ['txt', 'csv']

# global_booking_sync_api = None #BookingSyncAPI(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN)
# result_data = {} # need db in order to keep it, maybe use local storage
# bookings = []
# rentals = []


class ReusableForm(Form):
    value = TextField('Value:', validators=[validators.required()])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/authorize/", methods=['GET', 'POST'])
def authorize():
    global cache
    booking_sync_api = cache.get(API_CACHE)

    if request.method == 'POST':
        form = ReusableForm(request.form)
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        client_code = request.form['client_code']
        print client_id, client_secret, client_code
        print '------------------------------------'
        access_token, refresh_token = CredentialManager.generate_first_token(client_id,client_secret,client_code)
        print access_token,refresh_token
        cache.set('client_id', client_id)
        cache.set('client_secret', client_secret)
        cache.set('access_token', access_token)
        cache.set('refresh_token', refresh_token)

        if booking_sync_api is None:
            booking_sync_api = BookingSyncAPI(client_id, client_secret, access_token, refresh_token)
            print booking_sync_api
            cache.set(API_CACHE, booking_sync_api, timeout=CACHE_TIMEOUT)
        else:
            print 'api already created'
            booking_sync_api.credential_manager.client_id = client_id
            booking_sync_api.credential_manager.client_secret = client_secret
            booking_sync_api.credential_manager.access_token = access_token
            booking_sync_api.credential_manager.refresh_token = refresh_token
            cache.set(API_CACHE, booking_sync_api, timeout=CACHE_TIMEOUT)
        updateLocalData(booking_sync_api, cache)
        return redirect(url_for('file_upload'))
    else:
        client_id = cache.get('client_id')
        client_secret = cache.get('client_secret')
        access_token = cache.get('access_token')
        refresh_token = cache.get('refresh_token')

        if client_id and client_secret and access_token and refresh_token:
            print 'tokens exist'
            if booking_sync_api is None:
                booking_sync_api = BookingSyncAPI(client_id, client_secret, access_token, refresh_token)
                print booking_sync_api
                cache.set(API_CACHE, booking_sync_api, timeout=CACHE_TIMEOUT)
            else:
                print 'updating api tokens'
                booking_sync_api.credential_manager.client_id = client_id
                booking_sync_api.credential_manager.client_secret = client_secret
                booking_sync_api.credential_manager.access_token = access_token
                booking_sync_api.credential_manager.refresh_token = refresh_token
            try:
                access_token, refresh_token = booking_sync_api.credential_manager.roll_token()
                cache.set('access_token', access_token)
                cache.set('refresh_token', refresh_token)
                cache.set(API_CACHE, booking_sync_api, timeout=CACHE_TIMEOUT)
                updateLocalData(booking_sync_api, cache)
                return redirect(url_for('file_upload'))
            except LookupError:
                return render_template('authorization.html',
                                       authorization_url=CredentialManager.generate_authorize_url('{client_id}'))


        return render_template('authorization.html', authorization_url=CredentialManager.generate_authorize_url('{client_id}'))



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route("/", methods=['GET', 'POST'])
def submit():
    global cache
    print 'submit'
    form = ReusableForm(request.form)

    if len(form.errors) > 0:
        print form.errors
    booking_sync_api = cache.get(API_CACHE)
    if booking_sync_api is None:
        return redirect(url_for('authorize'))

    if request.method == 'POST':
        value = request.form['value']
        print value

        if form.validate():
            # Save the comment here.
            flash('Searching ' + value)
        else:
            flash('All the form fields are required. ')

        rentals = cache.get(RENTALS_CACHE)
        if rentals is None:
            rentals = booking_sync_api.rentals_store.list_json(filters={ 'fields': value })
            cache.set(RENTALS_CACHE, rentals, timeout=CACHE_TIMEOUT)
        print json.dumps(rentals)#, indent=4, sort_keys=True)
    else:
        updateLocalData(booking_sync_api, cache)

    return render_template('search.html', form=form)


@app.route("/enable_rentals/", methods=['GET', 'POST'])
def enable_rentals():
    global cache
    booking_sync_api = cache.get(API_CACHE)
    rentals = cache.get(RENTALS_CACHE)
    if request.method == 'POST':
        form = ReusableForm(request.form)
        rentals_to_enable = request.form['enable_rentals']
        rentals_to_disable = request.form['disable_rentals']
        enables = rentals_to_enable.split(',')
        disables = rentals_to_disable.split(',')
        for rental_name in enables:
            rental = get_rental_by_name(rentals, rental_name)
            assert rental is not None
            ensure_rental_entity_with_nightly_rates_managed_externally(booking_sync_api, rental, allow_manage=True)
            print 'enable rental %s' % rental_name
        for rental_name in disables:
            rental = get_rental_by_name(rentals, rental_name)
            assert rental is not None
            ensure_rental_entity_with_nightly_rates_managed_externally(booking_sync_api, rental, allow_manage=False)
            print 'disable rental %s' % rental_name

        return redirect(url_for('file_upload'))
    else:
        return render_template('rentals_enable.html')


@app.route("/file_upload/", methods=['GET', 'POST'])
def file_upload():
    global cache
    booking_sync_api = cache.get(API_CACHE)
    rentals = cache.get(RENTALS_CACHE)
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
            loaded_data = load_csv_data(rentals, file)
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


# @app.route("/rental_by_id/<string:id>/")
# def rental_by_id(id):
#     result_data['booking'] = booking_sync_api.rentals_store.get(int(id))
#     print 'bookings loaded'
#     return render_template('test.html')


# @app.route("/ping_booking/")
# def ping():
#     result_data['rental'] = booking_sync_api.rentals_store.list_json()
#     print 'rentals loaded'
#     return render_template('test.html')


# @app.route("/hello/<string:name>/")
# def hello(name):
#     return render_template(
#         'test.html', name=name)


if __name__ == "__main__":
    # sess.init_app(app)
    app.run(host='0.0.0.0', port=8080)