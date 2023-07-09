#!python
import sys
import xml.etree.ElementTree as ET
import json

use_vanilla_items = True

unlockList = [None] * 637
genItemList = []
modItemUnlockList = [None] * 637
ignoreList = {327, 328, 293, 105, 126, 214, 609, 313, 349}

extractedPath = sys.argv[1]

items = ET.parse(extractedPath + "resources-dlc3/items.xml")
players = ET.parse(extractedPath + "resources-dlc3/players.xml")
cards = ET.parse(extractedPath + "resources-dlc3/pocketitems.xml")

itempools = ET.parse(extractedPath + "resources-dlc3/itempools.xml")

def fill_tables():
	collect_enum = json.loads(open("enums/collectibles.json", "r").read())
	collect_file = create_static_file("../static/collectibles.lua")
	collect_file_comma = False
	players_enum = json.loads(open("enums/players.json", "r").read())
	players_file = create_static_file("../static/players.lua")
	players_file_comma = False
	trinkets_enum = json.loads(open("enums/trinkets.json", "r").read())
	trinket_file = create_static_file("../static/trinkets.lua")
	trinket_file_comma = False
	cards_enum = json.loads(open("enums/cards.json", "r").read())
	cards_file = create_static_file("../static/cards.lua")
	cards_file_comma = False
	pills_enum = json.loads(open("enums/pills.json", "r").read())
	pills_file = create_static_file("../static/pills.lua")
	pills_file_comma = False
	for item in items.getroot():
		if item.tag == "passive" or item.tag == "active" or item.tag == "familiar":
			append_file(collect_file, get_entry(item, collect_enum, "CollectibleType"), collect_file_comma)
			collect_file_comma = True
			add_unlocks(item, collect_enum)
		elif item.tag == "trinket":
			append_file(trinket_file, get_entry(item, trinkets_enum, "TrinketType"), trinket_file_comma)
			trinket_file_comma = True
	for item in players.getroot():
		append_file(players_file, get_entry(item, players_enum, "PlayerType"), players_file_comma)
		players_file_comma = True
		add_to_ignore(item)
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

	genItems()
	genPools()

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

def add_to_ignore(player):
	items = player.get("items")
	pocket = player.get("pocketActive")
	if items != None:
		items = map(int, items.split(','))
		for item in items:
			ignoreList.add(item)
	if pocket != None:
		pocket = int(pocket)
		ignoreList.add(pocket)

def add_unlocks(item, enum):
	if use_vanilla_items:
		item_id, achievement = get_entry_info(item, enum, "CollectibleType")
		if achievement != 0 and not (int(item.get("id")) in ignoreList):
			unlockList[achievement - 1] = item_id

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
		unlock_item = entry
		if entry == None:
			unlock_item = '"KZAchievementCheckerID' + str(modItemUnlockList[achievement]) + '"'
		prefix = '['
		if achievements_file_comma:
			prefix = ',['
		achievements_file.write(prefix + str(unlock_item) + ']=' + str(achievement + 1))
		achievements_file_comma = True
	achievements_file.write("}")
	achievements_file.close()

def genPools():
	total_length = 0
	items_by_pool = {}
	sorted_pools = sorted(itempools.getroot(), key=len, reverse=True)
	for pool in sorted_pools:
		total_length += len(pool)
	for pool in sorted_pools:
		items_by_pool[pool.get("Name")] = len(pool) / total_length * len(genItemList)
	total_by_pool = 0
	for pool in items_by_pool.items():
		rounded = round(pool[1])
		total_by_pool += rounded
		#print(str(pool[1]) + "	|	" + str(rounded) + "	|	" + pool[0])
		items_by_pool[pool[0]] = rounded
	#print(str(total_by_pool) + " / " + str(len(genItemList)))
	genLength = len(genItemList)
	if total_by_pool > genLength:
		i = 0
		while total_by_pool != genLength:
			items_by_pool[sorted_pools[i].get("Name")] -= 1
			total_by_pool -= 1
			i += 1
	elif total_by_pool < genLength:
		i = 0
		while total_by_pool != genLength:
			items_by_pool[sorted_pools[i].get("Name")] += 1
			total_by_pool += 1
			i += 1
	mod_itempools = open("../content/itempools.xml", "w")
	mod_itempools.write("<ItemPools>\n")
	used_modItems = 0
	for pool in itempools.getroot():
		mod_itempools.write("	<" + pool.tag + ' Name="' + pool.get("Name") + '">\n')
		amount = items_by_pool[pool.get("Name")]
		for i in range(amount):
			mod_itempools.write('		<Item Name="KZAchievementCheckerID' + str(genItemList[used_modItems + i]) + '" Weight="0.00001" DecreaseBy="0" RemoveOn="0"/>\n')
		used_modItems = used_modItems + amount
		mod_itempools.write("	</Pool>\n")
	mod_itempools.write("</ItemPools>")


fill_tables()