import os
from dotenv import load_dotenv
import requests

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
STORAGE_BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME')

REDIRECT_URI = 'http://localhost/exchange_token'

auth_url = (
    f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&response_type=code&scope=activity:read_all"
)

# Step 1: Direct user to authorize the app
print(f"Authenticate URL: {auth_url}")
AUTH_CODE = input("Enter the authorization code: ")

# Step 2: Exchange authorization code for access token
token_url = "https://www.strava.com/oauth/token"
token_payload = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'code': AUTH_CODE,
    'grant_type': 'authorization_code'
}
response = requests.post(token_url, data=token_payload)
tokens = response.json()

if 'access_token' not in tokens:
    print("Failed to retrieve access token.", tokens)
    exit()

access_token = tokens['access_token']
print("Access Token Obtained Successfully!")

# Step 3: Fetch Activities
activities_url = "https://www.strava.com/api/v3/athlete/activities"
headers = {'Authorization': f'Bearer {access_token}'}
params = {'per_page': 10, 'page': 1}
response = requests.get(activities_url, headers=headers, params=params)

if response.status_code == 200:
    activities = response.json()
    activity_1_id = activities[0]['id']
    activity_url = f"https://www.strava.com/api/v3/activities/{activity_1_id}"
    response = requests.get(activity_url, headers=headers,params=params)
    activity = response.json()
    print("Activity fetched successfully.", activity)
    
else:
    print("Failed to fetch activities.", response.json())

