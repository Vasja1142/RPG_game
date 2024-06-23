import random
import pygame
from entities.projectile import Projectile


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, level): # Добавляем level в конструктор Enemy
        super().__init__()
        self.image = pygame.image.load("assets/images/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 90))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 1
        self.max_health = 50 + (level * 5)  # Сохраняем максимальное здоровье
        self.health = self.max_health
        self.attack_cooldown = 500
        self.last_attack_time = 0
        self.attack_distance = random.randint(595, 605)
        self.damage = 10 + (level * 2)  # Увеличиваем урон с уровнем

    def attack(self, projectile_group):
        """Атакует игрока снарядом."""
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            # Направление всегда влево (-1, 0)
            direction = pygame.math.Vector2(-1, 0)

            projectile = Projectile(self.rect.center, direction)
            projectile_group.add(projectile)
            self.last_attack_time = now

    def update(self, projectile_group):
        """Обновляет состояние врага."""

        if self.rect.right > self.attack_distance and self.speed > 0:
            # Движение влево, только если скорость не равна 0
            self.rect.x -= self.speed
        else:
            # Остановить движение
            self.speed = 0
            # Атака
            self.attack(projectile_group)