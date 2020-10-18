from characters.strategies import Strategy

class SpellsOnly(Strategy):
    def determine_action(self, enemies):
        target = self.determine_target(enemies)
        spell_name = self.determine_spell(enemies)
        self.character.cast_spell([target], spell_name)

    def determinate_bonus_action(self, enemies):
        target = self.determine_target(enemies)
        # spell_name = self.determine_spell(enemies)
        self.character.bonus_action(target)

    def determine_spell(self, enemies):
        return "Firebolt"
        # return "HoldPerson" if self.character.concentrating_spell is None else "Firebolt"
