local json = require("json")
local exports = {}

local function export_table(table, path)
	local dir = string.gsub(debug.getinfo(1).source, "^@(.+/)[^/]+$", "%1")
	local file = assert(io.open(dir .. "devScripts/enums/" .. path .. ".json", "w"))
		file:write(json.encode(table))
	file:close()
end

function exports.players()
	export_table(PlayerType, "players")
end

function exports.all()
	exports.players()
end

exports.table = export_table

return exports