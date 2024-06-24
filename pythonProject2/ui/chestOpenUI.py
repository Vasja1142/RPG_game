import pygame
from ui.button import Button
class ChestOpenUI:
    def __init__(self, game, chest):
        self.game = game
        self.chest = chest
        self.font = pygame.font.Font(None, 20)
        self.visible = False

        # Размеры и позиция окна
        self.width = 400
        self.height = 200
        self.x = self.game.screen_width // 2 - self.width // 2
        self.y = self.game.screen_height // 2 - self.height // 2

        # Кнопки
        self.equip_button = Button(
            "Надеть",
            self.x + 50,
            self.y + self.height - 40,
            100,
            30,
            (0, 150, 0),
            (0, 255, 0),
        )
        self.swap_button = Button(
            "Поменять",
            self.x + 50,
            self.y + self.height - 40,
            100,
            30,
            (0, 100, 150),
            (0, 200, 255),
        )
        self.sell_button = Button(
            "Продать",
            self.x + self.width - 150,
            self.y + self.height - 40,
            100,
            30,
            (150, 0, 0),
            (255, 0, 0),
        )

    def draw(self):
        if self.visible:
            # Фон окна
            pygame.draw.rect(
                self.game.screen, (50, 50, 50), (self.x, self.y, self.width, self.height)
            )

            # Заголовок
            title_text = self.font.render("Сундук", True, (255, 255, 255))
            self.game.screen.blit(title_text, (self.x + 10, self.y + 10))

            # Предмет из сундука
            self.draw_equipment_info(self.chest.equipment, 1)

            # Найденный предмет такого же типа
            existing_equipment = self.game.player.get_equipment(self.chest.equipment.equipment_type)
            if existing_equipment:
                self.draw_equipment_info(existing_equipment, 2)
                self.swap_button.draw(self.game.screen)
            else:
                self.equip_button.draw(self.game.screen)

            self.sell_button.draw(self.game.screen)

    def draw_equipment_info(self, equipment, slot_number):
        y_offset = 40 + (slot_number - 1) * 70
        text = f"{slot_number}. {equipment.name} (Уровень {equipment.level})"
        equipment_text = self.font.render(text, True, (255, 255, 255))
        self.game.screen.blit(equipment_text, (self.x + 10, self.y + y_offset))


        y_offset += 30
        for i, skill in enumerate(equipment.skills):
            skill_text = self.font.render(f"{skill['name']}: +{skill['value']}", True, (255, 255, 255))
            self.game.screen.blit(skill_text, (self.x + 10, self.y + y_offset + i * 20))

    def handle_events(self, event):
        if self.visible:
            if self.equip_button.is_clicked(event):
                self.game.player.add_equipment(self.chest.equipment)
                self.chest.kill()
                self.visible = False
            elif self.swap_button.is_clicked(event):
                existing_equipment = self.game.player.get_equipment(self.chest.equipment.equipment_type)
                self.game.player.remove_equipment(existing_equipment)
                self.game.player.add_equipment(self.chest.equipment)
                self.chest.kill()
                self.visible = False
            elif self.sell_button.is_clicked(event):
                self.game.player.sell_equipment(self.chest.equipment)
                self.chest.kill()
                self.visible = False

    def show(self):
        self.visible = True