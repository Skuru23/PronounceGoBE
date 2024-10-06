from schemas.auth import SignupRequest
from firebase_admin import credentials, auth

def signup(request: SignupRequest):
    try:
        user = auth.create_user(
            email = request.email,
            password = request.password
        )
    except:
        pass