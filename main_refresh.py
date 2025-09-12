import json, os, random, math, time, socket, server, Encryption, threading #server is self made to split up Multiplayer and client code
from queue import Queue

#Skill formatting:
#List: {0 : , 1 : , 2 : , 3 : ]
#0 --> Damage multiplier (* normal damage)
#1 --> Heal back (* dealt damage)
#2 --> Status effect: 0: None, 1: freeze, 2: fire
#3 --> Buff: 0: None, 1: strenght buff (mult), 2: dexterity buff (mult), 3: defense buff (mult), 4: instant heal <num>

e = Encryption.Encryption()
Q_transfer = Queue()

space = "===================="

stat_default = {
    "strenght" : 10,
    "b_strenght" : 10,
    "dexterity" : 10,
    "b_dexterity" : 10,
    "defense" : 10,
    "b_defense" : 10,
    "health" : 100,
    "maxhealth" : 100,
    "xp" : 0,
    "level" : 1,
    "gear" : {},
    "pets" : {},
    "e_sword" : None,
    "e_shield" : None,
    "e_armor" : None,
    "e_pet" : None,
    "t_floor" : 1,
    "t_level" : 1,
    "silver" : 0,
    "dmg_record" : 0,
    "boss_day" : 0,
    "pet_eggs" : 0,
    "hatching_egg" : [False, 0],
    "d_quest" : [],
    "mining_level" : 1,
    "mining_xp" : 0,
    "iron" : 0,
    "gold" : 0,
    "g_gems" : 0, #green gems
    "b_gems" : 0, #blue gems
    "r_gems" : 0, #red gems
    "p_gems" : 0, #purple gems
    "rg_gems" : 0, #refined green gems
    "rb_gems" : 0, #refined blue gems
    "rr_gems" : 0, #refined red gems
    "rp_gems" : 0, #refined purple gems
    "c_gems" : 0, #clean gems
    "rc_gems" : 0 #refined clean gems
    }

drop_chances = {
    "common" : 27,
    "rare" : 75,
    "epic" : 90,
    "legendary" : 98
    }

#c_r: index 0 is a dictionairy with rewards: {(player_stat_key) : (amount)}
d_quests = [
    {
        "name" : "Find the lost pickaxe",
        "desc" : "A miner who got lost in the dungeons, lost his pickaxe and needs help finding it back!",
        "comp_msg" : "After giving the pickaxe back to the miner, he thanks you and gives you a green gem!",
        "c_r" : [{"g_gems" : 1}]
        }
    ]

ore_rates = {
    "iron" : 0,
    "gold" : 10,
    "g_gems" : 15,
    "b_gems" : 25,
    "r_gems" : 40,
    "rg_gems" : 76,
    "rb_gems" : 125,
    "rr_gems" : 200
    }

