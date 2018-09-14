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
player_items = [ potion, hipotion, ether, grenade ]
enemy_items = []

# Instantiate characters
player = Character(1200, 65, 60, 35, player_magic, player_items)
enemy = Character(1200, 65, 60, 35, enemy_magic, enemy_items)

turn = 1
dev1 = '================================================================================'
dev2 = '--------------------------------------------------------------------------------'
invalid_action = 'Please choose an option from the menu'

print('\n' + colored('AN ENEMY ATTACKS!', 'red', attrs=['bold']))

# Start main game loop
while True:
    print('\n' + dev1)
    print(colored('Turn ' + str(turn), attrs=['bold']) + '\n')

    # Player turn
    cprint('Player turn', 'green', attrs=['bold'])
    player.choose_action()
    player_action = input('Choose action: ')

    ## Type 'exit' to quit the game
    if player_action == 'exit':
        cprint('Bye!', 'green', attrs=['bold'])
        break

    ## Action choice must be a number
    try:
        player_action = int(player_action) - 1
    except:
        print(invalid_action)
        continue

    if player_action == 0:

        ## Attack
        player_dmg = player.generate_damage()
        enemy.take_damage(player_dmg)

    elif player_action == 1:

        ## Choose a spell to cast
        player.choose_spell()
        player_magic_choice = input('Choose spell: ')

        if player_magic_choice == 'back':
            continue

        try:
            player_magic_choice = int(player_magic_choice) - 1
            player_spell = player.magic[player_magic_choice]
        except:
            print(invalid_action)
            continue

        ### Check spell MP cost
        if player_spell.cost > player.mp:
            print('\n' + colored('Not enough MP to cast spell!', 'blue', attrs=['bold']))
            continue

        ### Cast the spell
        print('\nYou cast ' + colored(player_spell.name, 'blue', attrs=['bold']) + '!')

        player_spell_dmg = player_spell.generate_damage()

        if player_spell.type == 'black':
            ### Damage the enemy
            enemy.take_damage(player_spell_dmg)
        elif player_spell.type == 'white':
            ### Heal the player
            player.heal(player_spell_dmg)
        else:
            print('Invalid spell type.')
            continue

        player.reduce_mp(player_spell.cost)

    elif player_action == 2:

        ## Choose and item to use
        player.choose_item()
        player_Item_choice = input('Choose item: ')

        if player_Item_choice == 'back':
            continue

        try:
            player_Item_choice = int(player_Item_choice) - 1
            player_item = player.items[player_Item_choice]
        except:
            print(invalid_action)
            continue

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

        ### Check quantity

    else:
        print(invalid_action)
        continue

    ## Enemy is killed and the player wins
    if enemy.hp < 1:
        print('\n' + colored('Enemy defeated!', 'red', attrs=['bold']))
        break

    print(colored('Enemy HP: ', 'red', attrs=['bold']) + str(enemy.hp) + '/' + str(enemy.maxhp))
    print(colored('Your HP: ', 'green', attrs=['bold']) + str(player.hp) + '/' + str(player.maxhp))
    print(colored('Your MP: ', 'blue', attrs=['bold']) + str(player.mp) + '/' + str(player.maxmp))

    # Enemy turn
    print('\n' + dev2 + '\n')
    cprint('Enemy turn', 'red', attrs=['bold'])
    ## Enemy just attacks for now
    enemy_action = 0

    if enemy_action == 0:
        ## Attack the player
        enemy_dmg = enemy.generate_damage()
        player.take_damage(enemy_dmg)
        print(colored('Your HP: ', 'green', attrs=['bold']) + str(player.hp))

    ## Player has been killed and looses
    if player.hp < 1:
        print('\n' + colored('You have been defeated!', 'red', attrs=['bold']) + '\n')
        break

    turn += 1
