import os
import requests
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException
from urllib.parse import urlencode

auth_router = APIRouter()

#Load .env file into os.environ
def load_env_file(env_file=".env"):
    if not os.path.exists(env_file):
        print(f"{env_file} not found.")
        return

    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            os.environ[key] = value
            # print(key, value)

# Load .env file at startup
load_env_file()

LINE_AUTH_URL = "https://access.line.me/oauth2/v2.1/authorize"
CLIENT_ID = os.getenv("LINE_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "profile openid"
STATE = "1234567890"
print(f"CLIENT_ID: {CLIENT_ID}")
print(f"REDIRECT_URI: {REDIRECT_URI}")

@auth_router.get("/login")
async def login():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": STATE,
    }
    login_url = f"{LINE_AUTH_URL}?{urlencode(params)}"
    print(login_url)
    return {"url": login_url}


LINE_TOKEN_URL = "https://api.line.me/oauth2/v2.1/token"
# In-memory storage (Can be replaced with Redis or DB later)
ACCESS_TOKEN_STORAGE = {}

@auth_router.get("/callback")
async def callback(code: str, state: str):
    if state != STATE:
        raise HTTPException(status_code=400, detail="Invalid state")

    # Request Access Token
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(LINE_TOKEN_URL, data=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get access token")

    token_data = response.json()
    
    # Store Access Token (in the storage for now)
    ACCESS_TOKEN_STORAGE["access_token"] = token_data["access_token"]
    
    # Redirect the client to the frontend dashboard
    frontend_dashboard_url = "http://localhost:3000/dashboard"  # Frontend URL
    return RedirectResponse(url=frontend_dashboard_url)


LINE_PROFILE_URL = "https://api.line.me/v2/profile"

@auth_router.get("/profile")
async def profile():
    # Load the Access Token stored in the Backend
    access_token = ACCESS_TOKEN_STORAGE.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Request LINE API to get user profile
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_response = requests.get("https://api.line.me/v2/profile", headers=headers)

    if profile_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user profile")

    print(profile_response.json())
    return profile_response.json()
