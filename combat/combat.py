from combat.combat_utils import (
    all_unconscious,
    combat_status,
    log,
)

should_print = False

def attack(attacker, defender):
    attacker.attack(defender)

def turn(character, enemies):
    character.strategy.determine_action(enemies)
    character.strategy.determinate_bonus_action(enemies)

def combat_round(combat_order, npcs, players):
    for character in combat_order:
        if character.can_act():
            # print("{}'s turn".format(character.name))
            if character.is_npc:
                turn(character, players)
            else:
                turn(character, npcs)
        else:
            log("{} can't act".format(character.name), should_print=should_print)
        character.resolve_end_of_turn_effects()

def combat(combat_order, npcs, players):
    round = 1
    while(not all_unconscious(npcs) and not all_unconscious(players)):
        log('Round: ' + str(round), should_print=should_print)
        combat_status(npcs, players, should_print)
        check = combat_round(combat_order, npcs, players)
        log('\n')
        round += 1

    log('COMBAT END:\n')
    combat_status(npcs, players, should_print)
