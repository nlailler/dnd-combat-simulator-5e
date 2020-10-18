from characters.strategies import Strategy

class AttacksOnly(Strategy):
    def determine_action(self, enemies):
        attacks_remaining = self.character.attacks_per_round
        while attacks_remaining > 0:
            target = self.determine_target(enemies)
            attacks_remaining = self.character.attack(target, attacks_remaining)

    def determinate_bonus_action(self, enemies):
        target = self.determine_target(enemies)
        self.character.bonus_action(target)
