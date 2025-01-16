# Jam Track Data
This repository has code that generates and displays Jam Track data, primarily on how many songs there are per artist in FNFestival and the number of songs per genre.

## New:
There are no new additions in the commit.

## Changes:
The program now writes to files using UTF-8 encoding so it write the special characters in Spanish & Hatsune Miku songs.

As the pie chart was getting crowded again, it now only shows artists more than 3 songs.

## How does it work?
The list of all available jam tracks can be found on the public Fortnite Content API at [this link](https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks).

I update the files every time Jam Tracks are added to the API.

## Other Information
I am considering either making a web app or an executable that can pull up all this data and display it more nicely. If there are any other suggestions, please reach out to me.
