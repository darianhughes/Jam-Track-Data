# Author: Darian Hughes
# Last Modified: 5/12/2024
# JamTracks.py

import requests
import matplotlib.pyplot as plt
import re

response = requests.get("https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks")

if response.status_code != 200:
    print("Failed to fetch data.")
    exit()

data = response.json()

number_of_songs_per_artist = {}
songs_per_artist = {}
number_of_songs = 0
for i, entry in enumerate(data):
    if i >= 6 and entry != "_suggestedPrefetch":
        number_of_songs += 1
        artists = re.split(' w/ | & | ft. | + |, ', data[entry]['track']['an'])
        songTitle = data[entry]['track']['tt']
        for artist in artists:
            if '+' in artist:
                artists = artist.split("+")
        for unformated_artist in artists:
            artist = unformated_artist.strip()
            if artist in number_of_songs_per_artist.keys() and len(number_of_songs_per_artist) > 0:
                numSongs = number_of_songs_per_artist[artist]
                number_of_songs_per_artist.update({artist: numSongs + 1})
            else:
                if artist != "":
                    number_of_songs_per_artist.update({artist: 1})

            if artist in songs_per_artist.keys() and len(songs_per_artist) > 0:
                songs_per_artist[artist].append(songTitle)
            else:
                songList = [songTitle]
                songs_per_artist.update({artist: songList})
        
# Grouping artists with only one song
single_song_artists = {}
number_of_single_song_artists = 0
for artist, count in number_of_songs_per_artist.items():
    if count == 1:
        single_song_artists[artist] = count
        number_of_single_song_artists += 1

# Save to TXT file
with open('songs_per_artist.txt', 'w') as f:
    for artist, song_count in number_of_songs_per_artist.items():
        f.write(f"{artist}: {song_count} songs\n")
        for songName in songs_per_artist[artist]:
            f.write(f"\t{songName}\n")
    
print("Data saved to songs_per_artist.txt")
print(f"Number of Single Song Artits: {number_of_single_song_artists}/{len(number_of_songs_per_artist)} artists")

# Plotting - Pie chart for artists with more than one song

# Set subplot parameters
plt.rcParams['figure.subplot.bottom'] = 0
plt.rcParams['figure.subplot.right'] = 0.9
plt.rcParams['figure.subplot.top'] = 0.974

plt.figure(figsize=(12, 6))
songs_per_artist_with_count = ["{} ({} songs)".format(artist, count) for artist, count in number_of_songs_per_artist.items() if count > 1]
plt.pie([count for artist, count in number_of_songs_per_artist.items() if count > 1], 
        labels=songs_per_artist_with_count, 
        autopct='%1.1f%%', startangle=200)
plt.title('Artists by Song Count (More than One Song)')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

# Plotting - Pie chart for song genres

# Create a dictionary to store genres and their counts
songs_ge = {}
number_of_songs_with_ge = 0
for i, entry in enumerate(data):
    if i >= 6 and entry != "_suggestedPrefetch":
        song_title = data[entry]['track']['tt']
        if 'ge' in data[entry]['track'] and data[entry]['track']['ge']:
            number_of_songs_with_ge += 1
            genre = data[entry]['track']['ge']
            songs_ge[song_title] = genre

print(f"Number of Song With Genres: {number_of_songs_with_ge}/{number_of_songs} songs")

# Count the occurrence of each genre
genre_counts = {}
for genre in songs_ge.values():
    for value in genre:
        if value in genre_counts:
            genre_counts[value] += 1
        else:
            genre_counts[value] = 1

# Plotting the pie chart
plt.figure(figsize=(8, 8))
plt.pie(genre_counts.values(), labels=genre_counts.keys(), autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Genres')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Show plot
plt.show()