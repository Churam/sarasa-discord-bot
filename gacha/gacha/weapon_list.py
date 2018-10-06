import json
from random import randrange
from random import choice
#Dictionnary containing the SSR Weapons
SSR_weps = {}
SSR_weps["Dainsleif"] = "Altaïr"
SSR_weps["Lohengrin"] = "Percival"
SSR_weps["Claíomh Solais"] = "Charlotta"
SSR_weps["Nagelring"] = "Izmir"
SSR_weps["Ascalon"] = "Siegfried"
SSR_weps["Greatsword Andalius"] = "Aletheia"
SSR_weps["Yyrkoon"] = "Yuisis"
SSR_weps["Caladbolg"] = "Jeanne D'Arc (Light)"
SSR_weps["Ethereal Lasher"] = "Ferry (SSR)"
SSR_weps["Hauteclaire"] = "Albert"
SSR_weps["Hrotti"] = "Seruel"
SSR_weps["Disparia"] = "Jeanne D'Arc (Dark)"
SSR_weps["Gram"] = "Beatrix"
SSR_weps["Lyst Sin"] = "Vira"
SSR_weps["Mistilteinn"] = "Vaseraga"
SSR_weps["Hoarfrost Blade Persius"] = "Lancelot"
SSR_weps["Phantom Thief Blade"] = "Chat Noir"
SSR_weps["Arsene"] = "Catherine"
SSR_weps["Heaven's Cloud"] = "Petra"
SSR_weps["Thunder Dirk Jove"] = "Agielba"
SSR_weps["Twin Helix"] = "Rosamia (SSR)"
SSR_weps["Azoth"] = "Vania"
SSR_weps["Bloody Scar"] = "Veight"
SSR_weps["Brionac"] = "Zeta (Fire)"
SSR_weps["Luin"] = "Heles"
SSR_weps["Pilum"] = "Nezahualpilli"
SSR_weps["Gae Derg"] = "Razia"
SSR_weps["Gargantua"]= "Arulumaya"
SSR_weps["Turpin Spear"]= "Carmelina"
SSR_weps["Skyrend Spear"]= "Forte"
SSR_weps["Sunspot Spear"]= "Zeta (Dark)"
SSR_weps["Scarlet Crest Axe"]= "Yuel"
SSR_weps["Way Flyer"]= "Aoidos"
SSR_weps["Blossom Axe"]= "Vane (SSR)"
SSR_weps["Mettle"]= "Nemone"
SSR_weps["Split End"]= "Melissabelle"
SSR_weps["Windflash"]= "Gawain"
SSR_weps["Ukonvasara"]= "Lady Grey"
SSR_weps["Soul Eater"]= "Hallessena"
SSR_weps["Vassago"]= "Melleau"
SSR_weps["Forbidden Inferno"]= "Anthuria"
SSR_weps["Illusion Scepter"]= "Magisa"
SSR_weps["Starblaze Rings"]= "Zahlhamelina"
SSR_weps["Ice Crystal Staff"]= "Lily"
SSR_weps["Montague's Oath"]= "Romeo"
SSR_weps["Ouroboros"]= "Cagliostro"
SSR_weps["Thyrsus"]= "De La Fille (Earth)"
SSR_weps["Kerykeion"]= "De La Fille (Light)"
SSR_weps["Wing of the Pure"]= "Korwa"
SSR_weps["Capulet's Oath"]= "Juliet"
SSR_weps["Sealed Claustrum"]= "Sarunan"
SSR_weps["Gridarvor"]= "Marquiares"
SSR_weps["Kalaurops"]= "Sarunan (Dark)"
SSR_weps["Meteora"]= "Yngwie"
SSR_weps["Vlisragna"]= "Silva"
SSR_weps["Stratomizer"]= "Eustace"
SSR_weps["Far Away"]= "Lennah"
SSR_weps["Blushing Blossom Pin"]= "Societte (Fire)"
SSR_weps["Brahma Gauntlet"]= "Ghandagoza"
SSR_weps["Magma Gauntlet"]= "Aliza"
SSR_weps["Metal Hand"]= "Lady Katapillar and Vira"
SSR_weps["Scarlet Vane"]= "Societte (Water)"
SSR_weps["Ancient Bandages"]= "Ayer"
SSR_weps["Coco n Mimi"]= "Cerberus"
SSR_weps["Roseate Aetherial Bow"]= "Metera (Fire)"
SSR_weps["Aetherial Bow"]= "Metera (Wind)"
SSR_weps["Heroic Bow"]= "Feena"
SSR_weps["Mobius Strip"]= "Clarisse"
SSR_weps["Melodic Sphere"]= "Lilele"
SSR_weps["Ocean Harp"]= "Sophia"
SSR_weps["Sandcastle Song-Lume"]= "Sara"
SSR_weps["Cords of Heaven Lillah"]= "Arriet"
SSR_weps["Venustas"]= "Narmaya"
SSR_weps["Dragon Slayer"]= "Amira"
SSR_weps["Fudo-Kuniyuki"]= "Yodarha"
SSR_weps["Fusion Mobius"]= "Clarisse (Light)"
SSR_weps["Deirdre's Claws"] = "Scathacha"
SSR_weps["Symbol of Justice"] = "Baotorda (SSR)"
SSR_weps["Bella Aeterna"] = "Yggdrasil"
SSR_weps["Draco Claw"] = "Grea (SSR)"
SSR_weps["Daemon's Spine"] = "Anne"
SSR_weps["Gothic Cutlery"] = "Dorothy and Claudia"
SSR_weps["Heiliges Schwert"] = "Lancelot (Wind)"
 
