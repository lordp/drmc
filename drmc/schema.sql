DROP TABLE IF EXISTS alts;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS player_recipes;
DROP TABLE IF EXISTS recipes;

CREATE TABLE alts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE NOT NULL,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE items (
	alt_id INTEGER NOT NULL,
	item_id INTEGER NOT NULL,
	item_name TEXT NOT NULL,
	item_count INTEGER NOT NULL,
	FOREIGN KEY (alt_id) REFERENCES alts (id)
);

CREATE TABLE recipes (
	id INTEGER UNIQUE NOT NULL,
	group_name TEXT,
	name TEXT NOT NULL,
	profession TEXT NOT NULL
);

CREATE TABLE players (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE NOT NULL
);

CREATE TABLE player_recipes (
	player_id INTEGER NOT NULL,
	recipe_id INTEGER NOT NULL,
	FOREIGN KEY (player_id) REFERENCES players (id),
	FOREIGN KEY (recipe_id) REFERENCES recipes (id)
);

CREATE TABLE player_availability (
	player_id INTEGER NOT NULL,
	availability TEXT NOT NULL,
	FOREIGN KEY (player_id) REFERENCES players (id),
);

-- Enchants
INSERT INTO recipes VALUES (23804, "Weapon", "Mighty Intellect", "enchanting");
INSERT INTO recipes VALUES (20034, "Weapon", "Crusader", "enchanting");
INSERT INTO recipes VALUES (20032, "Weapon", "Lifestealing", "enchanting");
INSERT INTO recipes VALUES (22749, "Weapon", "Spell Power", "enchanting");
INSERT INTO recipes VALUES (22750, "Weapon", "Healing Power", "enchanting");
INSERT INTO recipes VALUES (23803, "Weapon", "Mighty Spirit", "enchanting");
INSERT INTO recipes VALUES (20031, "Weapon", "Superior Striking", "enchanting");
INSERT INTO recipes VALUES (23799, "Weapon", "Strength", "enchanting");
INSERT INTO recipes VALUES (23800, "Weapon", "Agility", "enchanting");
INSERT INTO recipes VALUES (13898, "Weapon", "Fiery Weapon", "enchanting");
INSERT INTO recipes VALUES (20035, "2H Weapon", "Major Spirit", "enchanting");
INSERT INTO recipes VALUES (20036, "2H Weapon", "Major Intellect", "enchanting");
INSERT INTO recipes VALUES (20030, "2H Weapon", "Superior Impact", "enchanting");
INSERT INTO recipes VALUES (27837, "2H Weapon", "Agility", "enchanting");
INSERT INTO recipes VALUES (25086, "Cloak", "Dodge", "enchanting");
INSERT INTO recipes VALUES (25081, "Cloak", "Greater Fire Resistance", "enchanting");
INSERT INTO recipes VALUES (25082, "Cloak", "Greater Nature Resistance", "enchanting");
INSERT INTO recipes VALUES (25084, "Cloak", "Subtlety", "enchanting");
INSERT INTO recipes VALUES (25083, "Cloak", "Stealth", "enchanting");
INSERT INTO recipes VALUES (20015, "Cloak", "Superior Defense", "enchanting");
INSERT INTO recipes VALUES (20014, "Cloak", "Greater Resistance", "enchanting");
INSERT INTO recipes VALUES (13882, "Cloak", "Lesser Agility", "enchanting");
INSERT INTO recipes VALUES (13522, "Cloak", "Lesser Shadow Resistance", "enchanting");
INSERT INTO recipes VALUES (20025, "Chest", "Greater Stats", "enchanting");
INSERT INTO recipes VALUES (20028, "Chest", "Major Mana", "enchanting");
INSERT INTO recipes VALUES (20026, "Chest", "Major Health", "enchanting");
INSERT INTO recipes VALUES (13941, "Chest", "Stats", "enchanting");
INSERT INTO recipes VALUES (20023, "Boots", "Greater Agility", "enchanting");
INSERT INTO recipes VALUES (20024, "Boots", "Spirit", "enchanting");
INSERT INTO recipes VALUES (20020, "Boots", "Greater Stamina", "enchanting");
INSERT INTO recipes VALUES (13890, "Boots", "Minor Speed", "enchanting");
INSERT INTO recipes VALUES (25080, "Gloves", "Superior Agility", "enchanting");
INSERT INTO recipes VALUES (25073, "Gloves", "Shadow Power", "enchanting");
INSERT INTO recipes VALUES (25074, "Gloves", "Frost Power", "enchanting");
INSERT INTO recipes VALUES (25072, "Gloves", "Threat", "enchanting");
INSERT INTO recipes VALUES (25079, "Gloves", "Healing Power", "enchanting");
INSERT INTO recipes VALUES (25078, "Gloves", "Fire Power", "enchanting");
INSERT INTO recipes VALUES (20013, "Gloves", "Greater Strength", "enchanting");
INSERT INTO recipes VALUES (20012, "Gloves", "Greater Agility", "enchanting");
INSERT INTO recipes VALUES (13947, "Gloves", "Riding Skill", "enchanting");
INSERT INTO recipes VALUES (13868, "Gloves", "Advanced Herbalism", "enchanting");
INSERT INTO recipes VALUES (13841, "Gloves", "Advanced Mining", "enchanting");
INSERT INTO recipes VALUES (13698, "Gloves", "Skinning", "enchanting");
INSERT INTO recipes VALUES (13620, "Gloves", "Fishing", "enchanting");
INSERT INTO recipes VALUES (20016, "Shield", "Superior Spirit", "enchanting");
INSERT INTO recipes VALUES (20017, "Shield", "Greater Stamina", "enchanting");
INSERT INTO recipes VALUES (13933, "Shield", "Frost Resistance", "enchanting");
INSERT INTO recipes VALUES (13689, "Shield", "Lesser Block", "enchanting");
INSERT INTO recipes VALUES (23802, "Bracer", "Healing Power", "enchanting");
INSERT INTO recipes VALUES (20011, "Bracer", "Superior Stamina", "enchanting");
INSERT INTO recipes VALUES (20010, "Bracer", "Superior Strength", "enchanting");
INSERT INTO recipes VALUES (23801, "Bracer", "Mana Regeneration", "enchanting");
INSERT INTO recipes VALUES (20009, "Bracer", "Superior Spirit", "enchanting");
INSERT INTO recipes VALUES (20008, "Bracer", "Greater Intellect", "enchanting");
INSERT INTO recipes VALUES (13931, "Bracer", "Deflection", "enchanting");
INSERT INTO recipes VALUES (25130, "", "Brilliant Mana Oil", "enchanting");
INSERT INTO recipes VALUES (20749, "", "Brilliant Wizard Oil", "enchanting");
INSERT INTO recipes VALUES (12810, "", "Enchanted Leather", "enchanting");
INSERT INTO recipes VALUES (12655, "", "Enchanted Thorium Bar", "enchanting");