gear = {
    "Wooden Sword" : {
        "name" : "Wooden Sword",
        "rarity" : "common",
        "defense" : 0,
        "strenght" : 6,
        "dexterity" : 2,
        "type" : "sword",
        "skill" : False
        },
    "Wooden Pricker" : {
        "name" : "Wooden Pricker",
        "rarity" : "common",
        "defense" : 0,
        "strenght" : 12,
        "dexterity" : 5,
        "type" : "sword",
        "skill" : False
        },
    "Big Fork" :  {
        "name" : "Big Fork",
        "rarity" : "common",
        "defense" : 0,
        "strenght" : 5,
        "dexterity" : 0,
        "type" : "sword",
        "skill" : True,
        "skill_d" : {
            "desc" : "Deal 2x normal damage",
            "msg" : "You prick your fork in your enemy",
            "SD" : [2, 0, 0, [0], [0]],
            "item" : "Big Fork"
            }
        },
    "Iron Sword" : {
        "name" : "Iron Sword",
        "rarity" : "common",
        "defense" : 32,
        "strenght" : 10,
        "dexterity" : 4,
        "type" : "sword",
        "skill" : False
        },
    "Broken Knife" : {
        "name" : "Broken Knife",
        "rarity" : "common" ,
        "defense" : 0,
        "strenght" : 8,
        "dexterity" : 7,
        "type" : "sword",
        "skill" : False
        },
    "Hard Bone" : {
        "name" : "Hard Bone",
        "rarity" : "rare",
        "defense" : 0,
        "dexterity" : 0,
        "strenght" : 22,
        "type" : "sword",
        "skill" : False
        },
    "Clean Blade" : {
        "name" : "Clean Blade",
        "rarity" : "rare",
        "defense" : 0,
        "dexterity" : 15,
        "strenght" : 15,
        "type" : "sword",
        "skill" : False
        },
    "Blood Fang" : {
        "name" : "Blood Fang",
        "rarity" : "epic",
        "defense" : 40,
        "dexterity" : 10,
        "strenght" : 20,
        "type" : "sword",
        "skill" : True,
        "skill_d" : {
            "desc" : "Deal 2x normal damage and gain 25% of the damage dealt back as health",
            "msg" : "You slay the Fang with a mighty swing in your enemy while feeling your energy come back",
            "SD" : [2, .25, 0, [0], [0]],
            "item" : "Blood Fang"
            }
        },
    "Rhino Horn" : {
        "name" : "Rhino Horn",
        "rarity" : "epic",
        "defense" : 300,
        "dexterity" : 2,
        "strenght" : 5,
        "type" : "sword",
        "skill" : True,
        "skill_d" : {
            "desc" : "Get 3x defense",
            "msg" : "You use your horn with all your might and feel yourself getting tougher",
            "SD" : [2, 0, 0, [3, 3], [0]],
            "item" : "Rhino Horn"
            }
        },
    "Soulstealer Shortbow" : {
        "name" : "Soulstealer Shortbow",
        "rarity" : "legendary",
        "defense" : 100,
        "dexterity" : 60,
        "strenght" : 60,
        "type" : "sword",
        "skill" : True,
        "skill_d" : {
            "desc" : "Deal 5x normal damage",
            "msg" : "While feeling a legendary energy going through your veins you aim your bow and strike...",
            "SD" : [5, 0, 0, [1, 2], [1, 100]],
            "item" : "Soulstealer Shortbow"
            }
        },
    "Wooden Shield" : {
        "name" : "Wooden Shield",
        "rarity" : "common",
        "defense" : 25,
        "dexterity" : 0,
        "strenght" : 0,
        "type" : "shield",
        "skill" : False
        },
    "Iron Shield" : {
        "name" : "Iron Shield",
        "rarity" : "common",
        "defense" : 40,
        "dexterity" : 0,
        "strenght" : 0,
        "type" : "shield",
        "skill" : False
        },
    "Bone Shield" : {
        "name" : "Bone Shield",
        "rarity" : "rare",
        "defense" : 60,
        "dexterity" : 0,
        "strenght" : 10,
        "type" : "shield",
        "skill" : False
        },
    "Stone Shield" : {
        "name" : "Stone Shield",
        "rarity" : "rare",
        "defense" : 100,
        "dexterity" : -20,
        "strenght" : 0,
        "type" : "shield",
        "skill" : False
        },
    "Power Shield" : {
        "name" : "Power Shield",
        "rarity" : "rare",
        "defense" : 50,
        "dexterity" : 0,
        "strenght" : 25,
        "type" : "shield",
        "skill" : True,
        "skill_d" : {
            "desc" : "Throw the shield at your enemy, for 2.5x normal damage",
            "msg" : "You throw the shield with a powerful swing at your enemy",
            "SD" : [2.5, 0, 0, [0], [0]],
            "item" : "Power Shield"
            }
        },
    "Bloodshed Shield" : {
        "name" : "Bloodshed Shield",
        "rarity" : "epic",
        "defense" : 125,
        "dexterity" : 25,
        "strenght" : 25,
        "type" : "shield",
        "skill" : True,
        "skill_d" : {
            "desc" : "Charge a beam of blood and gain back 100% of dealt damage",
            "msg" : "You feel a inner energy coming out of you...",
            "SD" : [1, 1, 0, [0], [0]],
            "item" : "Bloodshed Shield"
            }
        },
    "Rhino Skull" : {
        "name" : "Rhino Skull",
        "rarity" : "epic",
        "defense" : 200,
        "dexterity" : 0,
        "strenght" : 0,
        "type" : "shield",
        "skill" : True,
        "skill_d" : {
            "desc" : "Get 3x defense",
            "msg" : "You put the sturdy skull in front of you and feel stronger",
            "SD" : [0, 0, 0, [3, 3], [0]],
            "item" : "Rhino Skull"
            }
        },
    "Shield of the Souls" : {
        "name" : "Shield of the Souls",
        "rarity" : "legendary",
        "defense" : 400,
        "dexterity" : 50,
        "strenght" : 50,
        "type" : "shield",
        "skill" : True,
        "skill_d" : {
            "desc" : "Get 3x strenght and deal 3x damage",
            "msg" : "You feel a beam of light going out of your shield get stronger",
            "SD" : [3, 0, 0, [1, 3], [1, 100]],
            "item" : "Shield of the Souls"
            }
        },
    "Leather Armor" : {
        "name" : "Leather Armor",
        "rarity" : "common",
        "defense" : 15,
        "dexterity" : 10,
        "strenght" : 0,
        "type" : "armor",
        "skill" : False
        },
    "Metal Armor" : {
        "name" : "Metal Armor",
        "rarity" : "common",
        "defense" : 40,
        "dexterity" : 0,
        "strenght" : 25,
        "type" : "armor",
        "skill" : False
        },
    "Armor of Bones" : {
        "name" : "Armor of Bones",
        "rarity" : "rare",
        "defense" : 60,
        "dexterity" : 0,
        "strenght" : 0,
        "type" : "armor",
        "skill" : True,
        "skill_d" : {
            "desc" : "Get 2x damage for battle",
            "msg" : "You rittle the bone armor and feel yourself getting stronger",
            "SD" : [1, 0, 0, [1, 2], [0]],
            "item" : "Armor of Bones"
            }
        },
    "Cloth of Blood" : {
        "name" : "Cloth of Blood",
        "rarity" : "epic",
        "defense" : 40,
        "dexterity" : 35,
        "strenght" : 35,
        "type" : "armor",
        "skill" : True,
        "skill_d" : {
            "desc" : "Seal yourself in a veil of blood...",
            "msg" : "You feel a breeze filled with blood going around you",
            "SD" : [1.5, 0.5, 0, [3, 2], [0]],
            "item" : "Cloth of Blood"
            }
        },
    "Rhino Hide" : {
        "name" : "Rhino Hide",
        "rarity" : "epic",
        "defense" : 300,
        "dexterity" : 5,
        "strenght" : 5,
        "type" : "armor",
        "skill" : True,
        "skill_d" : {
            "desc" : "Go under the protective cover of the hide of a Rhino",
            "msg" : "You hide under the thick hide of a Rhino...",
            "SD" : [1, 0, 0, [3, 3], [0]],
            "item" : "Rhino Hide"
            }
        },
    "Mithril Armor" : {
        "name" : "Mithril Armor",
        "rarity" : "epic",
        "defense" : 150,
        "dexterity" : 0,
        "strenght" : 0,
        "type" : "armor",
        "skill" : False
        }
    }

#Pet buff definition:
#Index 0: Player Buff --> [0] if none, [1, <mult>] for strenght, [2, <mult>] for dexterity, [3, <mult>] for defense
pet = {
    "Black Cat" : {
        "name" : "Black Cat",
        "nametag" : "",
        "dmg" : 75,
        "xp" : 0,
        "level" : 1,
        "buff" : [[0]],
        "rarity" : "common"
        },
    "Ice Snake" : {
        "name" : "Ice Snake",
        "nametag" : "",
        "dmg" : 25,
        "xp" : 0,
        "level" : 1,
        "buff" : [[3, 2]],
        "rarity" : "rare"
        },
    "Rexy" : {
        "name" : "Rexy",
        "nametag" : "",
        "dmg" : 100,
        "xp" : 0,
        "level" : 1,
        "buff" : [[1, 2]],
        "rarity" : "epic"
        },
    "Forest Fantom" : {
        "name" : "Forest Fantom",
        "nametag" : "",
        "dmg" : 150,
        "xp" : 0,
        "level" : 1,
        "buff" : [[3,3]],
        "rarity" : "legendary"
        }
    }         

enemies = {
    "Goblin" : {
        "health" : 12,
        "defense" : 5,
        "strenght" : 5,
        "dexterity" : 5,
        "xp" : 1
        },
    "Spider" : {
        "health" : 15,
        "defense" : 6,
        "strenght" : 5,
        "dexterity" : 5,
        "xp" : 2
    },
    "Zombie" : {
        "health" : 20,
        "defense" : 8,
        "strenght" : 5,
        "dexterity" : 5,
        "xp" : 3
        },
    "Orc" : {
        "health" : 10,
        "defense" : 0,
        "strenght" : 8,
        "dexterity" : 8,
        "xp" : 3
        },
    "Venom Snake" : {
        "health" : 10,
        "defense" : 0,
        "strenght" : 15,
        "dexterity" : 0,
        "xp" : 5
        },
    "Ice Snake" : {
        "health" :  20,
        "defense" : 10,
        "strenght" : 2,
        "dexterity" : 1,
        "xp" : 3
        }
}