SSR_summs = []
SSR_summs.append("Athena")
SSR_summs.append("Prometheus")
SSR_summs.append("Satyr")
SSR_summs.append("Sethlans")
SSR_summs.append("Twin Elements")
SSR_summs.append("Ca Ong")
SSR_summs.append("Grani")
SSR_summs.append("Macula Marius")
SSR_summs.append("Neptune")
SSR_summs.append("Oceanus")
SSR_summs.append("Baal")
SSR_summs.append("Cybele")
SSR_summs.append("Gilgamesh")
SSR_summs.append("Medusa")
SSR_summs.append("Tezcatlipoca")
SSR_summs.append("Garuda")
SSR_summs.append("Morrigna")
SSR_summs.append("Nezha")
SSR_summs.append("Quetzalcoatl")
SSR_summs.append("Rose Queen")
SSR_summs.append("Setekh")
SSR_summs.append("Siren")
SSR_summs.append("Apollo")
SSR_summs.append("Hector")
SSR_summs.append("Odin")
SSR_summs.append("Thor")
SSR_summs.append("Vortex Dragon")
SSR_summs.append("Anubis")
SSR_summs.append("Dark Angel Olivia")
SSR_summs.append("Lich")
SSR_summs.append("Satan")
SSR_summs.append("Typhon")
SSR_summs.append("Bonito")
SSR_summs.append("Aphrodite")
SSR_summs.append("Garula, Shining Hawk")
SSR_summs.append("Zaoshen")
SSR_summs.append("Ankusha")
SSR_summs.append("Adramelech")


SSR_summs.append("Agni")
SSR_summs.append("Shiva")
SSR_summs.append("Kaguya")
SSR_summs.append("Varuna")
SSR_summs.append("Godsworn Alexiel")
SSR_summs.append("Titan")
SSR_summs.append("Zephyrus")
SSR_summs.append("Grand Order")
SSR_summs.append("Lucifer")
SSR_summs.append("Zeus")
SSR_summs.append("Hades")
SSR_summs.append("Bahamut")
SSR_summs.append("Europa")

#LEGFEST LIMITED, COMMENT IF NO LEGFEST

