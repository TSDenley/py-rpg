import random

class Character:
    def __init__(self, hp, mp, atk, df, magic):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atk = atk
        self.df = df
        self.magic = magic
        self.actions = ['Attack', 'Magic']

    def generate_damage(self):
        return random.randrange(self.atk - 10, self.atk + 10)

    def take_damage(self, dmg):
        self.hp -= dmg

    def choose_action(self):
        i = 1
        for action in self.actions:
            # Skip magic is character has no spells
            if action == 'Magic' and len(self.magic) < 1:
                continue
            print(str(i) + ':', action)
            i += 1

    def choose_spell(self):
        i = 1
        for spell in self.magic:
            print(str(i) + ':', spell.name, '(cost:', str(spell.cost) + ')')
            i += 1

    def reduce_mp(self, cost):
        self.mp -= cost
        if self.mp < 0:
            self.mp = 0
