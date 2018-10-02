import sys
import random
from colorama import init
from termcolor import colored, cprint
init()


class Game:
    def __init__(self, players, enemies):
        self.turn = 1
        self.players = players
        self.enemies = enemies
        self.characters = players + enemies
        self.invalid_action = 'Please choose an option from the menu'
        self.indt = '    '
        self.DEV1 = '================================================================================'
        self.DEV2 = '--------------------------------------------------------------------------------'

    """Print all character HP/MP at the begining of each turn"""
    def display_character_stats(self):
        print('\n' + self.DEV1)
        print(colored('Turn ' + str(self.turn), attrs=['bold']) + '\n')

        cprint('Players:', 'green', attrs=['bold'])

        for player in self.players:
            if player.hp > 0:
                player_hp = 'HP: ' + str(player.hp) + '/' + str(player.maxhp)
            else:
                player_hp = '(DEAD)'

            if len(player.magic) > 0:
                player_mp = 'MP: ' + str(player.mp) + '/' + str(player.maxmp)
            else:
                player_mp = ''

            print(
                  colored(player.name, attrs=['bold']),
                  player_hp,
                  player_mp
            )

        print(self.DEV2)
        cprint('Enemies:', 'red', attrs=['bold'])

        for enemy in self.enemies:
            if enemy.hp > 0:
                enemy_hp = 'HP: ' + str(enemy.hp) + '/' + str(enemy.maxhp)
            else:
                enemy_hp = '(DEAD)'

            if len(enemy.magic) > 0:
                enemy_mp = 'MP: ' + str(enemy.mp) + '/' + str(enemy.maxmp)
            else:
                enemy_mp = ''

            print(
                  colored(enemy.name, attrs=['bold']),
                  enemy_hp,
                  enemy_mp
            )

        print('\n')

    """
    Prompts player to choose action
    @param player - character instance
    @return int
    """
    def choose_player_action(self, player):
        cprint(player.name + '\'s turn', 'green', attrs=['bold'])
        player.choose_action()
        return input('Choose action: ')

    """
    Filter magic list to spell that can be afforded
    @param caster - character instance
    @return list - affordable spells
    """
    def filter_magic(self, caster):
        return list(filter(
                           lambda s: s.cost <= caster.mp,
                           caster.magic
                          ))

    """
    Set enemy action
    @param enemy - character instance
    @return int
    """
    def choose_enemy_action(self, enemy):
        cprint('\n' + enemy.name + '\'s turn', 'red', attrs=['bold'])

        ## Does the enemy have magic & MP?
        if len(enemy.magic) > 0 and enemy.mp > 0:
            if len(self.filter_magic(enemy)) > 0:
                # Randomly choose magic or attact
                return random.randrange(0, 2)

        # Default to attack
        return 0

    """
    Choose target player/enemy as target of spell or attack
    @return Character instance or False
    """
    def choose_target(self):
        cprint('\nTarget:', attrs=['bold'])

        i = 1
        for character in self.characters:
            if character.hp > 0:
                print(self.indt + str(i) + ':', character.name)
            else:
                print(self.indt + str(i) + ':', character.name, '(DEAD)')
            i += 1

        print(self.indt + '(back)')

        target_choice = input('Choose target: ')

        if target_choice == 'back':
            return False

        try:
            target_choice = int(target_choice) - 1
            target = self.characters[target_choice]
        except:
            print(invalid_action)
            return False

        return target

    """
    Choose a random player to attack
    @return player character instance
    """
    def choose_target_player(self):
        target = random.randrange(0, len(self.players))

        while self.players[target].hp < 1:
            target = random.randrange(0, len(self.players))

        return self.players[target]

    """
    Resolves a basic attack: damage a target
    @return True or False
    """
    def resolve_attack(self, attacker):
        target = self.choose_target()
        if not target:
            return False

        print('\n' + attacker.name, 'attacks', colored(target.name, attrs=['bold']) + '!')
        target.take_damage(attacker.generate_damage())

        return True

    """
    Resolve an enemy basic attack on a player
    @param attacker - character instance
    """
    def resolve_enemy_attack(self, attacker):
        target_player = self.choose_target_player()
        print('\n' + attacker.name, 'attacks', colored(target_player.name, attrs=['bold']) + '!')
        target_player.take_damage(attacker.generate_damage())

    """
    Resolves a spell effect: damages or heals a target
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
            cprint('\nNot enough MP to cast spell!', 'blue', attrs=['bold'])
            return False

        ## Designate a target
        target = self.choose_target()
        if not target:
            return False

        ## Cast the spell
        print(
              '\n' + caster.name, 'casts', colored(spell.name, 'blue', attrs=['bold']),
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
    Resolves an enemy spell effect: damages or heals a target
    """
    def resolve_enemy_spell(self, caster):
        target = self.choose_target_player()

        # Choose spell
        affordable_spells = self.filter_magic(caster)
        spell = affordable_spells[
            random.randrange(0, len(affordable_spells))
        ]

        # Cast the spell
        print(
              '\n' + colored(caster.name, 'red', attrs=['bold']), 'casts',
              colored(spell.name, 'blue', attrs=['bold']),
              'on', colored(target.name, attrs=['bold']) + '!'
        )

        spell_dmg = spell.generate_damage()

        if spell.type == 'black':
            target.take_damage(spell_dmg)
        elif spell.type == 'white':
            target.heal(spell_dmg)

        caster.reduce_mp(spell.cost)

    """
    Resolves an item effect: damages or heals a target
    @param user - character instance
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

    """
    Increment the turn counter
    """
    def next_turn(self):
        self.turn += 1

    """
    End game
    """
    def enemies_defeated(self):
        for enemy in self.enemies:
            if enemy.hp > 0:
                return

        print(
              '\n' + colored('All enemies are defeated!', 'red', attrs=['bold']),
              'Your party is victorious!'
        )

        sys.exit()

    def players_defeated(self):
        for player in self.players:
            if player.hp > 0:
                return

        print(
              '\n' + colored('All players are defeated!', 'red', attrs=['bold']),
              'Your enemies are victorious!'
        )

        sys.exit()
