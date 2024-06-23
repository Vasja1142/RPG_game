import pygame

class Equipment:
    def __init__(self, name, equipment_type, bonus):
        self.name = name
        self.equipment_type = equipment_type
        self.bonus = bonus

    def apply_bonus(self, player):
        """Применяет бонус к характеристикам игрока."""
        if self.equipment_type == "weapon":
            player.damage += self.bonus
        elif self.equipment_type == "helmet":
            player.health += self.bonus
        elif self.equipment_type == "shoes":
            player.speed += self.bonus
        elif self.equipment_type == "amulet":
            player.max_health += self.bonus
        elif self.equipment_type == "ring":
            player.damage += self.bonus
        elif self.equipment_type == "cloak":
            player.armor += self.bonus
        elif self.equipment_type == "armor":
            player.armor += self.bonus  # Бонус к защите