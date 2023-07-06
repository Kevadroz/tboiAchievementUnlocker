#!python
import sys
import xml.etree.ElementTree as ET
import json

extractedPath = sys.argv[1]
docsPath = sys.argv[2]

items = ET.parse(extractedPath + "resources-dlc3/items.xml")
players = ET.parse(extractedPath + "resources-dlc3/players.xml")
cards = ET.parse(extractedPath + "resources-dlc3/pocketitems.xml")

def fill_tables():
	collect_enum = json.loads(open("enums/collectibles.json", "r").read())
	collect_file = create_file("../static/collectibles.lua")
	collect_file_comma = False
	players_enum = json.loads(open("enums/players.json", "r").read())
	players_file = create_file("../static/players.lua")
	players_file_comma = False
	trinkets_enum = json.loads(open("enums/trinkets.json", "r").read())
	trinket_file = create_file("../static/trinkets.lua")
	trinket_file_comma = False
	cards_enum = json.loads(open("enums/cards.json", "r").read())
	cards_file = create_file("../static/cards.lua")
	cards_file_comma = False
	pills_enum = json.loads(open("enums/pills.json", "r").read())
	pills_file = create_file("../static/pills.lua")
	pills_file_comma = False
	for item in items.getroot():
		if item.tag == "passive" or item.tag == "active" or item.tag == "familiar":
			append_file(collect_file, get_entry(item, collect_enum, "CollectibleType"), collect_file_comma)
			collect_file_comma = True
		elif item.tag == "trinket":
			append_file(trinket_file, get_entry(item, trinkets_enum, "TrinketType"), trinket_file_comma)
			trinket_file_comma = True
	for item in players.getroot():
		append_file(players_file, get_entry(item, players_enum, "PlayerType"), players_file_comma)
		players_file_comma = True
	for item in cards.getroot():
		if item.tag == "card" or item.tag == "rune":
			append_file(cards_file, get_entry(item, cards_enum, "Card"), cards_file_comma)
			cards_file_comma = True
		elif item.tag == "pilleffect":
			append_file(pills_file, get_entry(item, pills_enum, "PillEffect"), pills_file_comma)
			pills_file_comma = True
	collect_file.write("}")
	trinket_file.write("}")
	players_file.write("}")
	cards_file.write("}")
	pills_file.write("}")
	collect_file.close()
	trinket_file.close()
	players_file.close()
	cards_file.close()
	pills_file.close()

def get_entry(entry, enum, enum_name):
	item_id = int(entry.get("id"))
	achievement = 0
	achievement_attrib = entry.get("achievement")
	if achievement_attrib != None:
		achievement = int(achievement_attrib)
	item_id = enum_name + "." + list(enum.keys())[list(enum.values()).index(item_id)]
	return("[" + str(item_id) + "]" + '=' + str(achievement))

def create_file(path):
	file = open(path, "w")
	file.write("return {")
	return file

def append_file(file, entry, comma):
	if comma:
		file.write("," + entry)
	else:
		file.write(entry)

fill_tables()