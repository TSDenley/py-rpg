from colorama import init
from termcolor import colored, cprint
init()


DEV1 = '================================================================================'
DEV2 = '--------------------------------------------------------------------------------'
invalid_action = 'Please choose an option from the menu'
indt = '    '

class Game:
    def __init__(self, players, enemies):
        self.turn = 1
        self.players = players
        self.enemies = enemies
        self.invalid_action = invalid_action

    def display_character_stats(self):
        print('\n' + DEV1)
        print(colored('Turn ' + str(self.turn), attrs=['bold']) + '\n')

        cprint('Players:', 'green', attrs=['bold'])

        for player in self.players:
            print(
                  colored(player.name, attrs=['bold']),
                  'HP:', str(player.hp) + '/' + str(player.maxhp),
                  'MP:', str(player.mp) + '/' + str(player.maxmp)
            )

        print(DEV2)
        cprint('Enemies:', 'red', attrs=['bold'])

        for enemy in self.enemies:
            print(
                  colored(enemy.name, attrs=['bold']),
                  'HP:', str(enemy.hp) + '/' + str(enemy.maxhp),
                  'MP:', str(enemy.mp) + '/' + str(enemy.maxmp)
            )

        print('\n')

    def choose_player_action(self, player):
        cprint('Player turn', 'green', attrs=['bold'])
        player.choose_action()
        return input('Choose action: ')

    def choose_enemy_action(self, enemy):
        cprint('\nEnemy turn', 'red', attrs=['bold'])
        return 0

    """
    Choose target player/enemy as target of spell or attack
    @return Character instance or False
    """
    def choose_target(self):
        print('\n' + colored('Target:', attrs=['bold']))

        targets = self.players + self.enemies

        i = 1
        for target in targets:
            print(indt + str(i) + ':', target.name)
            i += 1

        print(indt + '(back)')

        target_choice = input('Choose target: ')

        if target_choice == 'back':
            return False

        try:
            target_choice = int(target_choice) - 1
            target = targets[target_choice]
        except:
            print(invalid_action)
            return False

        return target

    """
    Resolves a spell effect: damages or heals a target
    @calls self.choose_target()
    @return True or False
    """
    def resolve_spell(self, caster):
        # Choose a spell to cast
        caster.choose_spell()
        spell_choice = input('Choose spell: ')

        if spell_choice == 'back':
            return False

        try:
            spell_choice = int(spell_choice) - 1
            spell = caster.magic[spell_choice]
        except:
            print(invalid_action)
            return False

        ## Check spell MP cost
        if spell.cost > caster.mp:
            print('\n' + colored('Not enough MP to cast spell!', 'blue', attrs=['bold']))
            return False

        ## Designate a target
        target = self.choose_target()
        if not target:
            return False

        ## Cast the spell
        print(
              '\n' + caster.name, 'cast', colored(spell.name, 'blue', attrs=['bold']),
              'on', colored(target.name, attrs=['bold']) + '!'
        )

        spell_dmg = spell.generate_damage()

        if spell.type == 'black':
            target.take_damage(spell_dmg)
        elif spell.type == 'white':
            target.heal(spell_dmg)
        else:
            print('Invalid spell type')
            return False

        caster.reduce_mp(spell.cost)
        return True

    """
    Resolves an item effect: damages or heals a target
    @calls self.choose_target()
    @return True or False
    """
    def resolve_item(self, user):
        # Choose and item to use
        user.choose_item()
        item_choice = input('Choose item: ')

        if item_choice == 'back':
            return False

        try:
            item_choice = int(item_choice) - 1
            item = user.items[item_choice]['item']
        except:
            print(invalid_action)
            return False

        ## Reduce item quantity from player inventory
        user.items[item_choice]['qty'] -= 1

        ## Designate a target
        target = self.choose_target()
        if not target:
            return False

        ## Resolve the item effect
        if item.type == 'restore_hp':
            target.heal(item.prop)
        elif item.type == 'restore_mp':
            target.heal_mp(item.prop)
        elif item.type == 'restore_hp_mp':
            target.heal(item.prop)
            target.heal_mp(item.prop)
        elif item.type == 'damage':
            target.take_damage(item.prop)
        else:
            print('Invalid item type')
            return False

        return True

    def next_turn(self):
        self.turn += 1