-- Alchemy
INSERT INTO recipes (id, name, profession) VALUES (17634, "Flask of Petrification", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17635, "Flask of the Titans", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17636, "Flask of Distilled Wisdom", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17637, "Flask of Supreme Power", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17554, "Elixir of Superior Defense", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17571, "Elixir of the Mongoose", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (24266, "Gurubashi Mojo Madness", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17638, "Flask of Chromatic Resistance", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (22732, "Major Rejuvenation Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17580, "Major Mana Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17556, "Major Health Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (24365, "Mageblood Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17570, "Greater Stoneshield Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17573, "Greater Arcane Elixir", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (24368, "Major Troll's Blood Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17574, "Greater Fire Protection Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17575, "Greater Frost Protection Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17576, "Greater Nature Protection Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17577, "Greater Arcane Protection Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17578, "Greater Shadow Protection Potion", "alchemy");
INSERT INTO recipes (id, name, profession) VALUES (17187, "Transmute: Arcanite", "alchemy");

-- Engineering
INSERT INTO recipes (id, name, profession) VALUES (19830, "Arcanite Dragonling", "engineering");
INSERT INTO recipes (id, name, profession) VALUES (22795, "Core Marksman Rifle", "engineering");
INSERT INTO recipes (id, name, profession) VALUES (22704, "Field Repair Bot 74A", "engineering");
INSERT INTO recipes (id, name, profession) VALUES (22797, "Force Reactive Disk", "engineering");

-- Leatherworking
INSERT INTO recipes (id, name, profession) VALUES (22927, "Hide of the Wild", "leatherworking");
INSERT INTO recipes (id, name, profession) VALUES (19093, "Onyxia Scale Cloak", "leatherworking");
INSERT INTO recipes (id, name, profession) VALUES (23709, "Corehound Belt", "leatherworking");

-- Tailoring
INSERT INTO recipes (id, name, profession) VALUES (27660, "Big Bag of Enchantment", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (18455, "Bottomless Bag", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (26087, "Core Felcloth Bag", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (18445, "Mooncloth Bag", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (24902, "Runed Stygian Belt", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (18560, "Mooncloth", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (24901, "Runed Stygian Leggings", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (24903, "Runed Stygian Boots", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (24091, "Bloodvine Vest", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (24092, "Bloodvine Leggings", "tailoring");
INSERT INTO recipes (id, name, profession) VALUES (24093, "Bloodvine Boots", "tailoring")

-- Cooking
INSERT INTO recipes (id, name, profession) VALUES (25659, "Dirge's Kickin' Chimaerok Chops", "cooking");
INSERT INTO recipes (id, name, profession) VALUES (24801, "Smoked Desert Dumplings", "cooking");
INSERT INTO recipes (id, name, profession) VALUES (22761, "Runn Tum Tuber Surprise", "cooking");
INSERT INTO recipes (id, name, profession) VALUES (18243, "Nightfin Soup", "cooking");
INSERT INTO recipes (id, name, profession) VALUES (18240, "Grilled Squid", "cooking");

-- Blacksmithing
INSERT INTO recipes (id, name, profession) VALUES (21161, "Sulfuron Hammer", "blacksmithing");
INSERT INTO recipes (id, name, profession) VALUES (23638, "Black Amnesty", "blacksmithing");
INSERT INTO recipes (id, name, profession) VALUES (27589, "Black Grasp of the Destroyer", "blacksmithing");
INSERT INTO recipes (id, name, profession) VALUES (23639, "Blackfury", "blacksmithing");
INSERT INTO recipes (id, name, profession) VALUES (23652, "Blackguard", "blacksmithing");
INSERT INTO recipes (id, name, profession) VALUES (27829, "Titanic Leggings", "blacksmithing");