SSR_weps["Blutgang"] = "Black Knight"
# SSR_weps["AK-4A"] = "Eugen"
# SSR_weps["Gambanteinn"] = "Io (Grand)"
# SSR_weps["Murgleis"] = "Katalina (Grand)"
# SSR_weps["Reunion"] = "Lecia"
SSR_weps["Eden"] = "Lucio"
SSR_weps["Parazonium"] = "Orchid"
# SSR_weps["Benedia"] = "Rackam (Grand)"
# SSR_weps["Love Eternal"] = "Rosetta (Grand)"
SSR_weps["Ixaba"] = "Sturm"
SSR_weps["Blue Sphere"] = "Drang"
SSR_weps["Cute Ribbon"] = "Zooey (Summer)"
SSR_weps["Certificus"] = "Vira (Grand)
SSR_Weps["Fallen Sword"] = Olivia

# -------------------------------------- SR ---------------------------------------#

SR_chara_weps = {}
SR_chara_weps["Sword of Sorcery"] = "Owen"
SR_chara_weps["Arson Link"] = "Blazing Teacher Elmott"
SR_chara_weps["Ember Blade"]="Carren"
SR_chara_weps["Ram-Dao"]="Gayne"
SR_chara_weps["Tanzanite Sword Mikoh"]="Therese (Bunny)"
SR_chara_weps["Aquablade"]="Mina"
SR_chara_weps["Bottle o' Blossoms"]="Lamretta (Water)"
SR_chara_weps["Royal Rapier"]="Ange"
SR_chara_weps["Frying Pan"]="Yaia"
SR_chara_weps["Grand Edge"]="Herja (SR)"
SR_chara_weps["White Flag"]="Mimlemel and Stumpeye"
SR_chara_weps["True Teardrop"]="Vermeil (SR)"
SR_chara_weps["Lyst"]="Vira"
SR_chara_weps["Purity Blade"]="Lucius"
SR_chara_weps["Tilvung"]="Helnar"
SR_chara_weps["Soulbond Dirk"]="Teena"
SR_chara_weps["Shrike's Beak"]="Jamil"
SR_chara_weps["Sword of Lisblanc"]="Farrah (SR)"
SR_chara_weps["Soul Edge"]="Ferry (SR)"
SR_chara_weps["Puppet Knife"]="Danua"
SR_chara_weps["Scalpel"]="Shao"
SR_chara_weps["Wyrm Claw"]="Tanya (SR)"
SR_chara_weps["Flare Glaive"]="Mariah"
SR_chara_weps["Raging Halberd"]="Vane (SR)"
SR_chara_weps["Narval"]="Ulamnuran"
SR_chara_weps["Titanium Harpoon"]="Sig"
SR_chara_weps["Dreadflayer"]="Laguna"
SR_chara_weps["Giant Fork"]="Redluck"
SR_chara_weps["Golden Mop"]="Claudia"
SR_chara_weps["Massive Axe"]="Ryan (SR)"
SR_chara_weps["Fremel Hammer"]="Almeida"
SR_chara_weps["Great Hammer"]="Galadar (SR)"
SR_chara_weps["Cloud Tomahawk"]="Eso (SR)"
SR_chara_weps["Golden Woofer"]="Daetta (SR)"
SR_chara_weps["Voulge"]="Zaja"
SR_chara_weps["Arson"]="Elmott"
SR_chara_weps["Nature's Mystery"]="Dante"
SR_chara_weps["Soothing Torch"]="Rosamia (SR)"
SR_chara_weps["Witch's Broom"]="Anna"
SR_chara_weps["Ice Bough Staff"]="Erin"
SR_chara_weps["Spritewood Staff"]="Mishra"
SR_chara_weps["Zhonpeli"]="Lamretta (Earth)"
SR_chara_weps["Aerial Cane"]="Arusha"
SR_chara_weps["Flower Crown"]="Jasmine (SR)"
SR_chara_weps["Wind-Rhyme Staff"]="Noa"
SR_chara_weps["Sacred Codex"]="Johann"
SR_chara_weps["Cursed Cane"]="Will"
SR_chara_weps["Shadow Scepter"]="Goblin Mage"
SR_chara_weps["Dolphin"]="Cucuroux"
SR_chara_weps["Fire Piece"]="Mary (SR)"
SR_chara_weps["Colorful Crackerjack"]="Pengy"
SR_chara_weps["Quarrel"]="Sahli Lao"
SR_chara_weps["Handy Arquebus"]="Jessica"
SR_chara_weps["Standard Albion Bolt"]="Tyre"
SR_chara_weps["Hunter's Rifle"]="Ludmila"
SR_chara_weps["Chain Knuckles"]="Ezecrain"
SR_chara_weps["Crimson Talons"]="Sen"
SR_chara_weps["Cup and Saucer"]="Dorothy"
SR_chara_weps["Kaiser Knuckles"]="Alec"
SR_chara_weps["Impact Knuckles"]="Soriz"
SR_chara_weps["Metal Glove"]="Ladiva"
SR_chara_weps["Merciless Chastening"]="Hazen (SR)"
SR_chara_weps["Heavy Blast Knuckles"]="Feather (SR)"
SR_chara_weps["Misanga Bracelet"]="J.J."
SR_chara_weps["Tiger Fang"]="Mimlemel"
SR_chara_weps["Glass Bow"]="Sutera (Fire)"
SR_chara_weps["Ice Bow"]="Milleore"
SR_chara_weps["Sutera's Bow"]="Sutera"
SR_chara_weps["Aquarium Harp"]="Ejaeli"
SR_chara_weps["Songsmith's Harp"]="Elta"
SR_chara_weps["Stravaria"]="Keehar"
SR_chara_weps["Wandering Blade"]="Lucius"
SR_chara_weps["Zanbato"]="Sevilbarra"
SR_chara_weps["Cruel Claw"]="Predator"
SR_chara_weps["Holy Axe"] = "Sevastien"
SR_chara_weps["Arondight"] = "Baotorda"
SR_chara_weps["Brocken Lance"] = "Deliford"
SR_chara_weps["Lance d'Espoir"] = "Jeanne d'Arc (SR)"
SR_chara_weps["Katzbalger"] = "Jamil (Dark)"
SR_chara_weps["Slingshot"] = "Sarya"
SR_chara_weps["Unsigned Blade"] = "Mirin"
SR_chara_weps["Staff of the Star Seeker"] = "Sophia (SR)"



