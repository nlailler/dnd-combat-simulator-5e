import importlib

from combat.combat_utils import (
    half,
    roll,
)
from characters.constants import (
    RerollType,
    RerollStatus,
    Condition,
)

class Character:
    def __init__(self, is_npc, data, weapons):
        self.is_npc = is_npc
        self.name = data.get('name')
        self.hp = data.get('hp')
        self.max_hp = data.get('hp')
        self.ac = data.get('ac')
        self.initiative = data.get('initiative')
        self.attacks_per_round = data.get('attacks_per_round')
        self.damage_per_round = data.get('damage_per_round')
        self.extra_damage = data.get('extra_damage')
        self.to_hit = data.get('to_hit')
        self.advantages = data.get('advantages')
        self.disadvantages = data.get('disadvantages')
        self.saves = data.get("saves")
        self.weapon = weapons[data.get("weapon")]
        self.resistances = data.get("resistances")
        self.concentrating_spell = None
        self.concentration_spell_effect = None
        self.targets_concentrating_on = 0
        self.spells = self._load_spells(data.get("spells"))
        self.spell_to_hit = data.get("spell_to_hit", 0)
        self.spell_dc = data.get("spell_dc", 0)
        self.strategy = self._load_strategy(data.get("strategy", "Strategy"))
        self.conditions = []
        self.effects = []

    def _load_spells(self, spell_names):
        spells = {}
        module = importlib.import_module("characters.spells")
        for spell_name in spell_names:
            class_ = getattr(module, spell_name)
            instance = class_()
            spells[spell_name] = instance
        return spells

    def _load_strategy(self, strategy_name):
        module = importlib.import_module("characters.strategies")
        class_ = getattr(module, strategy_name)
        return class_(self)

    def _factor_in_resistance(self, damage):
        def resistance(d):
            if d["type"] in self.resistances:
                return half(d["damage"])
            else:
                return d["damage"]

        return list(map(resistance, damage))

    def resolve_end_of_turn_effects(self):
        for effect in self.effects:
            effect.secondary_effect()

    def add_condition(self, condition):
        self.conditions.append(condition)

    def remove_condition(self, condition):
        self.conditions.remove(condition)

    def add_effect(self, effect):
        self.effects.append(effect)

    def remove_effect(self, effect):
        self.effects.remove(effect)

    def roll(self, type):
        has_advantage = type in self.advantages
        has_disadvantage = type in self.disadvantages
        return roll(has_advantage, has_disadvantage)

    def attack(self, target, attacks_remaining=None):
        if attacks_remaining == None:
            attacks_remaining = self.attacks_per_round

        while(attacks_remaining > 0):
            roll = self.roll(RerollType.ATTACK)
            self.weapon.attack(roll, self.to_hit, target)
            attacks_remaining -= 1
            if target.hp == 0:
                return attacks_remaining

        return 0

    def cast_spell(self, targets, spell_name):
        spell = self.spells[spell_name]
        # for target in targets:
        #     print("{} is casting {} on {}!".format(self.name, spell_name, target.name))
        spell.execute(self, targets)

    def bonus_action(self, target):
        pass

    def make_save(self, dc, save):
        roll = self.roll(save)
        made_save = roll + self.saves[save] >= dc
        # print("Made save?: {}".format(made_save))
        return made_save

    def receive_damage(self, damage, saved=False):
        """
        :param damage: [{"type": DAMAGE_TYPE, "damage": int}]
        """
        damage_after_resistance = self._factor_in_resistance(damage)
        damage_to_receive = sum(damage_after_resistance)
        damage_to_receive = half(damage_to_receive)
        if self.concentrating_spell is not None:
            self.concentration_check
        self.hp = max(0, self.hp - damage_to_receive)

    def status(self):
        return "{} has {} hp".format(self.name, self.hp)

    def concentration_check(self, damage):
        concentration_dc = max(half(damage), 10)
        roll = self.roll(RerollType.CONCENTRATION)
        if roll + self.saves[Stats.CON] < concentration_dc:
            print("lost concentration")
            self.concentrating_spell.cleanup_effect(self.concentration_spell_effect)
            self.concentrating_spell = None

    def can_act(self):
        cannot_act = self.is_unconscious() or self.is_incapacitated()
        return not cannot_act

    def is_incapacitated(self):
        return Condition.INCAPACITATED in self.conditions

    def is_unconscious(self):
        if self.hp < 0:
            self.hp = 0
        return self.hp == 0
