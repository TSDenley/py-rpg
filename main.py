from classes.character import Character
from colorama import init
from termcolor import colored, cprint

player_magic = [
    {'name': 'Fire', 'cost': 10, 'dmg': 60},
    {'name': 'Thunder', 'cost': 15, 'dmg': 80},
    {'name': 'Blizzard', 'cost': 20, 'dmg': 100},
]

player = Character(1200, 65, 60, 34, player_magic)
enemy = Character(1200, 65, 45, 25, player_magic)

turn = 1
dev1 = '================================================================================'
dev2 = '--------------------------------------------------------------------------------'
invalid_action = 'Please choose an option from the menu'

print('\n' + colored('AN ENEMY ATTACKS!', 'red', attrs=['bold']))

# Start main game loop
while True:
    print('\n' + dev1)
    print(colored('Turn ' + str(turn), attrs=['bold']) + '\n')

    cprint('Player turn', 'green', attrs=['bold'])
    player.choose_action()
    print('(exit)')
    player_action = input('Choose action: ')

    # Type 'exit' to quit the game
    if player_action == 'exit':
        cprint('Bye!', 'green', attrs=['bold'])
        break

    # Action choice must be a number
    try:
        player_action = int(player_action) - 1
    except:
        print(invalid_action)
        continue

    if player_action == 0:
        # Attack
        player_dmg = player.generate_damage()
        enemy.take_damage(player_dmg)
        print('\nYou attacked for ' + colored(str(player_dmg), 'red', attrs=['bold']) + ' points of damage!')
        print(colored('Enemy HP: ', 'red', attrs=['bold']) + str(enemy.hp))
    elif player_action == 1:
        # Choose a spell to cast
        print('\n' + colored('Magic', 'blue', attrs=['bold']))
        player.choose_spell()
        print('(back)')
        player_spell_choice = input('Choose spell: ')

        if player_spell_choice == 'back':
            continue

        try:
            player_spell_choice = int(player_spell_choice) - 1
            player_spell = player.magic[player_spell_choice]
        except:
            print(invalid_action)
            continue

        # Check spell MP cost
        if player_spell['cost'] > player.mp:
            print('\n' + colored('Not enough MP to cast spell!', 'blue', attrs=['bold']))
            continue

        # Cast the spell
        print('\nYou cast ' + colored(player_spell['name'], 'blue', attrs=['bold']) + '!')
        player.reduce_mp(player_spell['cost'])

        player_spell_dmg = player.generate_spell_damage(player_spell['dmg'])
        enemy.take_damage(player_spell_dmg)
        print('Your spell does ' + colored(str(player_spell_dmg), 'blue', attrs=['bold']) + ' points of damage!')

        print(colored('Enemy HP: ', 'red', attrs=['bold']) + str(enemy.hp))
        print(colored('Your MP: ', 'blue', attrs=['bold']) + str(player.mp))
    else:
        print(invalid_action)
        continue

    # Enemy is killed and the player wins
    if enemy.hp < 1:
        print('\n' + colored('Enemy defeated!', 'red', attrs=['bold']))
        break

    print('\n' + dev2 + '\n')
    cprint('Enemy turn', 'red', attrs=['bold'])
    # Enemy just attacks for now
    enemy_action = 0

    if enemy_action == 0:
        # Attack the player
        enemy_dmg = enemy.generate_damage()
        player.take_damage(enemy_dmg)
        print('Enemy attacked for ' + colored(str(enemy_dmg), 'red', attrs=['bold']) + ' points of damage!')
        print(colored('Your HP: ', 'green', attrs=['bold']) + str(player.hp))

    # Player has been killed and looses
    if player.hp < 1:
        print('\n' + colored('You have been defeated!', 'red', attrs=['bold']) + '\n')
        break

    turn += 1
