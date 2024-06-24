import pygame
from entities.projectile import Projectile


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        super().__init__()
        self.game = game
        self.max_health = 100  # ДОБАВЛЕНО
        self.gold = 0  # Начальное количество золота
        self.health = self.max_health
        self.vision_range = 800  # Добавляем дальность видимости игрока

        player_image = pygame.image.load(
            "assets/images/player.png"
        ).convert_alpha()
        player_image = pygame.transform.scale(player_image, (140, 140))
        self.image = player_image
        self.rect = self.image.get_rect(topleft=pos)

        self.attack_cooldown = 300
        self.last_attack_time = 0

        self.experience = 0
        self.level = 1
        self.damage = 10
        self.speed = 3
        self.armor = 0
        self.equipment = []  # Список для хранения экипировки

    def add_equipment(self, equipment):
        """Добавляет предмет экипировки в список."""
        # Проверка, нет ли в списке уже экипировки такого типа
        for existing_equipment in self.equipment:
            if existing_equipment.equipment_type == equipment.equipment_type:
                return  # Не добавляем, если уже есть экипировка такого типа

        self.equipment.append(equipment)  # <--- Добавляем экипировку в инвентарь игрока

        # Применяем бонус к характеристикам
        equipment.apply_bonus(self)

    def sell_equipment(self, equipment):
        """Продаёт предмет экипировки."""
        self.gold += equipment.level * 5  # Цена продажи зависит от уровня предмета
        self.remove_equipment(equipment)  # Удаляем предмет из инвентаря

    def get_equipment(self, equipment_type):
        """Возвращает предмет экипировки указанного типа, если он есть в инвентаре."""
        for equipment in self.equipment:
            if equipment.equipment_type == equipment_type:
                return equipment
        return None

    def remove_equipment(self, slot_index):
        """Удаляет предмет экипировки из списка по индексу."""

        def remove_equipment(self, equipment):
            """Удаляет предмет экипировки из списка."""
            if equipment in self.equipment:
                self.equipment.remove(equipment)

            # Снимаем бонус экипировки
            if equipment_to_remove.equipment_type == "weapon":
                self.damage -= equipment_to_remove.bonus
            elif equipment_to_remove.equipment_type == "helmet":
                self.health -= equipment_to_remove.bonus
            elif equipment_to_remove.equipment_type == "shoes":
                self.speed -= equipment_to_remove.bonus
            elif equipment_to_remove.equipment_type == "amulet":
                self.max_health -= equipment_to_remove.bonus
            elif equipment_to_remove.equipment_type == "ring":
                self.damage -= equipment_to_remove.bonus
            elif equipment_to_remove.equipment_type == "cloak":
                self.armor -= equipment_to_remove.bonus
            elif equipment_to_remove.equipment_type == "armor":
                self.armor -= equipment_to_remove.bonus  # Бонус к защите

    def attack(self, projectile_group):
        """Создает снаряд и добавляет его в группу."""
        now = pygame.time.get_ticks()

        # Проверка на ручной режим
        if not self.game.auto_fire:
            projectile = Projectile(self.rect.center, direction=(1, 0))
            projectile_group.add(projectile)
        else:
            # Автоматический режим - используем cooldown
            if now - self.last_attack_time >= self.attack_cooldown:
                projectile = Projectile(self.rect.center, direction=(1, 0))
                projectile_group.add(projectile)
                self.last_attack_time = now

    def update(self, projectile_group, enemies):
        """Обновляет состояние игрока."""
        # Проверка видимости врагов
        in_vision = any(
            enemy.rect.right < self.rect.right + self.vision_range
            for enemy in enemies
        )

        # if in_vision:
            # self.attack(projectile_group)