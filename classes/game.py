# CONSTRUCTOR, PRIVATE, PUBLIC, PROTECTED

import random
from .magic import Spell

# color code
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'       #RED
    ENDC = '\033[0m'        #END OF STRING STYLE
    BOLD = '\033[1m'        #BOLD
    UNDERLINE = '\033[4m'

class Person:
    # CONSTRUCTOR
    # self = this.
    # PRIVATE attribute, need to use getter (__)
    # PROTECTED attribute (_)
    # PUBLIC attribute ( )
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atk = atk
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    # choose an action: Attack or Magic
    def choose_action(self):
        i = 1
        print("\n" + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "ACTIONS:" + bcolors.ENDC)
        for item in self.actions:
            print("     "  + str(i) + ".", item)
            i += 1

    # Attack: normal attack with dmg random
    def generate_damage(self):
        atkl = self.atk - 10
        atkh = self.atk + 10
        return random.randrange(atkl, atkh)

    # Magic: choose magic
    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            print("     "  + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    # magic attack cost
    def reduce_mp(self, cost):
        self.mp -= cost

    # Item: choose item
    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("     "  + str(i) + ".", item["item"].name, ":", item["item"].description, "(x"+str(item["quantity"]) +")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "TARGET" + bcolors.ENDC)
        for enemy in enemies:
            print("   " + str(i) + "." + enemy.name)
            i += 1
        choice = int(input("Choose target: ")) - 1
        return choice

    # Defend, reduce hp
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, hp):
        self.hp += hp
        if(self.hp > self.maxhp):
            self.hp = self.maxhp

    # Getter
    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

     # Draw HP, MP bar
    def do_bar(self, p, maxp, num):
        bar = ""
        bar_sticks = (p / maxp) * num  # 25 case in life hp_bar

        while bar_sticks > 0:
            bar += "█"
            bar_sticks -= 1

        while len(bar) < num:
            bar += " "
        return bar

    def do_string(self, p, maxp, num):
        string = str(p) + "/" + str(maxp)
        current = ""

        if len(string) < num:
            decreased = num - len(string)
            while decreased > 0:
                current += " "
                decreased -= 1

            current += string
        else:
            current = string
        return current

    def get_stats(self):
        hp_bar = self.do_bar(self.hp, self.maxhp, 25)
        mp_bar = self.do_bar(self.mp, self.maxmp, 10)

        current_hp = self.do_string(self.hp, self.maxhp, 9)
        current_mp = self.do_string(self.mp, self.maxmp, 7)

        print("                       _________________________            __________ ")
        print(bcolors.BOLD + self.name
              + "      " + current_hp + " |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC
              + bcolors.BOLD + "|  " + current_mp + " |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    def get_enemy_stats(self):
        hp_bar = self.do_bar(self.hp, self.maxhp, 47)
        current_hp = self.do_string(self.hp, self.maxhp, 11)

        print("                       _______________________________________________ ")
        print(bcolors.BOLD + self.name
              + "    " + current_hp + " |" + bcolors.FAIL + hp_bar + bcolors.ENDC + "|")