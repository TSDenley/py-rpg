import sys
from classes.game import Game
from classes.character import Character
from classes.magic import Spell
from classes.inventory import Item

from colorama import init
from termcolor import colored, cprint
init()


# Available magic
## Black magic (does damge)
fire = Spell('Fire', 10, 100, 'black')
thunder = Spell('Thunder', 10, 100, 'black')
blizzard = Spell('Blizzard', 10, 100, 'black')
quake = Spell('Quake', 15, 140, 'black')
meteor = Spell('Meteor', 22, 200, 'black')

## White magic (heals hp)
cure = Spell('Cure', 12, 120, 'white')
cura = Spell('Cura', 20, 200, 'white')

## Assign spells to characters
player_magic = [ fire, thunder, blizzard, quake, meteor, cure, cura ]

# Available Item
potion = Item('Potion', 'restore_hp', 'Restores 50 HP', 50)
hipotion = Item('Hi-Potion', 'restore_hp', 'Restores 150 HP', 150)
ether = Item('Ether', 'restore_mp', 'Restores 50 MP', 50)
hiether = Item('Hi-Ether', 'restore_mp', 'Restores 150 MP', 150)
elixir = Item('Elixir', 'restore_hp_mp', 'Fully restores HP & MP', 0)
grenade = Item('Grenade', 'damage', 'Damages all enemies', 300)

## Assign items
player_items = [
    { 'item': potion, 'qty': 5 },
    { 'item': ether, 'qty': 4 },
]
player1_items = [
    { 'item': hipotion, 'qty': 3 },
    { 'item': grenade, 'qty': 2 }
]

# Instantiate characters
## name, hp, mp, atk, df, magic, items
player1 = Character('Player 1', 750, 0, 100, 50, [], player1_items)
player2 = Character('Player 2', 500, 65, 45, 35, player_magic, player_items)
enemy = Character('Enemy 1', 300, 30, 60, 35, [ fire ], [])
enemy2 = Character('Enemy 2', 1400, 65, 80, 60, [], [])
enemy3 = Character('Enemy 3', 300, 30, 60, 35, [ fire ], [])

players = [ player1, player2 ]
enemies = [ enemy, enemy2, enemy3 ]

Game = Game(players, enemies)

print('\n' + colored('AN ENEMY ATTACKS!', 'red', attrs=['bold']))

# Start main game loop
while True:
    Game.display_character_stats()

    # Player turn
    p = 0
    # for player in players:
    while p < len(players):
        player = players[p]

        if player.hp > 0:
            player_action = Game.choose_player_action(player)

            ## Type 'exit' to quit the game
            if player_action == 'exit':
                cprint('\nBye!', 'green', attrs=['bold'])
                sys.exit()

            ## Action choice must be a number
            try:
                player_action = int(player_action) - 1
            except:
                print(Game.invalid_action)
                continue

            if player_action == 0:
                ## Attack
                if not Game.resolve_attack(player):
                    continue
            elif player_action == 1:
                ## Magic
                if not Game.resolve_spell(player):
                    continue
            elif player_action == 2:
                ## Item
                if not Game.resolve_item(player):
                    continue
            else:
                print(Game.invalid_action)
                continue
        p += 1

        # TODO: End game (all enemies are killed)
        ## Enemy is killed and the player wins
        # if enemy.hp < 1:
        #     print('\n' + colored('Enemy defeated!', 'red', attrs=['bold']))
        #     sys.exit()

    # Enemy turn
    for enemy in enemies:
        if enemy.hp > 0:
            ## Enemy just attacks for now
            enemy_action = Game.choose_enemy_action(enemy)

            if enemy_action == 0:
                target_player = Game.choose_target_player()
                print('\n' + enemy.name, 'attacks', colored(target_player.name, attrs=['bold']) + '!')
                target_player.take_damage(enemy.generate_damage())
            # elif enemy_action == 1:
                # Magic

    # TODO: End game (all players are killed)
    ## Player has been killed and looses
    # if player.hp < 1:
    #     print('\n' + colored('You have been defeated!', 'red', attrs=['bold']) + '\n')
    #     sys.exit()

    Game.next_turn()
