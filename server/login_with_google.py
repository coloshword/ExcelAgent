# login_with_google.py: module to login with google 
import google.oauth2.credentials 
import google_auth_oauthlib.flow 

client_secret_path = "../google_auth.json"

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    client_secret_path,
    scopes=[
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid'
    ]
)


flow.redirect_uri = 'https://www.wikipedia.org/'

# generate a URL
authorization_url, state = flow.authorization_url(
    access_type = 'offline',
    include_granted_scopes='true',
    prompt='consent'
)

print(authorization_url)
print(state)