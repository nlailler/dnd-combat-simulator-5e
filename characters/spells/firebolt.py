from characters.constants import Stats, RerollType
from characters.damage_die import DamageDie
from characters.spells.spell import Spell
from combat.combat_utils import log
from roll import hit_tally

class Firebolt(Spell):
    def __init__(self):
        self.primary_damage = DamageDie(2, 10, "fire", 0)
        super(Firebolt, self).__init__("Firebolt", Stats.DEX)

    def primary_effect(self, caster, targets):
        target = targets[0]
        roll = caster.roll(RerollType.ATTACK)
        if roll == 1:
            log("No damage (Nat 1)")
            return
        elif roll == 20:
            log("Nat 20!")
            hit_tally.append(1)
            damage = [self.primary_damage.calculate_damage(is_crit=True)]
        else:
            hit = roll + caster.spell_to_hit
            attack_hits = hit >= target.ac
            if attack_hits:
                hit_tally.append(1)
                log("Hit.")
                damage = [self.primary_damage.calculate_damage()]
            else:
                log("No damage (Miss)")
                return
        target.receive_damage(damage)