SR_weps = []
SR_weps.append("Fragarach")
SR_weps.append("Almace")
SR_weps.append("Ilhoon")
SR_weps.append("Twisted Dagger")
SR_weps.append("Mirage Knife")
SR_weps.append("Stiletto")
SR_weps.append("Fusetto")
SR_weps.append("Sword Breaker")
SR_weps.append("Trident")
SR_weps.append("Partisan")
SR_weps.append("Dragonfliar Cutter")
SR_weps.append("Shura Vhara")
SR_weps.append("Vajranda")
SR_weps.append("Bullova")
SR_weps.append("Shoka")
SR_weps.append("Horseman's Hammer")
SR_weps.append("Yagrush")
SR_weps.append("Pastoral Staff")
SR_weps.append("Holy Cane")
SR_weps.append("Dragon Tail")
SR_weps.append("Wheellock Axe")
SR_weps.append("Crosswind")
SR_weps.append("Snaphance")
SR_weps.append("Swallowtail")
SR_weps.append("Mauler")
SR_weps.append("Neko Punch")
SR_weps.append("Jamadhar")
SR_weps.append("Imperial Bow")
SR_weps.append("Sarnga")
SR_weps.append("Aves")
SR_weps.append("Elfin Bow")
SR_weps.append("Shadow Bow")
SR_weps.append("Athanasius")
SR_weps.append("Iron Tiger")
SR_weps.append("Fluorithium Blade")
SR_weps.append("Sauria")


