import pygame

class Notification:
    def __init__(self, text, x, y, width, height, color, duration=2000):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.duration = duration

        self.font = pygame.font.Font(None, 25)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )

        self.start_time = 0
        self.visible = False

    def show(self):
        """Отображает уведомление."""
        self.visible = True
        self.start_time = pygame.time.get_ticks()

    def draw(self, screen):
        """Отрисовывает уведомление."""
        if self.visible and pygame.time.get_ticks() - self.start_time < self.duration:
            pygame.draw.rect(
                screen, self.color, (self.x, self.y, self.width, self.height)
            )
            screen.blit(self.text_surface, self.text_rect)