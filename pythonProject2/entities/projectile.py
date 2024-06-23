import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed=8):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.direction = direction

        self.hit = False  # Флаг столкновения

    def update(self):
        """Обновляет позицию снаряда"""
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

        # Проверка выхода за пределы экрана
        if not 0 <= self.rect.x <= 800 or not 0 <= self.rect.y <= 600:
            self.kill()