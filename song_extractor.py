#!/usr/bin/env python3

import requests
import sys
import re
import json
import argparse

def seconds_to_minutes(seconds):
	seconds = int(seconds)
	minutes = seconds / 60
	seconds = seconds % 60
	return "%d:%02d" % (minutes, seconds)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Get BPM from songbpm.com',
		epilog='Made by @UnluckyGermi')

	parser.add_argument('song', help='Song name')
	parser.add_argument('-p', '--pretty', help='Prettify output', action='store_true')
	parser.add_argument('-j', '--json', help='Get information in JSON format', action='store_true')
	parser.add_argument('-x', '--xml', help='Get information in XML format', action='store_true')

	args = parser.parse_args()
	
	

	song_name = args.song
	main_url = "https://songbpm.com"
	post_data = {"query": song_name}
	song_code = requests.post(main_url + "/api/searches", json=post_data).json()["data"]["id"]
	song_data = requests.get(main_url + "/searches/" + song_code).text
	
	filtered_data = re.search(r"<script id=\"__NEXT_DATA__\".*>({.*})</script>", song_data).group(1)
	json_data = json.loads(filtered_data)

	if len(json_data["props"]["pageProps"]["songs"]) == 0:
		print("No results found")
		sys.exit(1)

	json_song = json_data["props"]["pageProps"]["songs"][0]

	song_bpm = json_song["tempo"]
	song_key = json_song["key"]
	song_name = json_song["name"]
	song_artist = json_song["artist"]["name"]
	song_duration = json_song["durationSeconds"]

	if args.json:
		print(json.dumps({
			"name": song_name,
			"artist": song_artist,
			"bpm": song_bpm,
			"key": song_key,
			"duration": seconds_to_minutes(song_duration)
		}))
	elif args.xml:
		print("<song>")
		print("\t<name>" + song_name + "</name>")
		print("\t<artist>" + song_artist + "</artist>")
		print("\t<bpm>" + str(song_bpm) + "</bpm>")
		print("\t<key>" + song_key + "</key>")
		print("\t<duration>" + seconds_to_minutes(song_duration) + "</duration>")
		print("</song>")
	elif args.pretty:
		print("\n\033[4m" + song_artist + " - " + song_name + "\033[0m")
		print(" - Key: " + song_key)
		print(" - Duration: " + seconds_to_minutes(song_duration))
		print(" - BPM: " + str(song_bpm))
	else:
		print("Song: " + song_artist + " - " + song_name + "\n")
		print("Key: " + song_key)
		print("Duration: " + seconds_to_minutes(song_duration))
		print("BPM: " + str(song_bpm))

