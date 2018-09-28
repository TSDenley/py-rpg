import random
from colorama import init
from termcolor import colored, cprint
init()


class Character:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.mp = mp
        self.maxmp = mp
        self.atk = atk
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = [ 'Attack', 'Magic', 'Items' ]
        self.indt = '    '

    def generate_damage(self):
        return random.randrange(self.atk - 10, self.atk + 10)

    def take_damage(self, dmg):
        self.hp -= dmg
        print('...' + colored(str(dmg), 'red', attrs=['bold']) + ' damage!')

        if self.hp < 1:
            cprint('\n' + self.name + ' is defeated!\n', attrs=['bold'])

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

    """
    Print action choice menu
    """
    def choose_action(self):
        i = 1
        for action in self.actions:
            # Skip magic is character has no spells
            if action == 'Magic' and len(self.magic) < 1:
                continue

            # Skip items if character has no items
            if action == 'Items' and len(self.items) < 1:
                continue

            print(self.indt + str(i) + '.', action)
            i += 1

        print(self.indt + '(exit)')

    """
    Print magic menu
    """
    def choose_spell(self):
        print('\n' + colored('Magic', 'blue', attrs=['bold']))

        i = 1
        for spell in self.magic:
            print(
                  self.indt + str(i) + '.',
                  spell.name,
                  '(cost:', str(spell.cost) + ')'
            )
            i += 1

        print(self.indt + '(back)')

    """
    Print item choice menu
    """
    def choose_item(self):
        print('\n' + colored('Items', 'blue', attrs=['bold']))

        i = 1
        for item in self.items:
            if item['qty'] < 1:
                continue

            print(
                 self.indt + str(i) + '.',
                 item['item'].name + ':',
                 item['item'].description,
                 '(' + str(item['qty']) + ')'
            )
            i += 1

        print(self.indt + '(back)')
