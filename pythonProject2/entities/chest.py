import pygame
from ui.chestOpenUI import ChestOpenUI  #  Импортируем класс ChestOpenUI

class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, equipment, game):
        super().__init__()
        self.image = pygame.image.load("assets/images/chest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.equipment = equipment
        self.opened = False
        self.game = game


    def open_chest(self):
        """Открывает сундук и показывает UI."""
        self.chest_open_ui = ChestOpenUI(self.game, self)
        self.chest_open_ui.show()

    def update(self):
        """Обрабатывает нажатие на сундук."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.open_chest()

    def draw(self, screen):
        """Отрисовывает сундук."""
        screen.blit(self.image, self.rect)

class ChestManager:
    def __init__(self):
        self.chest_level = 1  # Начальный уровень сундука

    def upgrade_chest(self, cost):
        """Повышает уровень сундука, если хватает денег."""
        if player.gold >= cost:  # Предполагаем, что у игрока есть атрибут gold
            player.gold -= cost
            self.chest_level += 1

    def create_chest(self, game):
        """Создает сундук с предметом, уровень которого зависит от уровня сундука."""
        new_equipment = game.get_random_equipment()
        new_equipment.level = self.chest_level  # Уровень предмета = уровень сундука
        new_chest = Chest(game.screen_width // 2 - 25, game.screen_height // 2 - 25, new_equipment, game)
        game.chest_group.add(new_chest)