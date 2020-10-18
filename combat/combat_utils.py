import math

from roll import rs

def log(message, should_print=False):
    if should_print:
        print(message)

def half(damage, round_up=False):
    half_damage = damage/2
    return math.ceil(half_damage) if round_up else math.floor(half_damage)

def roll(has_advantage, has_disadvantage):
    roll = rs.randint(1, 21)
    second_roll = rs.randint(1, 21)

    if has_advantage and not has_disadvantage:
        return max(roll, second_roll)
    elif not has_advantage and has_disadvantage:
        return min(roll, second_roll)
    else:
        return roll

def combat_status(npcs, players, should_print):
    log('Npcs:', should_print=should_print)
    for npc in npcs:
        log(npc.status(), should_print=should_print)

    log('Players:', should_print=should_print)
    for player in players:
        log(player.status(), should_print=should_print)

def all_unconscious(characters):
    return all([character.hp == 0 for character in characters])
