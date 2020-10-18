from characters.constants import Stats
from characters.damage_die import DamageDie
from characters.spells.spell import Spell


class Fireball(Spell):
    def __init__(self):
        self.primary_damage = DamageDie(8, 6, "fire", 0)
        super(Fireball, self).__init__("Fireball", Stats.DEX)

    def primary_effect(self, caster, targets):
        damage = self.primary_damage.calculate_damage()
        for target in targets:
            saved = target.make_save(caster.spell_dc, self.save)
            target.receive_damage(saved=saved)