enemy_keys = list(enemies.keys())

bosses = {
    "Giant" : {
        "health" : 25,
        "defense" : 20,
        "strenght" : 15,
        "dexterity" : 15,
        "xp" : 10,
        "s_msg" : "A very big giant towers over you and you feel him breathing"
        },
    "Rock Golem" : {
        "health" : 60,
        "defense" : 30,
        "strenght" : 5,
        "dexterity" : 0,
        "xp" : 10,
        "s_msg" : "While walking around you found a weird looking stone... NOOOOOO. ITS ALIVEEEEEE"
        },
    "Queen Spider" : {
        "health" : 50,
        "defense" : 5,
        "strenght" : 25,
        "dexterity" : 25,
        "xp" : 12,
        "s_msg" : "The mightiest of all spiders: Queen Spider"
        }
    }

boss_keys = list(bosses.keys())

class Player:
    def __init__(self, name):
        self.name = name
        self.activity = "menu"
        for key in stat_default:
            setattr(self, key, stat_default.get(key))
    def stats(self):
        print("--- Character Overview " + self.name + " Lvl " + str(self.level) + " ---")
        print("Highest damage:", self.dmg_record)
        print("Strenght: " + str(self.strenght))
        print("Defense: " + str(self.defense))
        print("Dexterity: " + str(self.dexterity))
        print("Health: ", str(self.health), "/", str(self.maxhealth))
        print("XP: " + str(self.xp) + "/" + str(self.level * 5))
        print("Silver: " + str(self.silver))
        print("\nTower Stats:\nFLOOR: " + str(self.t_floor) + "\nLEVEL: " + str(self.t_level))
        print("\n")
        wait = input("Press ENTER to continue")
    def update(self):
        c_strenght = self.b_strenght + (self.level - 1) * 10
        c_dexterity = self.b_dexterity + (self.level - 1) * 10
        c_defense = self.b_defense + (self.level - 1) * 10
        if not self.e_sword == None:
            c_strenght = c_strenght + int(self.e_sword["strenght"])
            c_dexterity = c_dexterity + int(self.e_sword["dexterity"])
            c_defense = c_defense + int(self.e_sword["defense"])
        if not self.e_shield == None:
            c_strenght = c_strenght + int(self.e_shield["strenght"])
            c_dexterity = c_dexterity + int(self.e_shield["dexterity"])
            c_defense = c_defense + int(self.e_shield["defense"])
        if not self.e_armor == None:
            c_strenght = c_strenght + int(self.e_armor["strenght"])
            c_dexterity = c_dexterity + int(self.e_armor["dexterity"])
            c_defense = c_defense + int(self.e_armor["defense"])
        self.strenght = c_strenght
        self.dexterity = c_dexterity
        self.defense = c_defense
    def check_egg(self):
        if self.pet_eggs > 0 and not self.hatching_egg[0]:
            self.hatching_egg = [True, 0]
            self.pet_eggs = self.pet_eggs - 1
            print("You started hatching your pet egg!")
    def pet_hatching(self, xp, msg):
        if not self.hatching_egg[0]:
            return
        self.hatching_egg[1] = self.hatching_egg[1] + xp
        if msg:
            Gxp = self.hatching_egg[1]
            print(f"Egg hatching progress: {Gxp}/100")
        if self.hatching_egg[1] >= 100:
            pet_list = []
            owned_pets = []
            for x in self.pets:
                    owned_pets.append(x)
            for x in pet:
                pet_list.append(x)
            if pet_list == owned_pets:
                print("\nYou already collected all pets! You will get 5 free lootboxes instead.")
                self.hatching_egg = [False]
                return
            commons = []
            rares = []
            epics = []
            legendarys = [] 
            for x in pet:
                if pet[x]["rarity"] == "common":
                    commons.append(x)
                if pet[x]["rarity"] == "rare":
                    rares.append(x)
                if pet[x]["rarity"] == "epic":
                    epics.append(x)
                if pet[x]["rarity"] == "legendary":
                    legendarys.append(x)
            while True:
                n = random.randint(0, 100)
                if n > drop_chances["legendary"]:
                    n = random.randint(0, (len(legendarys) - 1))
                    dPet = legendarys[n]
                elif n > drop_chances["epic"]:
                    n = random.randint(0, (len(epics) - 1))
                    dPet = epics[n]
                elif n > drop_chances["rare"]:
                    n = random.randint(0, (len(rares) - 1))
                    dPet = rares[n]
                else:
                    n = random.randint(0, (len(commons) - 1))
                    dPet = commons[n]
                dPet = pet_list[n]
                if not dPet in owned_pets:
                    break
            print(f"\nYour pet egg hatched! You got a {dPet}! It was added to your pet library\n")
            self.hatching_egg = [False]
            self.pets.update({dPet : pet[dPet]})
            if self.pet_eggs > 0:
                self.pet_eggs = self.pet_eggs - 1
                self.hatching_egg = [False, 0]
                print("\nHatching new egg!")
    def additem(self, item_name):
        library = gear[item_name]
        new_item = gear[item_name]
        self.gear.update({item_name : new_item})
    def save(self):
        file_name = self.name + ".json"
        
        data = {
            "name" : self.name,
            "b_strenght" : self.b_strenght,
            "strenght" : self.strenght,
            "b_defense" : self.b_defense,
            "defense" : self.defense,
            "health" : self.health,
            "b_dexterity" : self.b_dexterity,
            "dexterity" : self.dexterity,
            "maxhealth" : self.maxhealth,
            "gear" : self.gear,
            'xp' : self.xp,
            "level" : self.level,
            "pets" : self.pets,
            "e_sword" : self.e_sword,
            "e_shield" : self.e_shield,
            "e_armor" : self.e_armor,
            "e_pet" : self.e_pet,
            "t_floor" : self.t_floor,
            "t_level" : self.t_level,
            "silver" : self.silver,
            "dmg_record" : self.dmg_record,
            "boss_day" : self.boss_day,
            "pet_eggs" : self.pet_eggs,
            "hatching_egg" : self.hatching_egg,
            "d_quest" : self.d_quest,
            "iron" : self.iron,
            "gold" : self.gold,
            "g_gems" : self.g_gems,
            "b_gems" : self.b_gems,
            "r_gems" : self.r_gems,
            "rg_gems" : self.rg_gems,
            "rb_gems" : self.rb_gems,
            "rr_gems" : self.rr_gems,
            "c_gems" : self.c_gems,
            "rc_gems" : self.rc_gems
            }
        data = e.encrypt(data).encode("utf-8")
        with open(file_name, "wb") as f:
            f.write(data)
    def load(self, data):
        for key in stat_default:
            setattr(self, key, data.get(key, stat_default.get(key)))
        for name in self.gear:
            self.gear.update({name : gear[name]})
        if self.e_sword:
            self.e_sword = gear[self.e_sword["name"]]
        if self.e_shield:
            self.e_shield= gear[self.e_shield["name"]]
        if self.e_armor:
            self.e_armor = gear[self.e_armor["name"]]
    def stat(self, *args):
        request = args[0]
        if request == "name": return self.name
        if request == "strenght": return self.strenght
        if request == "defense": return self.defense
        if request == "dexterity": return self.dexterity
        if request == "health": return self.health
        if request == "maxhealth": return self.maxhealth
        if request == "gear": return self.gear
        if request == "xp": return self.xp
        if request == "level": return self.level
        if request == "e_sword": return self.e_sword
        if request == "t_floor": return self.t_floor
        if request == "t_level": return self.t_level
    def change_stat(self, **kwargs):
        try:
            defense = kwargs["defense"]
        except:
            defense = 0
        try:
            strenght = kwargs["strenght"]
        except:
            strenght = 0
        try:
            dexterity = kwargs["dexterity"]
        except:
            dexterity = 0
        try:
            piercing_damage = kwargs["health"]
        except:
            piercing_damage = 0
        try:
            xp = kwargs["xp"]
        except:
            xp = 0
        try:
            self.e_sword = kwargs["e_sword"]
        except:
            pass
        try:
            pet_xp = kwargs["pet_xp"]
        except:
            pet_xp = 0
        for x in range(xp):
            if xp > 0:
                self.xp = self.xp + 1
                xp = xp -1
                if self.xp >= (self.level * 5):
                    self.xp = 0
                    self.level = self.level + 1
                    print("\nLEVEL UP:", self.name, "Level", self.level, "\n")
        for x in range(pet_xp):
            if pet_xp > 0:
                xp = self.e_pet["xp"] + 1
                self.e_pet.update({"xp" : (self.e_pet["xp"] + 1)})
                level = self.e_pet["level"]
                if self.e_pet["xp"] >= (self.e_pet["level"] * 15):
                    self.e_pet.update({"level" : (self.e_pet["level"] + 1)})
                    self.e_pet.update({"xp" : 0})
                    xp = 0
                    level = self.e_pet["level"]
                    if e_pet["nametag"] == "":
                        print(f"\nPet {self.e_pet['name']} leveled up!\n")
                    else:
                        print(f"\nPet {self.e_pet['nametag']} leveled up!\n")
                pet_info = self.pets[self.e_pet["name"]]
                pet_info.update({"xp" : xp})
                pet_info.update({"level" : level})
                self.pets.update({self.e_pet["name"] : pet_info})
                pet_xp = pet_xp - 1
        self.defense = self.defense + defense
        self.strenght = self.strenght + strenght
        self.dexterity = self.dexterity + dexterity
        self.health = math.floor(self.health + piercing_damage)
    def attack(self, b_strenght):
        e_defense = enemy_fight.stat("defense")
        e_dexterity = enemy_fight.stat("dexterity")
        e_dmg_reduct = 1 - (e_defense / (e_defense + 100))
        crit = random.randint(0, 5)
        random_damage_mult = (random.randint(7, 13) / 10)
        if crit == 5:
            return self.strenght * b_strenght * e_dmg_reduct * 2 * -1
        else:
            e_dodge_chance = e_dexterity / (e_dexterity + 100)
            dodge = random.randint(0, 100)
            if dodge > e_dodge_chance:
                return self.strenght * b_strenght * e_dmg_reduct * random_damage_mult * -1
            else:
                return 0
    def L_skills(self):
        skills = []
        if self.e_sword:
            if self.e_sword["skill"]:
                 skills.append(self.e_sword["skill_d"])
        if self.e_shield:
            if self.e_shield["skill"]:
                 skills.append(self.e_shield["skill_d"])
        if self.e_armor:
            if self.e_armor["skill"]:
                 skills.append(self.e_armor["skill_d"])                 
        return skills
        