SR_summs = []
SR_summs.append("Garnet Carbuncle")
SR_summs.append("Hellhound")
SR_summs.append("Hydra")
SR_summs.append("Vrazarek Firewyrm")
SR_summs.append("Angelie Cascade")
SR_summs.append("Aquamarine Carbuncle")
SR_summs.append("Wilinus Icewyrm")
SR_summs.append("Clay Golem")
SR_summs.append("Doomworm")
SR_summs.append("Golem")
SR_summs.append("Myconid")
SR_summs.append("Ruination Gargoyle")
SR_summs.append("Zircon Carbuncle")
SR_summs.append("Elmenhilde Windsprite")
SR_summs.append("Elusious Windwyrm")
SR_summs.append("Griffin")
SR_summs.append("Wyvern")
SR_summs.append("Opal Carbuncle")
SR_summs.append("Pixie")
SR_summs.append("Onyx Carbuncle")


#--------------------------------------R--------------------------------------#

R_chara_weps = {}
R_chara_weps["Fire Sword"]="Farrah"
R_chara_weps["Vintage Flat Iron"]="Rosine"
R_chara_weps["Shrimp Lure"]="Yodarha"
R_chara_weps["White Sword"]="Bridgette"
R_chara_weps["Heavy Metal Comb"]="La Coiffe"
R_chara_weps["Two-Handed Sword"]="Herja"
R_chara_weps["Xiphos"]="Volenna"
R_chara_weps["Lightbringer"]="Stan"
R_chara_weps["Old Sword"]="Krugne"
R_chara_weps["Paper Fan"]="Karteira"
R_chara_weps["Practice Sword"]="Thelonim"
R_chara_weps["Blue Crest"]="Cordelia"
R_chara_weps["Prism Tear"]="Vermeil"
R_chara_weps["Thunder Rapier"]="Rosamia (R)"
R_chara_weps["Dark Sword"]="Leonora"
R_chara_weps["Broken Bottle"]="Lamretta (R)"
R_chara_weps["Little Scarlet"]="Drusilla"
R_chara_weps["Mandau"]="Zehek"
R_chara_weps["Bloody Piercer"]="Tanya"
R_chara_weps["Switchblade"]="Lowain"
R_chara_weps["Silver Pole"]="Joel"
R_chara_weps["Ghillie Fork"]="Elmelaura"
R_chara_weps["Night Horn"]="Deliford"
R_chara_weps["Iron Pliers"]="Viceroy"
R_chara_weps["Soldier Axe"]="Ryan"
R_chara_weps["Draph Hammer"]="Galadar"
R_chara_weps["Sky Tomahawk"]="Eso"
R_chara_weps["Morning Star"]="Daetta"
R_chara_weps["Forest Hermit Staff"]="Dante"
R_chara_weps["Rubia Rod"]="Camieux (Earth)"
R_chara_weps["Torch"]="Camieux"
R_chara_weps["Snowman Rod"]="Suframare"
R_chara_weps["Student Notebook"]="Alistair"
R_chara_weps["Stone Pole"]="Norcel"
R_chara_weps["Taiaha"]="Jasmine"
R_chara_weps["Feather Wand"]="Anna"
R_chara_weps["Moss Tree Staff"]="Petra (R)"
R_chara_weps["Light Staff"]="Philosophia"
R_chara_weps["The Cross"]="Will"
R_chara_weps["Derringer"]="Barawa"
R_chara_weps["Flame Bolt"]="Karva"
R_chara_weps["Sawed-Off Shotgun"]="Garma"
R_chara_weps["Self Defender"]="Richard"
R_chara_weps["Petronel"]="Mary"
R_chara_weps["Chopsticks"]="Ippatsu"
R_chara_weps["Boogie Plates"]="Cailana"
R_chara_weps["Oven Mitts"]="Nene"
R_chara_weps["Tattoo Fist"]="Randall"
R_chara_weps["Iron Guard"]="Balurga"
R_chara_weps["Mythril Knuckles"]="Hazen"
R_chara_weps["Tonfa"]="Vanzza"
R_chara_weps["Enchanted Nail"]="Chloe"
R_chara_weps["Light Buckler"]="Pavidus"
R_chara_weps["Blast Knuckles"]="Feather (R)"
R_chara_weps["Flame Bow"]="Flesselles"
R_chara_weps["Bronze Bell"]="Bakura"
R_chara_weps["Night Bell"]="Lunalu"

