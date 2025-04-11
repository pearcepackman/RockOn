import sounddevice as sd
import soundfile as sf
import time
import os
import librosa 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "6f9aef3c3b57437a96b22a65bd487cd6"
client_secret = "0de78b48925b4b1b8d50c9824d42d6a4"

#ISSUE WITH SPOTIFY
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=
    client_secret=
))

# Recording parameters
duration = 15  # seconds
samplerate = 44100
folder = "recordings"

# Get where we're at currently
script_dir = os.path.dirname(os.path.abspath(__file__))

# Make path to folder
folder_path = os.path.join(script_dir, folder)

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Generate a unique filename with timestamp
timestamp = time.strftime("%Y%m%d_%H%M%S")  # Format: 20250411_153000
#filename = os.path.join(folder_path, f"recording_{timestamp}.wav")

# User input to start recording
r = input("Record or Analyze, Press enter to record new: ")
if r == "":
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)
    print("Recording...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    fileext = input("What would you like to call this file?: ")
    filename = os.path.join(folder_path, f"{fileext}.wav")
    sf.write(filename, recording, samplerate)
    print(f"Recording saved as: {filename}")
else:
    print("Silly goose")
    files = [f for f in os.listdir(folder_path) if f.endswith(".wav")]
    print("Recordings: ")
    filenum = 1
    for file in files:
        print(f"{filenum}: {file}")
        filenum += 1
    
    try:
        choice = int(input("Enter file number to analyze: ")) - 1
        selected_file = os.path.join(folder_path, files[choice])
        y, sr = librosa.load(selected_file, sr=None)
        rectempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        print(f"Your Tempo: {rectempo}")
    except:
        print("Invalid input")
    
    songsearch = sp.search(q="Penthouse Pauper", limit = 1, type = 'track')
    track_id = songsearch['tracks']['items'][0]['id']
    songfeatures = sp.audio_features(track_id)[0]
    
    print(f"Song Tempo: {songfeatures['tempo']}")

    



