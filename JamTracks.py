# Author: Darian Hughes
# Last Modified: 5/12/2024
# JamTracks.py

import requests
import matplotlib.pyplot as plt
import re
from datetime import datetime, timedelta

def is_within_five_days(input_date):
    # Parse the input date string in ISO 8601 format
    input_date = datetime.strptime(input_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    today = datetime.now()
    
    # Calculate the difference in days
    difference = abs((today - input_date).days)
    
    # Check if the difference is within 5 days
    return difference <= 5

response = requests.get("https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks")

if response.status_code != 200:
    print("Failed to fetch data.")
    exit()

data = response.json()

list_of_songs = []
date_of_song = {}
number_of_songs_per_artist = {}
songs_per_artist = {}
number_of_songs = 0
for i, entry in enumerate(data):
    if i >= 6 and entry != "_suggestedPrefetch":
        number_of_songs += 1
        artists = re.split(' w/ | & | ft. | + |, ', data[entry]['track']['an'])
        songTitle = data[entry]['track']['tt']
        songDate = data[entry]['_activeDate']
        date_of_song.update({songTitle: songDate})
        list_of_songs.append(songTitle)
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

sorted_list_of_songs = sorted(list_of_songs)

# Write the sorted list of songs to the list_of_songs.txt file
with open('list_of_songs.txt', 'w', encoding="utf-8") as f:
    for song in sorted_list_of_songs:
        f.write(f"{song}\n")

# Write new songs to a new_songs.txt file
with open('new_songs.txt', 'w', encoding="utf-8") as f:
    print('New songs from the past 5 days:')
    for song, modified_date in date_of_song.items():
        if is_within_five_days(modified_date):
            print(song)
            f.write(f"{song}\n")

print("Songs have been written to list_of_songs.txt and new_songs.txt.")
        
# Grouping artists with 2 or less songs
single_song_artists = {}
number_of_single_song_artists = 0
for artist, count in number_of_songs_per_artist.items():
    if count <= 2:
        single_song_artists[artist] = count
        number_of_single_song_artists += 1

# Getting the difficulties for songs and adding them to a .txt file.
print("Saving song difficulty data")

song_difficulties = {}
for i, entry in enumerate(data):
    if i > 6 and entry != "_suggestedPrefetch":
        songTitle = data[entry]['track']['tt']
        if 'vl' in data[entry]['track']['in'] and data[entry]['track']['in']['vl']:
            vocals = data[entry]['track']['in']['vl']
        else:
            vocals = "No data"

        if 'gr' in data[entry]['track']['in'] and data[entry]['track']['in']['gr']:
            guitar = data[entry]['track']['in']['gr']
        else:
            guitar = "No data"

        if 'ba' in data[entry]['track']['in'] and data[entry]['track']['in']['ba']:
            bass = data[entry]['track']['in']['ba']
        else:
            bass = "No data"

        if 'ds' in data[entry]['track']['in'] and data[entry]['track']['in']['ds']:
            drums = data[entry]['track']['in']['ds']
        else:
            drums = "No data"

        song_difficulties[songTitle] = [vocals, guitar, bass, drums]

hardestVl = []
hardestGr = []
hardestBa = []
hardestDs = []
for difficulties in song_difficulties:
    value = song_difficulties[difficulties]
    if value[0] != "No data":
        if value[0] >= 5:
            hardestVl.append(f"{difficulties} ({value[0]})")
    if value[1] != "No data":
        if value[1] >= 5:
            hardestGr.append(f"{difficulties} ({value[1]})")
    if value[2] != "No data":
        if value[2] >= 5:
            hardestBa.append(f"{difficulties} ({value[2]})")
    if value[3] != "No data":
        if value[3] >= 5:
            hardestDs.append(f"{difficulties} ({value[3]})")

with open('hardest_songs_per_instrument.txt', 'w', encoding="utf-8") as f:
    f.write("Vocals\n")
    for song in hardestVl:
        f.write(f"\t{song}\n")
    f.write("Guitar\n")
    for song in hardestGr:
        f.write(f"\t{song}\n")
    f.write("Bass\n")
    for song in hardestBa:
        f.write(f"\t{song}\n")
    f.write("Drums\n")
    for song in hardestDs:
        f.write(f"\t{song}\n")

print("Data saved to hardest_songs_per_instrument.txt")

# Plotting - Pie chart for artists with more than one song

# Set subplot parameters
plt.rcParams['figure.subplot.bottom'] = 0
plt.rcParams['figure.subplot.right'] = 0.9
plt.rcParams['figure.subplot.top'] = 0.974

plt.figure(figsize=(12, 6))
songs_per_artist_with_count = ["{} ({} songs)".format(artist, count) for artist, count in number_of_songs_per_artist.items() if count > 3]
plt.pie([count for artist, count in number_of_songs_per_artist.items() if count > 3], 
        labels=songs_per_artist_with_count, 
        autopct='%1.1f%%', startangle=200)
plt.title('Artists by Song Count (More than Three Songs)')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

sorted_songs_per_artist = {artist: sorted(songs, reverse=True) for artist, songs in songs_per_artist.items()}

print("Saving artist data...")
with open('songs_per_artist.txt', 'w', encoding="utf-8") as f:
    for artist, song_count in sorted(number_of_songs_per_artist.items(), key=lambda x: x[1], reverse=True):
        song_percent = round(((song_count/number_of_songs) * 100), 2)
        f.write(f"{artist}: {song_count} song(s) ({song_percent}%)\n")
        for song_name in sorted_songs_per_artist[artist]:
            f.write(f"\t{song_name}\n")
    
print("Data saved to songs_per_artist.txt")
print(f"Number of Single Song Artits: {number_of_single_song_artists}/{len(number_of_songs_per_artist)} artists")

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

print(f"Number of Songs With Genres: {number_of_songs_with_ge}/{number_of_songs} songs")

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