import pygame
from ui.notification import Notification

class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, equipment, game):
        super().__init__()
        self.image = pygame.image.load("assets/images/chest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.equipment = equipment
        self.opened = False
        self.game = game

    def open_chest(self, player):
        """Открывает сундук и применяет бонус к игроку."""
        if not self.opened:
            self.opened = True
            player.add_equipment(self.equipment)   # <--- Добавляем экипировку к игроку
            self.kill()

            # Отображение уведомления
            notification_text = f"Вы получили {self.equipment.name}! +{self.equipment.bonus} {self.equipment.equipment_type}"
            self.game.notification_text = self.game.font.render(notification_text, True, (255, 255, 255))
            self.game.notification_rect = self.game.notification_text.get_rect(
                center=(self.game.screen_width // 2, self.game.screen_height // 2 - 50)
            )
            self.game.show_notification = True
            self.game.notification_start_time = pygame.time.get_ticks() # Запускаем таймер для уведомления

    def update(self):
        """Обрабатывает нажатие на сундук."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.open_chest(self.game.player)

    def draw(self, screen):
        """Отрисовывает сундук."""
        screen.blit(self.image, self.rect)