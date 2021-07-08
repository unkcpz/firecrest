from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
import pkce
import json

app = Flask(__name__)
app.secret_key = 'secret string used by flask to keep the session 4eddfu8df'.encode('utf8')

# Keycloak configurationd for OIDC
CONF_URL = 'http://localhost:8080/auth/realms/kcrealm/.well-known/openid-configuration'


oauth = OAuth(app)
oauth.register(
    name='kc',
    server_metadata_url=CONF_URL,
    client_id='firecrest-pkce',
    client_secret='f3d443ab-b2c6-4250-af14-fa2ee32152f5',
    client_kwargs={
        'scope': 'openid email profile firecrest'
    }
)

# PKCE: code verifier and challenge used in pkce workflow
code_verifier = pkce.generate_code_verifier(length=128)
code_challenge = pkce.get_code_challenge(code_verifier)

@app.route('/')
def homepage():
    if 'user' in session:
        user = session.get('user')
        return render_template('home.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    # PKCE: we ask for authorization passing the challenge and specifying the method
    return oauth.kc.authorize_redirect(redirect_uri, code_challenge_method='S256', code_challenge=code_challenge)


@app.route('/callback')
def callback():
    # PKCE: getting the token and validating against the verifier
    token = oauth.kc.authorize_access_token(code_verifier=code_verifier)
    session['user'] = oauth.kc.parse_id_token(token)
    return redirect('/')


# Note1: Authlib's flask_client does not have token revocation yet and a client with such feature should use OAuth2Session
@app.route('/logout')
def logout():
    session.pop('user', None)
    resp = app.make_response(render_template('home.html', user=None))
    return resp
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, ssl_context='adhoc')
