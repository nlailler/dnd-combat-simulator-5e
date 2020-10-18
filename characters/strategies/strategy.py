class Strategy:
    def __init__(self, character):
        self.character = character

    def determine_target(self, enemies):
        weakest_enemy = None
        for enemy in enemies:
            weakest_enemy_is_unconscious = weakest_enemy is None or weakest_enemy.hp == 0
            if weakest_enemy_is_unconscious:
                weakest_enemy = enemy
                continue

            enemy_is_weak_but_not_unconscious = enemy.hp > 0 and weakest_enemy.hp > enemy.hp
            if enemy_is_weak_but_not_unconscious:
                weakest_enemy = enemy
        return weakest_enemy

    def determine_spell(self, enemies):
        return "Firebolt"

    def determine_action(self, enemies):
        pass

    def determinate_bonus_action(self, enemies):
        pass
