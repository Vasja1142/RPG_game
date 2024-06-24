# entities/equipment.py
import pygame
import random

class Equipment:
    def __init__(self, name, equipment_type, bonus, level=1):
        self.name = name
        self.equipment_type = equipment_type
        self.bonus = bonus
        self.level = level
        self.skills = []  # Список навыков

    def apply_bonus(self, player):
        """Применяет бонус к характеристикам игрока."""
        if self.equipment_type == "weapon":
            player.damage += self.bonus
        elif self.equipment_type == "helmet":
            player.health = min(player.health + self.bonus, player.max_health)
        elif self.equipment_type == "shoes":
            player.speed += self.bonus
        elif self.equipment_type == "amulet":
            player.max_health += self.bonus
            player.health = min(player.health + self.bonus, player.max_health)
        elif self.equipment_type == "ring":
            player.damage += self.bonus
        elif self.equipment_type == "cloak":
            player.armor += self.bonus
        elif self.equipment_type == "armor":
            player.armor += self.bonus

    def upgrade(self):
        """Повышает уровень предмета."""
        self.level += 1
        self.bonus += 2

    def generate_random_skills(self, skill_list):
        """Добавляет 1-3 случайных навыка из списка."""
        num_skills = random.randint(1, 3)
        self.skills = random.sample(skill_list, num_skills)
        for skill in self.skills:
            skill["value"] = skill["base_strength"] + (self.level * skill["multiplier"])