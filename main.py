import sys
import json
import os
from datetime import datetime

from collections import defaultdict

from combat.combat import combat
from characters.character import Character
from characters.constants import (
    RerollType
)
from characters.weapon import Weapon
from combat.combat_utils import (
    all_unconscious,
    log,
)
from roll import hit_tally

should_print = False

def load_weapons(directory):
    weapons = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as json_file:
            weapon_name = filename[:-5]
            weapons[weapon_name] = Weapon(weapon_name, json.load(json_file))
    log(weapons)
    return weapons

def load_characters(directory, weapons, is_npc=False):
    characters = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as json_file:
            c = Character(is_npc, json.load(json_file), weapons)
            characters[c.name] = c
    log(characters)
    return characters

def roll_for_initiative(npcs, players):
    combat_order = defaultdict(list)
    for npc in npcs:
        roll = npc.roll(RerollType.INITIATIVE)
        combat_order[roll + npc.initiative] = npc

    for player in players:
        roll = player.roll(RerollType.INITIATIVE)
        combat_order[roll + player.initiative] = player
    list_pairs = combat_order.items()
    list_pairs = sorted(list_pairs, key=lambda t: t[0], reverse=True)
    return list_pairs

def reset(characters):
    for character in characters:
        character.hp = character.max_hp
        character.conditions = []
        character.effects = []
        character.concentrating_spell = None
        character.concentration_spell_effect = None
        character.targets_concentrating_on = 0

def main():
    weapons = load_weapons('weapons')
    dict_npcs = load_characters('npcs', weapons, is_npc=True)
    npcs = dict_npcs.values()
    dict_players = load_characters('players', weapons)
    players = dict_players.values()

    player_wins = 0
    trials1 = 1
    trials = 1000
    start = datetime.now()
    for count1 in range(trials1):
        print(trials*count1)
        print(datetime.now())
        for count in range(trials):
            combat_order = roll_for_initiative(npcs, players)
            for initiative, character in combat_order:
                log("{} rolled a {} for initiative".format(character.name, initiative))
            combat_order = [pair[1] for pair in combat_order]
            combat(combat_order, npcs, players)
            if all_unconscious(npcs):
                player_wins += 1.0
            reset(npcs)
            reset(players)
    # print(len(hit_tally))
    print("Players won {}% of the time".format(player_wins/(trials*trials1)*100))


if __name__== "__main__":
    main()
