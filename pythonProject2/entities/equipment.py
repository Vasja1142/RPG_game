# entities/equipment.py
import pygame

class Equipment:
    def __init__(self, name, equipment_type, bonus, level=1):  # Добавляем level
        self.name = name
        self.equipment_type = equipment_type
        self.bonus = bonus
        self.level = level

    def apply_bonus(self, player):
        """Применяет бонус к характеристикам игрока."""
        if self.equipment_type == "weapon":
            player.damage += self.bonus
        elif self.equipment_type == "helmet":
            player.health = min(player.health + self.bonus, player.max_health) # Исправлено
        elif self.equipment_type == "shoes":
            player.speed += self.bonus
        elif self.equipment_type == "amulet":
            player.max_health += self.bonus
            player.health = min(player.health + self.bonus, player.max_health)  # Применяем бонус к текущему здоровью
        elif self.equipment_type == "ring":
            player.damage += self.bonus
        elif self.equipment_type == "cloak":
            player.armor += self.bonus
        elif self.equipment_type == "armor":
            player.armor += self.bonus  # Бонус к защите

    def upgrade(self):
        """Повышает уровень предмета."""
        self.level += 1
        self.bonus += 2  # Например, увеличиваем бонус на 2 за уровень