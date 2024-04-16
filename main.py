from dotenv import find_dotenv, load_dotenv
from billboardInfo import BillboardInfo
import spotipy

import os

dotenv_path = find_dotenv()  # Finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found above

CLIENT_ID_SPOTIFY = os.getenv("clientID")

CLIENT_SECRET_SPOTIFY = os.getenv("clientSecret")
URL_REDIRECT = "https://example.com"

spotify_auth = spotipy.oauth2.SpotifyOAuth(
    redirect_uri=URL_REDIRECT,
    scope="playlist-modify-public playlist-modify-private",
    client_id=CLIENT_ID_SPOTIFY,
    client_secret=CLIENT_SECRET_SPOTIFY,
    show_dialog=True,
    cache_path="token.txt"
)
access_token = spotify_auth.get_access_token()

client = spotipy.Spotify(auth_manager=spotify_auth)  # Creates client object

bi = BillboardInfo()
song_list = bi.getTitles()
year = bi.date.split("-")[0]
song_uris = []
index = 0
for song in song_list:
    output = client.search(q=f"track: {song} year: {year}")  # Searches for the song
    try:
        uri = output["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(index)
        index += 1
    except IndexError:
        # ASSERT: Song isn't available in spotify
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = client.user_playlist_create(user=client.current_user()["id"],
                                       name=bi.date,
                                       public=True,
                                       collaborative=False,
                                       description=f'A playlist of billboard top 100 songs for {bi.date}')

playlist_id = playlist["id"]  # Gets the ID of the playlist that was just created
client.playlist_add_items(playlist_id=playlist_id, items=song_uris, position=None)  # Adds the URIs of the songs in
# the billboard top 100 to the playlist
