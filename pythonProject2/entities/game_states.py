import pygame
import random

from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from ui.button import Button

class GameState:
    """Базовый класс для всех игровых состояний."""

    def __init__(self, game):
        self.game = game

    def handle_events(self, event):
        """Обрабатывает события."""
        pass

    def update(self):
        """Обновляет логику."""
        pass

    def draw(self):
        """Отрисовывает графику."""
        pass


class MenuState(GameState):
    """Состояние главного меню."""

    def __init__(self, game):
        super().__init__(game)
        self.start_button = Button(
            "Начать игру",
            self.game.screen_width // 2 - 100,
            self.game.screen_height // 2 - 50,
            200,
            50,
            (0, 150, 0),
            (0, 255, 0),
        )

    def handle_events(self, event):
        if self.start_button.is_clicked(event):
            self.game.state = GameState(self.game)  # Переключаемся в состояние игры

    def update(self):
        pass  # Пока не требуется обновлять логику меню

    def draw(self):
        self.game.screen.blit(self.game.bg_image, (0, 0))
        self.start_button.draw(self.game.screen)

class GameState(GameState):
    """Состояние игры."""

    def __init__(self, game):
        super().__init__(game)
        self.game = game
        game.player = Player((50, 50))
        game.player_group = pygame.sprite.GroupSingle(game.player)
        game.player.equipment = [] # Инициализация списка экипировки игрока

    def handle_events(self, event):
        if self.game.show_game_over and self.game.ok_button.is_clicked(event):
            self.game.show_game_over = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Нажатие левой кнопки мыши
            mouse_pos = pygame.mouse.get_pos()
            for i, slot_pos in enumerate(self.game.equipment_slots):
                slot_rect = pygame.Rect(slot_pos[0], slot_pos[1], 50, 50)
                if slot_rect.collidepoint(mouse_pos):
                    self.game.player.remove_equipment(i)  # Снять экипировку
                    break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.player.attack(self.game.projectile_group)

    def update(self):
        self.game.player_group.update(self.game.projectile_group, self.game.enemy_group)
        self.game.enemy_group.update(self.game.enemy_projectile_group)
        self.game.projectile_group.update()
        self.game.enemy_projectile_group.update()

        self.game.handle_collisions()

        if self.game.player.health <= 0:
            self.game.game_over()

        now = pygame.time.get_ticks()
        if (
                now - self.game.last_enemy_spawn_time
                > self.game.enemy_spawn_cooldown
                and self.game.enemies_spawned < self.game.enemies_per_wave
        ):
            enemy_y = self.game.player.rect.centery - 40
            spawn_x = self.game.screen_width + random.randint(-50, 50)
            new_enemy = Enemy((spawn_x, enemy_y), self.game.level)
            self.game.enemy_group.add(new_enemy)
            self.game.enemies_spawned += 1

            self.game.last_enemy_spawn_time = now
            self.game.enemy_spawn_cooldown = random.randint(500, 1500)

        # Проверка на повышение уровня
        if self.game.player.experience >= self.game.player.level * 100:  # Условие повышения уровня
            self.game.player.level += 1
            self.game.player.experience = 0
            # ... (здесь можно добавить улучшения характеристик игрока)

    def draw(self):
        self.game.screen.blit(self.game.bg_image, (0, 0))  #  <---  Рисуем  фон  в  начале
        self.game.player_group.draw(self.game.screen)
        self.game.enemy_group.draw(self.game.screen)
        self.game.projectile_group.draw(self.game.screen)
        self.game.enemy_projectile_group.draw(self.game.screen)

        # Индикаторы здоровья
        health_label = self.game.font.render("Здоровье:", True, (255, 255, 255))
        self.game.screen.blit(health_label, (10, 10))
        self.game.draw_health_bar(self.game.player.health, 100, 10, width=150, height=15)

        for enemy in self.game.enemy_group:
            enemy_health_x = enemy.rect.centerx - 10
            self.game.draw_health_bar(enemy.health, enemy_health_x, enemy.rect.y - 15, width=30, height=5, show_text=False,
                                 max_health=enemy.max_health)

        # Отображение уровня
        level_text = self.game.font.render(f"Уровень: {self.game.level}", True, (255, 255, 255))
        self.game.screen.blit(level_text, (10, 30))

        # Отображение уровня и опыта игрока
        player_level_text = self.game.font.render(f"Уровень игрока: {self.game.player.level}", True, (255, 255, 255))
        self.game.screen.blit(player_level_text, (10, 50))
        exp_text = self.game.font.render(f"Опыт: {self.game.player.experience}", True, (255, 255, 255))
        self.game.screen.blit(exp_text, (10, 70))

        self.game.chest_group.draw(self.game.screen) # <--- Добавляем отрисовку сундуков

        # Отображение слотов экипировки:
        for i, slot_pos in enumerate(self.game.equipment_slots):
            pygame.draw.rect(self.game.screen, (100, 100, 100), (slot_pos[0], slot_pos[1], 50, 50))  # Серый фон слота

            # Отрисовка картинки экипировки
            if i < len(self.game.player.equipment):
                equipment_type = self.game.player.equipment[i].equipment_type
                if equipment_type in self.game.equipment_images:
                    image = self.game.equipment_images[equipment_type]
                    image = pygame.transform.scale(image, (50, 50))  # <--- Масштабируем изображение
                    self.game.screen.blit(image, (slot_pos[0], slot_pos[1]))  # <--- Рисуем  в  координатах  слота

        if self.game.show_game_over:
            game_over_font = pygame.font.Font(None, 50)
            game_over_text = game_over_font.render("Вы погибли!", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(
                center=(self.game.screen_width // 2, self.game.screen_height // 2)
            )
            self.game.screen.blit(game_over_text, text_rect)

            self.game.ok_button.draw(self.game.screen)