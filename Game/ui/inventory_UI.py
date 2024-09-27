import pygame

from ui.button import Button

class InventoryUI:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 20)
        self.visible = False  # Инвентарь по умолчанию скрыт
        self.selected_index = None

        # Размеры и позиция окна инвентаря
        self.width = 300
        self.height = 200
        self.x = self.game.screen_width // 2 - self.width // 2
        self.y = self.game.screen_height // 2 - self.height // 2

        # Кнопка "Продать"
        self.sell_button = Button(
            "Продать",
            self.x + self.width - 80,
            self.y + self.height - 30,
            70,
            25,
            (150, 0, 0),
            (255, 0, 0),
        )

    def draw(self):
        if self.visible:
            # Фон окна инвентаря
            pygame.draw.rect(
                self.game.screen, (50, 50, 50), (self.x, self.y, self.width, self.height)
            )

            # Заголовок
            title_text = self.font.render("Инвентарь", True, (255, 255, 255))
            self.game.screen.blit(title_text, (self.x + 10, self.y + 10))

            # Отображение предметов в инвентаре
            y_offset = 40
            for i, equipment in enumerate(self.game.player.equipment):
                text = f"{i + 1}. {equipment.name} (Уровень {equipment.level})"
                equipment_text = self.font.render(text, True, (255, 255, 255))

                # Выделение выбранного предмета
                if i == self.selected_index:
                    pygame.draw.rect(self.game.screen, (100, 100, 100),
                                     (self.x + 10, self.y + y_offset - 5, self.width - 90, 25))

                self.game.screen.blit(equipment_text, (self.x + 10, self.y + y_offset))
                y_offset += 25

            # Кнопка "Продать"
            self.sell_button.draw(self.game.screen)

    def handle_events(self, event):
        if self.visible:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.selected_index = self.get_selected_equipment_index()  # Выбор предмета по клику

            # Обработка нажатия на кнопку "Продать"
            if self.sell_button.is_clicked(event) and self.selected_index is not None:
                # Продаем выбранный предмет из инвентаря
                equipment_to_sell = self.game.player.equipment[self.selected_index]
                self.game.player.sell_equipment(equipment_to_sell)
                self.selected_index = None  # Сбрасываем выбор после продажи

    def get_selected_equipment_index(self):
        """Возвращает индекс выбранного предмета в инвентаре (начиная с 0) или None, если ничего не выбрано."""
        mouse_pos = pygame.mouse.get_pos()
        y_offset = 40
        for i in range(len(self.game.player.equipment)):
            item_rect = pygame.Rect(self.x + 10, self.y + y_offset, self.width - 90, 25)
            if item_rect.collidepoint(mouse_pos):
                return i
            y_offset += 25
        return None

    def toggle_visibility(self):
        """Переключает видимость инвентаря."""
        print("Вызов toggle_visibility")  # Отладочная печать
        self.visible = not self.visible