R_weps = []
R_weps.append("Anelace")
R_weps.append("Claymore")
R_weps.append("Falchion")
R_weps.append("Flame Rapier")
R_weps.append("Ice Sword")
R_weps.append("Icey Nail")
R_weps.append("Earth Cutlass")
R_weps.append("Fire Baselard")
R_weps.append("Kila")
R_weps.append("Mailbreaker")
R_weps.append("Water Kukri")
R_weps.append("Kris")
R_weps.append("Emerald Dagger")
R_weps.append("Leaf Dagger")
R_weps.append("Holy Kris")
R_weps.append("Assassin's Dagger")
R_weps.append("Dark Knife")
R_weps.append("Couse")
R_weps.append("Fire Glaive")
R_weps.append("Flame Halberd")
R_weps.append("Langdebeve")
R_weps.append("Aquan Killer")
R_weps.append("Earth Halberd")
R_weps.append("Halberd")
R_weps.append("Harvester")
R_weps.append("Battle Axe")
R_weps.append("Earth Zaghnal")
R_weps.append("Rock Hammer")
R_weps.append("Wind Axe")
R_weps.append("Tabar")
R_weps.append("Thunder Kalinga Axe")
R_weps.append("Neckchopper")
R_weps.append("Cane")
R_weps.append("Ocean Rod")
R_weps.append("Water Rod")
R_weps.append("Feather Staff")
R_weps.append("Emerald Cane")
R_weps.append("Wind Rod")
R_weps.append("Shareeravadi")
R_weps.append("Evil Wand")
R_weps.append("Grenade")
R_weps.append("Matchlock")
R_weps.append("Straight Anchor")
R_weps.append("Ranger Pistol")
R_weps.append("Hand Pistol")
R_weps.append("Jezail")
R_weps.append("Fireball")
R_weps.append("Heated Pata")
R_weps.append("Pata")
R_weps.append("Fish Tooth")
R_weps.append("Gauntlet")
R_weps.append("Tidal Wraps")
R_weps.append("Rock Cutter")
R_weps.append("Mythril Baghnakhs")
R_weps.append("Whirlwind Wraps")
R_weps.append("Composite Bow")
R_weps.append("Longbow")
R_weps.append("Mythril Bow")
R_weps.append("Earth Bow")
R_weps.append("Power Bow")
R_weps.append("War Bow")
R_weps.append("Wrapped Bow")
R_weps.append("Lyre of Lamia")
R_weps.append("Nodachi")
R_weps.append("Mythril Katana")

R_summs = []
R_summs.append("Minotaur")
R_summs.append("Twilight Devil")
R_summs.append("Venom Lancer")
R_summs.append("Walking Torch")
R_summs.append("Angelie")
R_summs.append("Crusher")
R_summs.append("Jawfish")
R_summs.append("Purgatorian")
R_summs.append("Rivacuda")
R_summs.append("Slime")
R_summs.append("Swordshark")
R_summs.append("Bonethorn")
R_summs.append("Crawler")
R_summs.append("Lumacie Griffin")
R_summs.append("Mandrake")
R_summs.append("Sleepyhead")
R_summs.append("Belle")
R_summs.append("Dragonflair")
R_summs.append("Hornbird")
R_summs.append("Rodfly")
R_summs.append("Ghost Light")
R_summs.append("Cave Bat")
R_summs.append("Imp")
R_summs.append("Skeleton")


SSR_weps_nb = len(SSR_weps)
SSR_weps_list = list(SSR_weps.keys())
SSR_summs_nb = len(SSR_summs)
SSR_summs_nb = len(SSR_summs)
SR_chara_weps_nb = len(SR_chara_weps)
SR_chara_weps_list = list(SR_chara_weps.keys())
SR_weps_nb = len(SR_weps)
SR_summs_nb = len(SR_summs)
R_chara_weps_nb = len(R_chara_weps)
R_chara_weps_list = list(R_chara_weps.keys())
R_weps_nb = len(R_weps)
R_summs_nb = len(R_summs)

