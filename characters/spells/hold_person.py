from characters.constants import Stats, Condition
from characters.damage_die import DamageDie
from characters.spells.spell import Spell, SpellEffect


class HoldPerson(Spell):
    def __init__(self):
        super(HoldPerson, self).__init__("HoldPerson", Stats.WIS)

    def primary_effect(self, caster, targets):
        number_failed = 0
        for target in targets:
            spell_effect = SpellEffect(caster, target, self)
            saved = target.make_save(caster.spell_dc, self.save)
            if saved:
                continue
            else:
                target.add_condition(Condition.PARALYZED)
                target.add_condition(Condition.INCAPACITATED)
                target.add_effect(spell_effect)
                number_failed += 1

        if number_failed > 0:
            caster.concentrating_spell = self
            caster.concentration_spell_effect = spell_effect
            caster.targets_concentrating_on = number_failed

    def secondary_effect(self, saved, caster, spell_effect):
        """resolves a secondary effect
        :param saved: boolean whether the target saved or not
        :param spell_effect: contains the dc, type of save and target of the effect
        """
        if saved:
            # print("Shoke off effect")
            self.cleanup_effect(caster, spell_effect)
        else:
            pass

    def cleanup_effect(self, caster, spell_effect):
        spell_effect.target.remove_condition(Condition.PARALYZED)
        spell_effect.target.remove_condition(Condition.INCAPACITATED)
        spell_effect.target.remove_effect(spell_effect)
        caster.targets_concentrating_on -= 1
        if caster.targets_concentrating_on < 1:
            caster.targets_concentrating_on = 0
            caster.concentrating_spell = None
            caster.concentration_spell_effect = None
