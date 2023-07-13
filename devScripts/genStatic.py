#!python
# WARNING! THIS FILE IS NOT CLEANED OR ORGANIZED.
import sys
import xml.etree.ElementTree as ET
import json

use_vanilla_items = True

unlockList = [None] * 637
genItemList = []
modItemUnlockList = [None] * 637
#ignoreList = {327, 328, 293, 105, 126, 214, 609, 313, 349}

extractedPath = sys.argv[1]

items = ET.parse(extractedPath + "resources-dlc3/items.xml")
players = ET.parse(extractedPath + "resources-dlc3/players.xml")
cards = ET.parse(extractedPath + "resources-dlc3/pocketitems.xml")

#itempools = ET.parse(extractedPath + "resources-dlc3/itempools.xml")

def fill_tables():
	collect_enum = json.loads(open("enums/collectibles.json", "r").read())
	players_enum = json.loads(open("enums/players.json", "r").read())
	players_file = create_static_file("../static/players.lua")
	players_file_comma = False
	trinkets_enum = json.loads(open("enums/trinkets.json", "r").read())
	cards_enum = json.loads(open("enums/cards.json", "r").read())
	pills_enum = json.loads(open("enums/pills.json", "r").read())
	for item in items.getroot():
		if item.tag == "passive" or item.tag == "active" or item.tag == "familiar":
			add_unlocks(item, collect_enum, "CollectibleType", 1)
		elif item.tag == "trinket":
			add_unlocks(item, trinkets_enum, "TrinketType", 2)
	for item in players.getroot():
		append_file(players_file, get_entry(item, players_enum, "PlayerType"), players_file_comma)
		players_file_comma = True
	for item in cards.getroot():
		if item.tag == "card" or item.tag == "rune":
			add_unlocks(item, cards_enum, "Card", 3)
		elif item.tag == "pilleffect":
			add_unlocks(item, pills_enum, "PillEffect", 4)
	players_file.write("}")
	players_file.close()

	genItems()

def get_entry_info(entry, enum, enum_name):
	item_id = int(entry.get("id"))
	achievement = 0
	achievement_attrib = entry.get("achievement")
	if achievement_attrib != None:
		achievement = int(achievement_attrib)
	item_id = enum_name + "." + list(enum.keys())[list(enum.values()).index(item_id)]
	return item_id, achievement


def get_entry(entry, enum, enum_name):
	item_id, achievement = get_entry_info(entry, enum, enum_name)
	return("[" + str(item_id) + "]" + '=' + str(achievement))

def create_static_file(path):
	file = open(path, "w")
	file.write("return {")
	return file

def append_file(file, entry, comma):
	if comma:
		file.write("," + entry)
	else:
		file.write(entry)

def add_unlocks(entry, enum, enum_name, entry_type):
	if use_vanilla_items:
		item_id, achievement = get_entry_info(entry, enum, enum_name)
		if achievement != 0: #and not (int(item.get("id")) in ignoreList):
			unlockList[achievement - 1] = entry_type, item_id

def genItems():
	modCollectibles_file = open("../content/items.xml", "w")
	modCollectibles_file.write('<items gfxroot="gfx/items/" version="1">\n')
	for achievement, collectible in enumerate(unlockList):
		if collectible == None:
			genItemList.append(achievement + 1)
	for item_id in genItemList:
		modCollectibles_file.write('	<passive name="KZAchievementCheckerID' + str(item_id) + '" achievement="' + str(item_id) + '" gfx="collectibles_001_thesadonion.png"/>\n')
		modItemUnlockList[item_id - 1] = item_id
	modCollectibles_file.write('</items>')
	modCollectibles_file.close()

	achievements_file = create_static_file("../static/achievements.lua")
	achievements_file_comma = False
	for achievement, entry in enumerate(unlockList):
		unlock_type = None
		unlock_item = None
		if entry == None:
			unlock_type = 0
			unlock_item = '"KZAchievementCheckerID' + str(modItemUnlockList[achievement]) + '"'
		else:
			unlock_type = entry[0]
			unlock_item = entry[1]
		prefix = '['
		if achievements_file_comma:
			prefix = ',['
		achievements_file.write(prefix + str(achievement + 1)  + ']={' + str(unlock_type) + ',' + str(unlock_item) + '}')
		achievements_file_comma = True
	achievements_file.write("}")
	achievements_file.close()


fill_tables()