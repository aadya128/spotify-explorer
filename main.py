# Install Spotipy library (only needed once)
!pip install spotipy --quiet

# Imports
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'https://example.com/callback'  # must match exactly with what you set on Spotify Dev Dashboard

scope = "user-library-read user-read-private user-top-read"

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
)

auth_url = sp_oauth.get_authorize_url()
print("🔗 Please go to this URL and authorize access:\n", auth_url)

redirected_url = input("Paste the full redirected URL here: ")

code = sp_oauth.parse_response_code(redirected_url)
token_info = sp_oauth.get_access_token(code, as_dict=True)
access_token = token_info['access_token']

sp = spotipy.Spotify(auth=access_token)
print("You're authenticated with Spotify!")

track_name = input("Enter a song name: ")
results = sp.search(q=track_name, type='track', limit=1)
track = results['tracks']['items'][0]

print(f"\n🎵 Track: {track['name']}")
print(f"🎤 Artist: {track['artists'][0]['name']}")
print(f"💿 Album: {track['album']['name']}")
print(f"📊 Popularity: {track['popularity']}")
print(f"⏱️ Duration: {round(track['duration_ms']/60000, 2)} min")

track_id = track['id']
features = sp.audio_features([track_id])[0]

df = pd.DataFrame({
    'Danceability': [features['danceability']],
    'Energy': [features['energy']],
    'Valence (Mood)': [features['valence']],
    'Tempo': [features['tempo']],
    'Speechiness': [features['speechiness']],
    'Acousticness': [features['acousticness']],
    'Instrumentalness': [features['instrumentalness']]
})

df.T.rename(columns={0: 'Score'}).style.background_gradient(cmap='YlGnBu')
