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

        self.equipment.append(equipment)
        self.apply_equipment_skills(equipment)

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

    def remove_equipment(self, equipment):
        """Удаляет предмет экипировки из списка по индексу."""
        if equipment in self.equipment:
            self.equipment.remove(equipment)

            # Снимаем бонус экипировки
            if equipment.equipment_type == "weapon":
                self.damage -= equipment.bonus
            elif equipment.equipment_type == "helmet":
                self.health -= equipment.bonus
            elif equipment.equipment_type == "shoes":
                self.speed -= equipment.bonus
            elif equipment.equipment_type == "amulet":
                self.max_health -= equipment.bonus
            elif equipment.equipment_type == "ring":
                self.damage -= equipment.bonus
            elif equipment.equipment_type == "cloak":
                self.armor -= equipment.bonus
            elif equipment.equipment_type == "armor":
                self.armor -= equipment.bonus

            self.remove_equipment_skills(equipment)  #  <--  Добавляем метод для удаления навыков

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

    def apply_equipment_skills(self, equipment):
        """Применяет навыки экипировки к игроку."""
        for skill in equipment.skills:
            if skill["name"] == "Вампиризм":
                self.vampirism = skill["value"]
            elif skill["name"] == "Ярость":
                self.fury = skill["value"]
            elif skill["name"] == "Регенерация":
                self.regeneration = skill["value"]
            elif skill["name"] == "Удача":
                self.luck = skill["value"]

    def remove_equipment_skills(self, equipment):
        """Удаляет навыки экипировки с игрока."""
        for skill in equipment.skills:
            if skill["name"] == "Вампиризм":
                self.vampirism = 0
            elif skill["name"] == "Ярость":
                self.fury = 0
            elif skill["name"] == "Регенерация":
                self.regeneration = 0
            elif skill["name"] == "Удача":
                self.luck = 0
    def update(self, projectile_group, enemies):
        """Обновляет состояние игрока."""
        # Проверка видимости врагов
        in_vision = any(
            enemy.rect.right < self.rect.right + self.vision_range
            for enemy in enemies
        )

        # if in_vision:
            # self.attack(projectile_group)