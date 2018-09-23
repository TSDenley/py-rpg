from classes.game import Game
from classes.character import Character
from classes.magic import Spell
from classes.inventory import Item

from colorama import init
from termcolor import colored, cprint
init()


# Available magic
## Black magic (does damge)
fire = Spell('Fire', 8, 100, 'black')
thunder = Spell('Thunder', 8, 100, 'black')
blizzard = Spell('Blizzard', 8, 100, 'black')
quake = Spell('Quake', 12, 140, 'black')
meteor = Spell('Meteor', 18, 200, 'black')

## White magic (heals hp)
cure = Spell('Cure', 12, 120, 'white')
cura = Spell('Cura', 20, 200, 'white')

## Assign spells to characters
player_magic = [ fire, thunder, blizzard, quake, meteor, cure, cura ]
enemy_magic = []

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
                    { 'item': hipotion, 'qty': 2 },
                    { 'item': ether, 'qty': 3 },
                    { 'item': grenade, 'qty': 1 }
               ]
enemy_items = []

# Instantiate characters
player = Character('Player', 1200, 65, 60, 35, player_magic, player_items)
enemy = Character('Enemy', 1200, 65, 60, 35, enemy_magic, enemy_items)

players = [ player ]
enemies = [ enemy ]

Game = Game(players, enemies)

print('\n' + colored('AN ENEMY ATTACKS!', 'red', attrs=['bold']))

# Start main game loop
while True:
    Game.display_character_stats()

    player_action = Game.choose_player_action(player)

    ## Type 'exit' to quit the game
    if player_action == 'exit':
        cprint('Bye!', 'green', attrs=['bold'])
        break

    ## Action choice must be a number
    try:
        player_action = int(player_action) - 1
    except:
        print(Game.invalid_action)
        continue

    if player_action == 0:

        ## Attack
        player_dmg = player.generate_damage()
        enemy.take_damage(player_dmg)

    elif player_action == 1:

        if not Game.resolve_spell(player):
            continue

    elif player_action == 2:

        ## Choose and item to use
        player.choose_item()
        player_item_choice = input('Choose item: ')

        if player_item_choice == 'back':
            continue

        try:
            player_item_choice = int(player_item_choice) - 1
            player_item = player.items[player_item_choice]['item']
        except:
            print(Game.invalid_action)
            continue

        ### Reduce item quantity from player inventory
        player.items[player_item_choice]['qty'] -= 1

        ### Resolve the item effect
        if player_item.type == 'restore_hp':
            player.heal(player_item.prop)
        elif player_item.type == 'restore_mp':
            player.heal_mp(player_item.prop)
        elif player_item.type == 'restore_hp_mp':
            player.heal(player_item.prop)
            player.heal_mp(player_item.prop)
        elif player_item.type == 'damage':
            enemy.take_damage(player_item.prop)
        else:
            print('Invalid item type')
            continue

    else:
        print(Game.invalid_action)
        continue

    ## Enemy is killed and the player wins
    if enemy.hp < 1:
        print('\n' + colored('Enemy defeated!', 'red', attrs=['bold']))
        break

    # Enemy turn
    cprint('Enemy turn', 'red', attrs=['bold'])
    ## Enemy just attacks for now
    enemy_action = 0

    if enemy_action == 0:
        ## Attack the player
        enemy_dmg = enemy.generate_damage()
        player.take_damage(enemy_dmg)

    ## Player has been killed and looses
    if player.hp < 1:
        print('\n' + colored('You have been defeated!', 'red', attrs=['bold']) + '\n')
        break

    Game.next_turn()
