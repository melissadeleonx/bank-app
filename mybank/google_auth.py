# google_auth.py
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request


# Path to client_secret.json file
# The secret file is in the variable environment(.env or any hosting/docker environment), deleted/gitignore upon submission of this project
CLIENT_SECRETS_FILE = settings.GOOGLE_CREDENTIALS_FILE

# Set up Oauth2 API and tester users using Google Cloud Console
# These scopes are responsible for logging in and signing up using Google
# For sending email confirmation/verification, use Gmail smtp, not Gmail API!  
SCOPES = [
    'openid', 
    'https://www.googleapis.com/auth/userinfo.email', 
    'https://www.googleapis.com/auth/userinfo.profile'
]

# redirect uri should be authorized on the Google Cloud console
# Check Google Oauth2 Documentation source for more instructions
def get_authorization_url():
    """Generate the authorization URL for OAuth 2.0."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/oauth2callback/' 
    )
    auth_url, _ = flow.authorization_url(
        access_type='offline', 
        include_granted_scopes='true'
    )
    return auth_url


def get_credentials_from_code(code):
    """
    Exchange the authorization code for OAuth2 credentials.
    """
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/oauth2callback/' 
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    return creds

def get_user_info(creds):
    """
    Use the OAuth2 credentials to fetch user information.
    """
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("Invalid credentials")

    # Use the credentials to fetch user info from Google's API
    from googleapiclient.discovery import build
    service = build('oauth2', 'v2', credentials=creds)
    user_info = service.userinfo().get().execute()
    return user_info