class Enemy:
    def __init__(self, enemy_type, damage, health, defense, dexterity, xp):
        self.type = enemy_type
        self.damage = damage
        self.health = health
        self.defense = defense
        self.dexterity = dexterity
        self.xp = xp
    def get_damage(self, damage):
        self.dgm_reduct = self.defense / (self.defense + 100)
        self.health = math.floor(self.health + damage)
        if self.health < 0:
            print("You killed " + self.type + "!")
            del self
    def change_stat(self, **kwargs):
        try:
            defense = kwargs["defense"]
        except:
            defense = 0
        try:
            damage = kwargs["damage"]
        except:
            damage = 0
        try:
            dexterity = kwargs["dexterity"]
        except:
            dexterity = 0
        try:
            piercing_damage = kwargs["health"]
        except:
            piercing_damage = 0
        self.defense = self.defense + defense
        self.damage = self.damage + damage
        self.dexterity = self.dexterity + dexterity
        self.health = self.health + piercing_damage
    def stat(self, *args):
        request = args[0]
        if request == "type":
            return self.type
        if request == "defense":
            return self.defense
        if request == "damage":
            return self.damage
        if request == "dexterity":
            return self.dexterity
        if request == "health":
            return self.health
        if request == "xp":
            return self.xp
    def attack(self, b_defense, b_dexterity):
        p_defense = Character.stat("defense") * b_defense
        p_dexterity = Character.stat("dexterity") * b_dexterity
        p_dmg_reduct = 1 - (p_defense / (p_defense + 100))
        crit = random.randint(0, 5)
        random_damage_mult = (random.randint(7, 13) / 10)
        if crit == 5:
            return self.damage * p_dmg_reduct * 2 * -1
        else:
            p_dodge_chance = p_dexterity / (p_dexterity + 100)
            dodge = random.randint(0, 100)
            if dodge > p_dodge_chance:
                return self.damage * p_dmg_reduct * random_damage_mult * -1
            else:
                return 0

def auto_actions():
    global my_stats, f_data, Q_transfer, time_yday
    my_stats = {}
    while True:
        time.sleep(15)
        Character.save()
        for key in stat_default:
            my_stats.update({key : Character.stat(key)})
            #Refresh stats every 15 seconds

        #All multiplayer handling here:
        if server.get("conn"):
            Q_transfer.put("activity")
        time_yday = time.gmtime(time.time())[7]
        if Character.pet_eggs > 0 and Character.egg_hatching[0] == False:
            Character.pet_eggs = Character.pet_eggs -1
            Character.pet_hatching = [True, 0]
            
