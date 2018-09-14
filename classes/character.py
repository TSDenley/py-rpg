import random
from colorama import init
from termcolor import colored, cprint
init()

indt = '    '

class Character:
    def __init__(self, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atk = atk
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = [ 'Attack', 'Magic', 'Items' ]

    def generate_damage(self):
        return random.randrange(self.atk - 10, self.atk + 10)

    def take_damage(self, dmg):
        self.hp -= dmg
        print('...' + colored(str(dmg), 'red', attrs=['bold']) + ' damage!')

    def reduce_mp(self, cost):
        self.mp -= cost
        if self.mp < 0:
            self.mp = 0

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        print('...recovered ' + colored(str(dmg), 'blue', attrs=['bold']) + ' HP!')

    def heal_mp(self, dmg):
        self.mp += dmg
        if self.mp > self.maxmp:
            self.mp = self.maxmp
        print('...recovered ' + colored(str(dmg), 'blue', attrs=['bold']) + ' MP!')

    def choose_action(self):
        i = 1
        for action in self.actions:
            # Skip magic is character has no spells
            if action == 'Magic' and len(self.magic) < 1:
                continue
            # Skip items if character has no items
            if action == 'Items' and len(self.items) < 1:
                continue
            print(indt + str(i) + '.', action)
            i += 1
        print(indt + '(exit)')

    def choose_spell(self):
        print('\n' + colored('Magic', 'blue', attrs=['bold']))
        i = 1
        for spell in self.magic:
            print(indt + str(i) + '.', spell.name, '(cost:', str(spell.cost) + ')')
            i += 1
        print(indt + '(back)')

    def choose_item(self):
        print('\n' + colored('Items', 'blue', attrs=['bold']))
        i = 1
        for item in self.items:
            print(indt + str(i) + '.', item.name + ':', item.description, '(x5)')
            i += 1
        print(indt + '(back)')
