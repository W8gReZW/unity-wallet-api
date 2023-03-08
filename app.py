from flask import Flask, url_for, redirect, session
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'your-secret-key'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='your-google-client-id',
    consumer_secret='your-google-client-secret',
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/login')
def login():
    callback_url = url_for('authorized', _external=True)
    return google.authorize(callback=callback_url)

@app.route('/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    access_token = resp['access_token']
    # use the access token to make API requests on behalf of the user
    return 'Access granted'
    
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run()