def m_handler():
    global f_stats, f_data, Q_transfer

    f_data = {}
    
    while not server.get("conn"):
        #Dont lag CPU but only run commands after getting connection
        time.sleep(0.05)
    print("Got connection! -", server.get("f_ip"))
    f_stats = None
    for key in stat_default:
        my_stats.update({key : Character.stat(key)})
    transfer = {"f_stats" : my_stats}
    server.do_transfer(transfer)
    time.sleep(1)
    while True:
        #print("DEBUG")
        transfer = {"f_stats" : my_stats}
        try:
            received_data = server.get_receive()
            if received_data:
                if received_data["f_stats"]:
                    f_stats = received_data["f_stats"]
                if received_data["request"]:
                    with received_data["request"] as request:
                        #Requests and responses here
                        if request == "activity":
                            r_request = Character.activity
                            transfer.update({"activity" : r_request})
                if received_data["activity"]: f_data.update({"activity" : received_data["activity"]})    
            try:
                transfer.update({"request" : Q_transfer.get()})
            except: pass
        except: pass
        #print("Pre Transfer")
        server.do_transfer(transfer)
        #print("Transferred!")
        #print(transfer)
        time.sleep(0.05)

def pet_menu():
    print(space + "\n---   PET MENU   ---")
    if Character.hatching_egg[0]:
        p_xp = Character.hatching_egg[1]
        print(f"Hatching progress: {p_xp}/100")
    else:
        print("Hatching progress: No Egg is Hatching")
    eggs = Character.pet_eggs
    print(f"Eggs: {eggs}")
    if Character.e_pet:
        if Character.e_pet["nametag"] == "":
            print("\nEquipped Pet: " + Character.e_pet["name"] + " - Level " + str(Character.e_pet["level"]) + "(" + str(Character.e_pet["xp"]) + "/" + str(Character.e_pet["level"] * 15) + ")")
        else:
            print("\nEquipped Pet: " + Character.e_pet["nametag"] + " (" + Character.e_pet["name"] + ") - Level " + str(Character.e_pet["level"]) + "(" + str(Character.e_pet["xp"]) + "/" + str(Character.e_pet["level"] * 15) + ")")
    else:
        print("\nEquipped Pet: None")
    y = 0
    pL = []
    if Character.pets:
        for x in Character.pets:
            if Character.pets[x]["nametag"] == "":
                print(str(y) + ". " + str(Character.pets[x]["name"]) + " - Level " + str(Character.pets[x]["level"]))
            else:
                print(str(y) + ". " + str(Character.pets[x]["nametag"]) + " (" + Character.pets[x]["name"] + ") - Level " + str(Character.pets[x]["level"]))
            pL.append(x)
    while True:
        p_input = input("E <num> to equip   -   N <num> name pet   -   ENTER to exit\n")
        if p_input == "":
            break
        
        if p_input[0] == "E":
            if p_input[1]:
                if int(p_input[1:]) <= len(pL) and int(p_input[1:]) >= 0:
                    select = pL[int(p_input[1:])]
                    Character.e_pet = pet[select]
                    print("Equipped pet: " + Character.e_pet["name"])
                    wait = input("\nPress ENTER to continue")
                else:
                    print("Invalid input")
            else:
                print("Invalid input")
        if p_input[0] == "N":
            if p_input[1]:
                if int(p_input[1:]) <= len(pL) and int(p_input[1:]) >= 0:
                    select = pL[int(p_input[1:])]
                    rename = input(f"Name for {select}(none to cancel): ")
                    if not rename == "":
                        pet_info = Character.pets[select]
                        pet_info.update({"nametag" : rename})
                        Character.pets.update({select : pet_info})
                        if Character.e_pet["name"] == pet_info["name"]:
                            Character.e_pet.update({"nametag" : rename})

def multiplayer():
    global f_ip
    while True:
        Character.activity = "mult"
        print("\n--- Tower RPG Local Multiplayer ---")
        if not server.get("conn"):
            print("[H]ow-to   -   [I]IP   -   [C]onnect   -   [S]tart Hosts\n[M]ain Menu")
        else:
            print("[F]riend Stats   -   [M]ain Menu   -   [B]attle")
        p_input = input()
        if p_input == "H" or p_input == "h":
            print("1. Run [I]P on your device\n2. Press [C]onnect on the other device and input the Key.\n3.") #finish this guide
        elif p_input == "I" or p_input == "i":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            print("Your key: " + s.getsockname()[0])
            s.close()
        elif p_input == "C" or p_input == "c":
            f_ip = input("Type exactly the key from your friend:\n")
            server.start_client(f_ip)
            time.sleep(0.5)
            print("Connecting...")
            break
        elif p_input == "S" or p_input == "s":
            f_ip = input("Type exactly the key from your friend:\n")
            server.start_server(f_ip)
            time.sleep(0.5)
            print("Connecting...")
            break
        elif p_input == "F" or p_input == "f":
            if f_stats:
                if f_data["activity"]: f_activity = f_data["activity"]
                else: f_activity = "..."
                print("Health: " + str(f_stats["health"]) + "/" + str(f_stats["maxhealth"]) + "\nPlaying: " + f_activity)
                print()
            else:
                print("Could not find your friends stats...")
        elif p_input == "M" or p_input == "m":
            print("\n")
            break

