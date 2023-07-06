local json = require("json")
local exports = {}

local function export_table(table, path)
	local dir = string.gsub(debug.getinfo(1).source, "^@(.+/)[^/]+$", "%1")
	local file = assert(io.open(dir .. "devScripts/enums/" .. path .. ".json", "w"))
		file:write(json.encode(table))
	file:close()
end

function exports.collectibles()
	export_table(CollectibleType, "collectibles")
end

function exports.players()
	export_table(PlayerType, "players")
end

function exports.trinkets()
	export_table(TrinketType, "trinkets")
end

function exports.cards()
	export_table(Card, "cards")
end

function exports.pills()
	export_table(PillEffect, "pills")
end

function exports.all()
	exports.collectibles()
	exports.players()
	exports.trinkets()
	exports.cards()
	exports.pills()
end

exports.table = export_table

return exports