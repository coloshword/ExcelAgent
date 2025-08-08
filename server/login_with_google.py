# login_with_google.py: module to login with google 
import google.oauth2.credentials 
import google_auth_oauthlib.flow 


def get_authorization_url() -> tuple[str, str]:
    '''
    Wrapper for flow.authorization_url to get the authorization url for login with google 
        Returns:
            (authorization_url, state): the authorization url and state as a tuple
    '''
    client_secret_path = "google_auth.json"
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret_path,
        scopes=[
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'openid'
        ]
    )
    flow.redirect_uri = 'http://127.0.0.1:5500/client/restrictedPage.html'
    # generate a URL
    return flow.authorization_url(
        access_type = 'offline',
        include_granted_scopes='true',
        prompt='consent'
    )