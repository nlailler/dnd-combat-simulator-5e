from roll import rs

class DamageDie:
    def __init__(self, number, size, type, flat_bonus):
        self.number = number
        self.size = size
        self.type = type
        self.flat_bonus = flat_bonus

    @classmethod
    def from_json(cls, data):
        return cls(data.get("number"), data.get("size"), data.get("type"), data.get("flat_bonus"))

    def calculate_damage(self, is_crit=False):
        rolled_damage = self.flat_bonus
        number = self.number * 2 if is_crit else self.number
        for i in range(number):
            rolled_damage += rs.randint(1, self.size + 1)
        self.info = "{}d{} + {} => {}".format(self.number, self.size, self.flat_bonus, rolled_damage)
        return {"type": self.type, "damage": max(0, rolled_damage)}
