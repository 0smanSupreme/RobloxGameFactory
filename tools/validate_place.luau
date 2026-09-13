-- Structural validator for a generated Roblox place.
-- This is NOT a substitute for a true runtime playtest.

local fs = require("@lune/fs")
local roblox = require("@lune/roblox")

local inputPath = ...

if inputPath == nil then
	error("Usage: lune run tools/validate_place.luau <place.rbxl>")
end

local bytes = fs.readFile(inputPath)
local game = roblox.deserializePlace(bytes)
local workspace = game:GetService("Workspace")
local replicatedStorage = game:GetService("ReplicatedStorage")

local errors = {}

local function requirePath(root, parts, label)
	local current = root
	for _, name in ipairs(parts) do
		current = current:FindFirstChild(name)
		if current == nil then
			table.insert(errors, "Missing required object: " .. label)
			return nil
		end
	end
	return current
end

-- These are intentionally minimal until docs/AI_TEMPLATE_GUIDE.md is replaced
-- with the exact paths from the repaired master.
local hazardSpawn = workspace:FindFirstChild("HazardSpawn", true)
local hazardEnd = workspace:FindFirstChild("HazardEnd", true)

if hazardSpawn == nil then
	table.insert(errors, "Could not find any descendant named HazardSpawn")
end

if hazardEnd == nil then
	table.insert(errors, "Could not find any descendant named HazardEnd")
end

local generatedAssets = workspace:FindFirstChild("GeneratedHazardAssets", true)
if generatedAssets == nil then
	table.insert(errors, "Could not find GeneratedHazardAssets after generation")
elseif #generatedAssets:GetDescendants() == 0 then
	table.insert(errors, "GeneratedHazardAssets exists but is empty")
end

local framework = replicatedStorage:FindFirstChild("GameFramework")
if framework == nil then
	table.insert(errors, "ReplicatedStorage/GameFramework is missing")
end

if #errors > 0 then
	for _, message in ipairs(errors) do
		warn(message)
	end
	error("Generated place failed structural validation with " .. tostring(#errors) .. " issue(s)")
end

print("Generated place passed structural validation: " .. inputPath)
