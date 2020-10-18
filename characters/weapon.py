from .damage_die import DamageDie
from combat.combat_utils import log
from roll import hit_tally

class Weapon:
    def __init__(self, name, data):
        self.name = name
        self.damage_dice = []
        for damage_die in data:
            self.damage_dice.append(DamageDie.from_json(damage_die))

    def _calculate_damage(self, is_crit=False):
        return [damage_die.calculate_damage(is_crit) for damage_die in self.damage_dice]

    def attack(self, roll, to_hit, target):
        if roll == 1:
            log("No damage (Nat 1)")
            return
        elif roll == 20:
            log("Nat 20!")
            hit_tally.append(1)
            damage = self._calculate_damage(is_crit=True)
        else:
            hit = roll + to_hit
            attack_hits = hit >= target.ac
            if attack_hits:
                hit_tally.append(1)
                log("Hit.")
                damage = self._calculate_damage()
            else:
                log("No damage (Miss)")
                return
        target.receive_damage(damage)