def fight(**battle):
    b_defense = battle.get("b_defense")
    b_strenght = battle.get("b_strenght")
    b_dexterity = battle.get("b_dexterity")
    if Character.e_pet:
        if not Character.e_pet["buff"][0] == 0:
            buff = Character.e_pet["buff"]
            if buff[0] == 1:
                b_strenght = b_strenght * buff[1]
            if buff[0] == 2:
                b_dexterity = b_dexterity * buff[1]
            if buff[0] == 3:
                b_defense = b_defense * buff[1]
    e_type = battle.get("e_type")
    skills = battle.get("skills")
    xp_on_kill = battle.get("xp_on_kill")
    uXp = battle.get("uXp")
    while enemy_fight.stat("health") > 0:
        health_bonus = 0
        Character.activity = "battle"
        enemy_attack = math.floor(enemy_fight.attack(b_defense, b_dexterity))
        character_attack = math.floor(Character.attack(b_strenght))
        wait = input("\n[A] ttack   -   [S] kill   -   [R]un \n")
        if wait == "A" or wait == "a":
            pass
        elif wait == "S" or wait == "s":
            if not skills:
                print("You have no available skills...\nUsed normal attack:")
            else:
                y = 0
                items = []
                for x in skills:
                    items.append(x)
                    print(str(y) + ". " + x["item"] + ": "  + x["desc"])
                    y = y + 1
                while True:
                    s = input("Skill <num>\n")
                    try:
                        if int(s) <= y and int(s) > -1:
                            s = items[int(s)]
                            print("\n" + s["msg"] + "\n")
                            skills.remove(s)
                            character_attack = math.floor(character_attack * s["SD"][0])
                            health_bonus = math.floor(character_attack * s["SD"][1])
                            health_bonus = health_bonus * -1
                            h = health_bonus
                            if not s["SD"][2] == 0:
                                pass
                            if not s["SD"][3][0] == 0:
                                if s["SD"][3][0] == 1:
                                    b_strenght = b_strenght * s["SD"][3][1]
                                if s["SD"][3][0] == 2:
                                    b_dexterity = b_dexterity * s["SD"][3][1]
                                if s["SD"][3][0] == 3:
                                    b_defense = b_defense * s["SD"][3][1]
                            while h > 0:
                                if Character.health < Character.maxhealth:
                                    Character.health = Character.health + 1
                                    h = h - 1
                                else:
                                    break
                            break
                        else:
                            print("Invalid skill")
                    except: print("Invalid input")
        elif wait == "R" or wait == "r":
            if e_type == "boss":
                print("Can't run from a boss!")
            else:
                if random.randint(0, 3)  == 0:
                    print("\nYou ran from", enemy_fight.stat("type"))
                    break
                else:
                    print("You failed to run...")
                    Character.change_stat(health = enemy_attack)
                    p_healthChange = enemy_attack
                    Character_attack = 0
                    print("YOUR HEALTH: " + str(Character.stat("health")) + "(" + str(p_healthChange) + ") | ENEMY HEALTH: ", str(enemy_fight.stat("health")) + "(" + str(character_attack) + ")")
        if not wait == "R" or wait == "r":
            #Fighting code:    
            enemy_check = enemy_fight.stat("health") + character_attack
            if Character.e_pet:
                pet_dmg = math.floor(random.randint(7, 11) / 10 * Character.e_pet["dmg"] * Character.e_pet["level"])
                enemy_check = enemy_check - pet_dmg
            p_healthChange = enemy_attack + health_bonus
            
            enemy_fight.get_damage(character_attack)
            if enemy_fight.health < 0:
                enemy_fight.health = 0
            if enemy_check > 0:
                Character.change_stat(health = enemy_attack)
                if Character.health < 0:
                    Character.health = 0
                if (character_attack * -1) > Character.dmg_record:
                    Character.dmg_record = character_attack * -1
                    print(space + "\nNEW DAMAGE RECORD " + str(character_attack * -1) + " DAMAGE\n" + space)
                print("You dealt", str(character_attack * -1), "damage")
                eg_dmg = character_attack * -1
                if Character.e_pet:
                    eg_dmg = eg_dmg + pet_dmg
                    if Character.e_pet["nametag"]:
                        print("Pet " + Character.e_pet["nametag"] + " dealt " + str(pet_dmg) + " damage")
                    else:
                        print("Pet " + Character.e_pet["name"] + " dealt " + str(pet_dmg) + " damage")
                    enemy_fight.get_damage(pet_dmg * -1)
                eg_dmg = eg_dmg * -1
                print("Enemy", enemy_fight.stat("type"), "dealt", str(enemy_attack * -1), "damage")
                print("YOUR HEALTH: " + str(Character.stat("health")) + "(" + str(p_healthChange) + ") | ENEMY HEALTH: ", str(enemy_fight.stat("health")) + "(" + str(eg_dmg) + ")")
                print("\n" + space)
            else:
                if (character_attack * -1) > Character.dmg_record:
                    Character.dmg_record = character_attack * -1
                    print(space + "\nNEW DAMAGE RECORD " + str(character_attack * -1) + " DAMAGE\n" + space)
                print("You dealt", str(character_attack * -1), "damage\n")
                print("+ " + str(xp_on_kill) + " xp\n+ " + str(xp_on_kill * 2) + " Silver")
                Character.change_stat(xp = xp_on_kill)
                Character.silver = Character.silver + xp_on_kill * 2
                Character.t_level = Character.t_level + 1
                Character.pet_hatching(uXp, True)
                Character.change_stat(pet_xp = uXp)
                if e_type == "enemy":
                    if Character.t_level > 9:
                        Character.t_level = 1
                        Character.t_floor = Character.t_floor + 1
                        print("1 Floor down...")
                elif e_type == "boss":
                    Character.boss_day = time_yday
                    print(space, "You got a pet egg!", space)
                    Character.pet_eggs = Character.pet_eggs + 1
                    Character.check_egg()
                wait = input("Press ENTER to continue...")
                print("\n")
                lootbox()
                if e_type == "boss":
                    lootbox()
                    lootbox()
                break
        if Character.stat("health") <= 0:
            print("\nYOU DIED")
            Character.health = Character.maxhealth
            l_s = math.floor(Character.silver * 0.3)
            print("Lost " + str(l_s) + " Silver")
            Character.silver = Character.silver - l_s
            #print("Lost quest progress")
            #Add quests and lose progress of em
            break

def mines():
    print("Started mining!")
    mining = True
    depth = 0
    while mining:
        depth = depth + 1

def mine():
    if not Character.level > 9:
        pass
        #print("You need to be at least level 10 to enter the mines!")
        #return
    print(space + space + space + "\n                      ⛏️ THE MINES ⛏️\n" + space + space + space)
    while True:
        print("[E] nter Mine   [G] uide   [P] ickaxes   -   ENTER to exit")
        print("[S] tats")
        p_input = input()
        if p_input == "":
            return
        if p_input == "G" or p_input == "g":
            print("\nWelcome to the mines!\nIn one of the most dangerous but most rewarding areas\nof the game, you will need to find gemstone\nnodes while fighting off extraordinary enemeies\n\nIf you enter the mines, you WON'T be able to \nleave until you find an exit!\nBe ready, explorer!")
        elif p_input == "E" or p_input == "e":
            mines()
        elif p_input == "S" or p_input == "s":
            print(f"\n{Character.name}'s Mining Stats:")
            print(f"Iron: {Character.iron}\nGold: {Character.gold}")
            print(f"Green Gems: {Character.g_gems}\nBlue Gems: {Character.b_gems}\nRed Gems: {Character.r_gems}")
            print(f"Refined Green Gems: {Character.rg_gems}\nRefined Blue Gems: {Character.rb_gems}\nRefined Red Gems: {Character.rr_gems}")
            print(f"Clean Gems: {Character.c_gems}\nRefined Clean Gems: {Character.rc_gems}\n")
            wait = input("Press ENTER to continue...")
        
