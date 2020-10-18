class Spell:
    def __init__(self, name, save, is_concentration=False):
        self.name = name
        self.save = save
        self.is_concentration = is_concentration

    def execute(self, caster, targets):
        self.primary_effect(caster, targets)

    def primary_effect(self, caster, targets):
        pass

    def secondary_effect(self, saved, caster, spell_effect):
        pass

    def cleanup_effect(self, target):
        pass


class SpellEffect:
    def __init__(self, caster, target, spell):
        self.caster = caster
        self.target = target
        self.spell = spell

    def secondary_effect(self):
        saved = self.target.make_save(self.caster.spell_dc, self.spell.save)
        self.spell.secondary_effect(saved, self.caster, self)
