local mod = RegisterMod("KZAchievementChecker", 1)
local json = require("json")
mod.exportEnums = require("exportEnum")
local unlocks = {}
local collectibleUnlocks = require("static.collectibles")
local playerUnlocks = require("static.players")
local trinketUnlocks = require("static.trinkets")
local cardUnlocks = require("static.cards")
local pillUnlocks = require("static.pills")

if not KZLibs then
	KZLibs = {}
end
KZLibs.AchievementChecker = mod

-- Call this [KZLibs.AchievementChecker.isAchievementUnlocked(x)] to get unlock status about achievement x, argument is a number between 1 and 637
function mod.isAchievementUnlocked(achievement)
	if achievement > 0 then
		return unlocks[achievement]
	end
	return true
end

-- Argument is a CollectibleType
function mod.isCollectibleUnlocked(collectible)
	if collectible ~= nil then
		if collectible == 0 then
			return true
		end
---@diagnostic disable-next-line: need-check-nil
		local id = collectibleUnlocks[collectible]
		if id ~= nil then
			return mod.isAchievementUnlocked(id)
		end
	end
	return nil
end

-- Argument is a PlayerType
function mod.isPlayerUnlocked(player)
	if player ~= nil then
		if player == 0 or player == -1 then
			return true
		end
---@diagnostic disable-next-line: need-check-nil
		local id = playerUnlocks[player]
		if id ~= nil then
			return mod.isAchievementUnlocked(id)
		end
	end
	return nil
end

-- Argument is a TrinketType
function mod.isTrinketUnlocked(trinket)
	if trinket ~= nil then
		if trinket == 0 then
			return true
		end
---@diagnostic disable-next-line: need-check-nil
		local id = trinketUnlocks[trinket]
		if id ~= nil then
			return mod.isAchievementUnlocked(id)
		end
	end
	return nil
end

-- Argument is a Card
function mod.isCardUnlocked(card)
	if card ~= nil then
		if card == 0 or card == -1 then
			return true
		end
---@diagnostic disable-next-line: need-check-nil
		local id = cardUnlocks[card]
		if id ~= nil then
			return mod.isAchievementUnlocked(id)
		end
	end
	return nil
end

-- Argument is a PillEffect
function mod.isPillUnlocked(pill)
	if pill ~= nil then
		if pill == -1 then
			return true
		end
---@diagnostic disable-next-line: need-check-nil
		local id = pillUnlocks[pill]
		if id ~= nil then
			return mod.isAchievementUnlocked(id)
		end
	end
	return nil
end


local modCollectiblesStart = Isaac.GetItemIdByName("KZAchievementCheckerID1")
local modCollectiblesEnd = Isaac.GetItemIdByName("KZAchievementCheckerID637")

local function clearUnlocks()
	for a=1, 637 do
		unlocks[a] = false
	end
end
clearUnlocks()

local function checkUnlocks()
	clearUnlocks()

	local player = Isaac.GetPlayer(0)
	local playerHasChaos = false
	local playerHasTMTrainer = false

	if player:HasCollectible(CollectibleType.COLLECTIBLE_CHAOS) then
		player:RemoveCollectible(CollectibleType.COLLECTIBLE_CHAOS)
		playerHasChaos = true
	end

	if player:HasCollectible(CollectibleType.COLLECTIBLE_TMTRAINER) then
		player:RemoveCollectible(CollectibleType.COLLECTIBLE_TMTRAINER)
		playerHasTMTrainer = true
	end

	local itemPool = Game():GetItemPool()

	itemPool:AddRoomBlacklist(CollectibleType.COLLECTIBLE_SKATOLE)
	itemPool:AddRoomBlacklist(CollectibleType.COLLECTIBLE_POOP)
	itemPool:AddRoomBlacklist(CollectibleType.COLLECTIBLE_BUTT_BOMBS)
	itemPool:AddRoomBlacklist(CollectibleType.COLLECTIBLE_NUMBER_TWO)
	itemPool:AddRoomBlacklist(CollectibleType.COLLECTIBLE_BROWN_NUGGET)
	itemPool:AddRoomBlacklist(CollectibleType.COLLECTIBLE_DIRTY_MIND)

	local isPoolNotEmpty = true

	while isPoolNotEmpty do
		local collectible = itemPool:GetCollectible(ItemPoolType.POOL_SHELL_GAME, true, Random(), CollectibleType.COLLECTIBLE_SAD_ONION)
		if collectible >= modCollectiblesStart and collectible <= modCollectiblesEnd then
			unlocks[collectible - modCollectiblesStart + 1] = true
		else
			if collectible == CollectibleType.COLLECTIBLE_SAD_ONION then
				isPoolNotEmpty = false
			end
		end
	end

	mod:SaveData(json.encode(unlocks))

	if playerHasChaos then
		player:AddCollectible(CollectibleType.COLLECTIBLE_CHAOS, 0, false)
	end
	if playerHasTMTrainer then
		player:AddCollectible(CollectibleType.COLLECTIBLE_TMTRAINER, 0, false)
	end

	itemPool:ResetRoomBlacklist()
end

local function onGameStart(_, isContinued)
	if isContinued then
		if mod:HasData() then
			unlocks = json.decode(mod:LoadData())
		else
			clearUnlocks()
		end
	else
		checkUnlocks()
	end
end

mod:AddCallback(ModCallbacks.MC_POST_GAME_STARTED, onGameStart)

if mod:HasData() then
	unlocks = json.decode(mod:LoadData())
end