def collections():
    print("Collections:")
    swords = []
    shields = []
    armor = []
    pets = list(pet.keys()) 
    for x in gear:
        if gear[x]["type"] == "sword":
            swords.append(x)
        if gear[x]["type"] == "shield":
            shields.append(x)
        if gear[x]["type"] == "armor":
            armor.append(x)     
    owned_swords = []
    owned_shields = []
    owned_armor = []
    owned_pets = list(Character.pets.keys())
    for x in Character.gear:
        if gear[x]["type"] == "sword":
            owned_swords.append(x)
        if gear[x]["type"] == "shield":
            owned_shields.append(x)
        if gear[x]["type"] == "armor":
            owned_armor.append(x)
    perc_swords = int(len(owned_swords) / len(swords)* 100)
    perc_shields = int(len(owned_shields) / len(shields) * 100)
    perc_armor = int(len(owned_armor) / len(armor) * 100)
    perc_pets = int(len(owned_pets) / len(pets) * 100)
    swords_bar = ""
    shields_bar = ""
    armor_bar = ""
    pets_bar = ""
    for x in range(0, 101, 5):
        if perc_swords > x:
            swords_bar = swords_bar + "#"
    while len(swords_bar) < 20:
        swords_bar = swords_bar + "-"
    for x in range(0, 101, 5):
        if perc_shields > x:
            shields_bar = shields_bar + "#"
    while len(shields_bar) < 20:
        shields_bar = shields_bar + "-"
    for x in range(0, 101, 5):
        if perc_armor > x:
            armor_bar = armor_bar + "#"
    while len(armor_bar) < 20:
        armor_bar = armor_bar + "-"
    for x in range(0, 101, 5):
        if perc_pets > x:
            pets_bar = pets_bar + "#"
    while len(pets_bar) < 20:
        pets_bar = pets_bar + "-"
    print("Swords:   " + swords_bar + "  - " + str(len(owned_swords)) + "/" + str(len(swords)))
    print("Shields:  " + shields_bar + "  - " + str(len(owned_shields)) + "/" + str(len(shields)))
    print("Armor:    " + armor_bar + "  - " + str(len(owned_armor)) + "/" + str(len(armor)))
    print("Pets:     " + pets_bar + "  - " + str(len(owned_pets)) + "/" + str(len(pets)))
    wait = input("\nPress ENTER to continue")
    
#Lootbox opening
def lootbox():
    commons = []
    rares = []
    epics = []
    legendarys = []
    for x in gear:
        item = gear[x]
        if item["rarity"] == "common":
            commons.append(item["name"])
        elif item["rarity"] == "rare":
            rares.append(item["name"])
        elif item["rarity"] == "epic":
            epics.append(item["name"])
        elif item["rarity"] == "legendary":
            legendarys.append(item["name"])
    for x in range(3):
        n = random.randint(1, 100)
        if n > drop_chances["legendary"]:
            n = random.randint(0, (len(legendarys) -1))
            r = "Legendary"
            item_name = legendarys[n]
        elif n > drop_chances["epic"]:
            n = random.randint(0, (len(epics) -1))
            item_name = epics[n]
            r = "Epic"
        elif n > drop_chances["rare"]:
            n = random.randint(0, (len(rares) -1))
            item_name = rares[n]
            r = "Rare"
        else:
            n = random.randint(0, (len(commons) -1))
            item_name = commons[n]
            r = "Common"
        if x < 2:
            text = "Spinning...: " + r + " " + item_name + " -  Press ENTER"
            wait = input(text)
    print(space, "\nYou dropped a", r, item_name, "!\n")
    Character.additem(item_name)

def inventory():
    Character.activity = "inventory"
    e_sword = Character.stat("e_sword")
    try: equipped_s = e_sword["name"]
    except: equipped_s = ""
    try: equipped_sh = Character.e_shield["name"]
    except: equipped_sh = ""
    try: equipped_a = Character.e_armor["name"]
    except: equipped_a = ""
    print("--- Inventory ---\n")
    print("Sword/bow: ", equipped_s)
    print("Shield:    ", equipped_sh)
    print("Armor:     ", equipped_a, "\n")
    gear = Character.stat("gear")
    swords = []
    y = 0
    pSword = []
    print("Swords/Bows:")
    for x in gear:
        if gear[x]["type"] == "sword":
            swords.append(x)
            st = gear[x]["strenght"]
            dex = gear[x]["dexterity"]
            de = gear[x]["defense"]
            print(str(y) + ". " + gear[x]["rarity"].capitalize() + " " + str(x) + "   =   Strenght: " + str(st) + " - Defense: " + str(de) + " - Dexterity: " + str(dex))
            if gear:
                if gear[x]:
                    if gear[x]["skill"]:
                        print("   -Skill: " + gear[x]["skill_d"]["desc"])
            y = y + 1
    shields = []
    print("Shields:")
    for x in gear:
        if gear[x]["type"] == "shield":
            shields.append(x)
            st = gear[x]["strenght"]
            dex = gear[x]["dexterity"]
            de = gear[x]["defense"]
            print(str(y) + ". " + gear[x]["rarity"].capitalize() + " " + str(x) + "   =   Strenght: " + str(st) + " - Defense: " + str(de) + " - Dexterity: " + str(dex))
            if gear:
                if gear[x]:
                    if gear[x]["skill"]:
                        print("   -Skill: " + gear[x]["skill_d"]["desc"])
            y = y + 1
    armor = []
    print("Armor:")
    for x in gear:
        if gear[x]["type"] == "armor":
            armor.append(x)
            st = gear[x]["strenght"]
            dex = gear[x]["dexterity"]
            de = gear[x]["defense"]
            print(str(y) + ". " + gear[x]["rarity"].capitalize() + " " + str(x) + "   =   Strenght: " + str(st) + " - Defense: " + str(de) + " - Dexterity: " + str(dex))
            if gear:
                if gear[x]:
                    if gear[x]["skill"]:
                        print("   -Skill: " + gear[x]["skill_d"]["desc"])
            y = y + 1
    all_gear = []
    for x in swords:
        all_gear.append(x)
    for x in shields:
        all_gear.append(x)
    for x in armor:
        all_gear.append(x)
    print("E <num> to equip   -   ENTER to exit")
    p_input = input()
    if p_input != "":
        if p_input[0] == "E" or p_input[0] == "e":
            try:
                select = all_gear[int(p_input[1:])]
                if gear[select]["type"] == "sword":
                    Character.change_stat(e_sword = gear[select])
                    print("Equipped Sword/Bow:", select)
                if gear[select]["type"] == "shield":
                    Character.e_shield = gear[select]
                    print("Equipped Shield:", select)
                if gear[select]["type"] == "armor":
                    Character.e_armor = gear[select]
                    print("Equipped Armor:", select)
                wait = input("\nPress ENTER to Continue\n")
            except:
                print("Invalid input")
                inventory()
        elif p_input[0]  == "E" or p_input[0] == "e":
            pass
    elif p_input != "S" and p_input != "s":
        pass

