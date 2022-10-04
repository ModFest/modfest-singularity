# A quick little server-ready script - designed to have actions run only once, then
# automatically prevent them from running again.
execute if block -100 -64 -100 bedrock run scoreboard objectives add CA_totalPlayerJoins dummy "Joins"
execute if block -100 -64 -100 bedrock run scoreboard objectives add CA_uniquePlayerJoins dummy "Unique Joins"
execute if block -100 -64 -100 bedrock run setblock -100 -64 -100 barrier