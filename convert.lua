local lunajson = require 'lunajson'

dofile("/tmp/GBankClassic.lua")
file = io.open("/tmp/GBankClassic.json", "w")
io.output(file)
io.write(lunajson.encode(GBankClassicDB))
io.close()
	