def dungeon():
    print(space + space + space + "\n                   -<= DUNGEON MENU =>-                    \n" + space + space + space)
    while True:
        print("[D] ungeon Master    [E] nter Dungeon   -   ENTER to exit")
        print("[S] tats             [T] he mines")
        p_input = input()
        if p_input == "":
            break
        elif p_input == "D" or p_input == "d":
            print("Quests:")
        elif p_input == "S" or p_input == "s":
            print("\nYour Dungeon Stats:")
            wait = input("Press ENTER to continue...")
        elif p_input == "T" or p_input == "t":
            wait = mine()

def daily_boss():
    if Character.boss_day == time_yday:
        print("You already killed your daily boss!")
        return
    global enemy_fight
    b_strenght = 1
    b_dexterity = 1
    b_defense = 1
    skills = Character.L_skills()
    n = random.randint(0, (len(boss_keys) - 1))
    enemy_type = bosses[boss_keys[n]]
    enemy_fight = Enemy(boss_keys[n], Character.level*enemy_type["strenght"], Character.level*enemy_type["health"], Character.level*enemy_type["defense"], Character.level*enemy_type["dexterity"], math.floor(enemy_type["xp"]*0.5*Character.level))
    xp_on_kill = math.floor(enemy_type["xp"] * Character.level * 0.5)
    uXp = enemy_type["xp"]
    name = boss_keys[n]
    print("\n---   DAILY BOSS   ---")
    print(enemy_type["s_msg"])
    print(f"The boss {name} looks angry at you....")
    fight(b_defense = b_defense, b_dexterity = b_dexterity, b_strenght = b_strenght, skills = skills, xp_on_kill = xp_on_kill, e_type = "boss", uXp = uXp)

def tower():
    global enemy_fight
    b_strenght = 1
    b_dexterity = 1
    b_defense = 1
    skills = Character.L_skills()
    
    floor = Character.t_floor
    level = Character.t_level

    floor_mult = math.floor(2 ** (floor - 1))
    multiplier = round(((1 + (level * 0.1)) * floor_mult), 1) #Times 2 for each floor, +10% every level. So for floor 1 level 1 1.1x and floor 2 level 3 2.6x
    xp_mult = multiplier * 0.5
    print("-== THE TOWER ==-\nFLOOR " + str(floor) + " | LEVEL " + str(level) + " (x" + str(multiplier) + ")")
    
    n = random.randint(0, (len(enemy_keys) - 1))
    enemy_type = enemies[enemy_keys[n]]
    enemy_fight = Enemy(enemy_keys[n], multiplier*enemy_type["strenght"], multiplier*enemy_type["health"], multiplier*enemy_type["defense"], multiplier*enemy_type["dexterity"], xp_mult*enemy_type["xp"])
    
    print("\nA", enemy_keys[n], "appears. \n")

    xp_on_kill = enemy_type["xp"]

    fight(b_defense = b_defense, b_dexterity = b_dexterity, b_strenght = b_strenght, skills = skills, xp_on_kill = xp_on_kill, e_type = "enemy", uXp = xp_on_kill)
        
def healing():
    print("\nWelcome to the House of Healing! \nYou can regenerate 1HP every 1 second here.")
    while True:
        Character.activity = "healing"
        check = input("Press ENTER to Heal...")
        if check == "":
            pass
        else:
            break
        if not Character.stat("health") >= Character.stat("maxhealth"):
            Character.change_stat(health = 1)
            print("Health: ", Character.stat("health"), "/", Character.stat("maxhealth"))
            time.sleep(1)
        else:
            print("Full health!")
            break
    
def load_Character():
    global Character
    save_dir = os.path.dirname(os.path.realpath(__file__))
    characters = []
    for x in os.listdir(save_dir):
        if x.endswith(".json"):
            characters.append(x)
    if len(characters) > 0:
        print("Characters:")
        for y in range(len(characters)):
            filename = characters[y]
            character_name, ext = os.path.splitext(filename)
            print(str(y) + ". " + character_name)
        print(space)
        character = input("Load Character <num>   -   [D] elete Character   -   [N] ew Character\n")
        if character == "d" or character == "D":
            which = input("Character <num>")
            try:
                print(characters[int(which)])
                os.remove(characters[int(which)])
                character_name, ext = os.path.splitext(characters[int(which)])
                print("Deleted Character", character_name)
                load_Character()
                return
            except:
                print("Invalid Character")
                load_Character()
                return
        if character.isdigit():
        #Try:
            character_name, etc = os.path.splitext(characters[int(character)])
            print("Loading character " + character_name + "...")
            file_name = characters[int(character)]
            size = os.path.getsize(file_name)
            with open(file_name, "rb") as f:
                data = f.read()            
            data = e.decrypt(data)
            Character = Player(data["name"])
            Character.load(data)
        else:
            name = input("Name your character:\n")
            Character = Player(name)
    else:
        name = input("Name your character:\n")
        Character = Player(name)
    print("\n")

def shop():
    while True:
        print("\n--- Shop ---\nBuy items here with silver collected from killing enemies\n")
        #Not finished yet
        break

def main():
    while True:
        Character.activity = "menu"
        Character.update()
        print("--- Tower RPG Menu ---")
        print("[T] ower         [S] tats          [H] Healing       [Q] uit")
        print("[I] nventory     [F] riend         [B] uy Item       [C] ollections")
        print("[D] Daily boss   [P] ets           [M] Dungeon Menu")
        player_input = input()
        if player_input == "T" or player_input == "t":
            wait = tower()
        elif player_input == "S" or player_input == "s":
            Character.stats()
        elif player_input == "H" or player_input == "h":
            wait = healing()
        elif player_input == "i" or player_input == "I":
            wait = inventory()
        elif player_input == "F" or player_input == "f":
            wait = multiplayer()
        elif player_input == "M" or player_input == "m":
            wait = dungeon()
        elif player_input == "B" or player_input == "b":
            wait = shop()
        elif player_input == "C" or player_input == "c":
            wait = collections()
        elif player_input == "D" or player_input == "d":
            wait = daily_boss()
        elif player_input == "P" or player_input == "p":
            wait = pet_menu()
        elif player_input == "Q" or player_input == "q":
            print("\n")
            Character.save()
            print("Saved and exiting...")
            break
        
time_yday = time.gmtime(time.time())[7]
load_Character()

if __name__ == "__main__":
    mult = threading.Thread(target=m_handler, daemon=True)
    mult.start()
    auto_save_thread = threading.Thread(target=auto_actions, daemon=True).start()
    main()
