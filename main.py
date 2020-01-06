# del enemies[enemy]
# name.relace(" ", "")

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create white magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")

# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},
                {"item": grenade, "quantity": 5}]

player1 = Person("Valos ", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick  ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot ", 3089, 174, 288, 34, player_spells, player_items)
players = [player1, player2, player3]

enemy1 = Person("Imp   ", 1250, 130, 560, 325, [], [])
enemy2 = Person("Magus ", 11200, 701, 525, 25, [], [])
enemy3 = Person("Imp   ", 1250, 130, 560, 325, [], [])
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD, "AN ENEMY ATTACK!" + bcolors.ENDC)

def attack_enemy(enemy, dmg, s):
    enemies[enemy].take_damage(dmg)
    print(s)

    if enemies[enemy].get_hp() == 0:
        print(enemies[enemy].name + " has died.")
        del enemies[enemy]

while running:

    # HP bar
    print("==============================")
    print("\n")
    print("NAME                   HP                                   MP")

    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    # Player attack phase
    for player in players:
        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            attack_enemy(enemy, dmg, "You attacked " + enemies[enemy].name.replace(" ", "") + " for " + str(dmg) + " points of damage.")

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1

            if magic_choice < 0:
                continue

            if magic_choice >= len(player.magic):
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            cost = spell.cost

            current_mp = player.get_mp()

            if cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                # back to choose action
                continue

            player.reduce_mp(cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                attack_enemy(enemy, magic_dmg, bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to " + enemies[enemy].name.replace(" ", "") + "." + bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice < 0:
                continue

            if item_choice >= len(player.items):
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for ", str(item.prop), "HP." + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP." + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                attack_enemy(enemy, item.prop, bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to " + enemies[enemy].name.replace(" ", "") + "." + bcolors.ENDC)

    # Check if battle is over
    defeated_enemies = defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check winner
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:
        print(bcolors.FAIL + "You lose!" + bcolors.ENDC)
        running = False

    # Enemy attack phase
    for enemy in enemies:
        target = random.randrange(0, 3)
        enemy_dmg = enemy.generate_damage()

        players[target].take_damage(enemy_dmg)
        print(enemy.name.replace(" ", "") +" attacks ", players[target].name.replace(" ", ""), "for", enemy_dmg)