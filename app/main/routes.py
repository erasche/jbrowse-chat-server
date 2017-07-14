import json
import os

from . import main

from flask import session, redirect, url_for, request
from flask_oauth import OAuth



GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']

oauth = OAuth()
google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'
    },
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={
        'grant_type': 'authorization_code'
    },
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET
)


@main.route('/login')
def login():
    session['referrer'] = request.referrer
    callback = url_for('main.authorized', _external=True)
    return google.authorize(callback=callback)


@main.route('/oauth2/google')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('main.index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


@main.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect('/login')

    account = session.get('account', None)
    if not account:
        access_token = access_token[0]
        from urllib2 import Request, urlopen, URLError

        headers = {'Authorization': 'OAuth '+access_token}
        req = Request('https://www.googleapis.com/oauth2/v1/userinfo', None, headers)
        try:
            res = urlopen(req)
            session['account'] = json.loads(res.read())
        except URLError as e:
            if e.code == 401:
                # Unauthorized - bad token
                session.pop('access_token', None)
                return redirect(url_for('main.login'))

    if 'referrer' in session:
        return redirect(session['referrer'])

    return '<pre>' + json.dumps(session['account'], indent=2) + '</pre>'
