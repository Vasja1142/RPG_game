import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed=8, color=(255, 0, 0), shape="rect", size=(10, 5)):
        super().__init__()
        self.color = color
        self.shape = shape
        self.size = size

        if self.shape == "rect":
            self.image = pygame.Surface(self.size)
            self.image.fill(self.color)
        elif self.shape == "oval":  # <---  Добавляем поддержку овалов
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)  #  <--- Для прозрачности
            pygame.draw.ellipse(self.image, self.color, (0, 0, *self.size))

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