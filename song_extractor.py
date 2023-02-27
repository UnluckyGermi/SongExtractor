#!/usr/bin/env python3

import requests
import sys
import re
import json
import argparse

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

	song_key = re.search(r'<div class="flex flex-1 flex-col items-center"><span class="text-xs uppercase">Key</span><span class="text-2xl text-gray-700 sm:text-3xl">(\w(?#/\w♭)?)</span></div>', song_data).group(1)
	song_duration = re.search(r'<div class="flex flex-1 flex-col items-center"><span class="text-xs uppercase">Duration</span><span class="text-2xl text-gray-700 sm:text-3xl">(\d{1,2}:\d{2})</span></div>', song_data).group(1)
	song_bpm = re.search(r'<div class="flex flex-1 flex-col items-center"><span class="text-xs uppercase">BPM</span><span class="text-2xl font-bold text-gray-700 sm:text-3xl sm:font-normal">(\d+)</span></div>', song_data).group(1)

	song_artist = re.search(r"""<p class="text-sm font-light uppercase sm:text-base">([\w ]+)</p>""", song_data).group(1)
	song_name = re.search(r"""<p class="pr-2 text-lg sm:text-2xl sm:font-light">([\w ]+)</p>""", song_data).group(1)

	if args.json:
		print(json.dumps({
			"name": song_name,
			"artist": song_artist,
			"bpm": song_bpm,
			"key": song_key,
			"duration": song_duration
		}))
	elif args.xml:
		print("<song>")
		print("\t<name>" + song_name + "</name>")
		print("\t<artist>" + song_artist + "</artist>")
		print("\t<bpm>" + str(song_bpm) + "</bpm>")
		print("\t<key>" + song_key + "</key>")
		print("\t<duration>" + song_duration + "</duration>")
		print("</song>")
	elif args.pretty:
		print("\n\033[4m" + song_artist + " - " + song_name + "\033[0m")
		print(" - Key: " + song_key)
		print(" - Duration: " + song_duration)
		print(" - BPM: " + str(song_bpm))
	else:
		print("Song: " + song_artist + " - " + song_name + "\n")
		print("Key: " + song_key)
		print("Duration: " + song_duration)
		print("BPM: " + str(song_bpm))

