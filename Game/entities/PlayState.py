import pygame
import pygame.locals

from entities.enemy import Enemy
from entities.chest import Chest, ChestManager
from ui.inventory_UI import InventoryUI
from entities.game_states import MenuState, GameState


class PlayState(GameState):
    """Состояние игры."""

    def __init__(self, game):
        super().__init__(game)

        self.game = game
        self.game.auto_fire = True
        self.game.last_action_time = 0
        self.open_chest = None  # Добавляем атрибут для хранения ссылки на открытый сундук
        game.player = Player((50, 100), game)
        game.player_group = pygame.sprite.GroupSingle(game.player)
        game.player.equipment = []

    def handle_events(self, event):
        if self.game.show_game_over and self.game.ok_button.is_clicked(event):
            self.game.show_game_over = False  #  Сбрасываем флаг после нажатия OK
            self.game.player.health = self.game.MAX_HEALTH  #  Возвращаем здоровье игрока


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.player.attack(self.game.projectile_group)
                self.game.last_action_time = pygame.time.get_ticks()
                self.game.auto_fire = False

        # Открываем/закрываем инвентарь по нажатию клавиши "I"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                print("Нажата клавиша I в PlayState")
                self.game.inventory_ui.toggle_visibility()

        self.game.inventory_ui.handle_events(event)

        chest = None
        for chest in self.game.chest_group:
            if chest.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    chest.open_chest()
                    self.open_chest = chest
                    break

        if self.open_chest and hasattr(self.open_chest, 'chest_open_ui'):
            if self.open_chest.chest_open_ui.sell_button.is_clicked(event):
                # ... (логика продажи)
                self.open_chest.chest_open_ui.visible = False  # Закрываем окно с сундуком
                self.open_chest = None

            self.open_chest.chest_open_ui.handle_events(event)

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

        if self.game.player.experience >= self.game.player.level * 100:
            self.game.player.level += 1
            self.game.player.experience = 0

        # --- Проверка простоя и автоматическая стрельба ---
        time_since_last_action = pygame.time.get_ticks() - self.game.last_action_time

        # Автоматическая стрельба, если враги в поле зрения
        in_vision = any(
            enemy.rect.right < self.game.player.rect.right + self.game.player.vision_range
            for enemy in self.game.enemy_group
        )

        if self.game.auto_fire and in_vision:
            self.game.player.attack(self.game.projectile_group)

        # Переключение в автоматический режим после простоя
        elif not self.game.auto_fire and time_since_last_action > 5000:
            self.game.auto_fire = True

    def draw(self):
        self.game.screen.blit(self.game.bg_image, (0, 0))
        self.game.player_group.draw(self.game.screen)
        self.game.enemy_group.draw(self.game.screen)
        self.game.projectile_group.draw(self.game.screen)
        self.game.enemy_projectile_group.draw(self.game.screen)

        health_label = self.game.font.render("Здоровье:", True, (255, 255, 255))
        self.game.screen.blit(health_label, (10, 10))
        # Шкала здоровья и опыта игрока
        self.game.draw_health_bar(
            self.game.player.health,
            100,
            10,
            width=150,
            height=15,
            experience=self.game.player.experience,  # Добавляем опыт
            max_experience=self.game.player.level * 100  # Максимальный опыт для текущего уровня
        )
        for enemy in self.game.enemy_group:
            enemy_health_x = enemy.rect.centerx - 10
            self.game.draw_health_bar(enemy.health, enemy_health_x, enemy.rect.y - 15, width=30, height=5,
                                      show_text=False, max_health=enemy.max_health)

        # Уровень игрока
        player_level_text = self.game.font.render(f"Уровень: {self.game.player.level}", True,
                                               (255, 255, 255))  # Меняем надпись
        self.game.screen.blit(player_level_text, (10, 30))

        gold_text = self.game.font.render(f"Золото: {self.game.player.gold}", True, (255, 255, 255))  # Новая строка
        self.game.screen.blit(gold_text, (10, 50))  # Новая строка

        # Подземелье
        dungeon_font = pygame.font.Font(None, 30)  # Создаем шрифт большего размера (например, 40)
        dungeon_text = dungeon_font.render(f"Подземелье: {self.game.level}", True, (255, 255, 255))
        text_rect = dungeon_text.get_rect(center=(self.game.screen_width // 2, 30))
        self.game.screen.blit(dungeon_text, text_rect)



        self.game.chest_group.draw(self.game.screen)

        for equipment_type, slot_pos in self.game.equipment_slots.items():
            pygame.draw.rect(self.game.screen, (100, 100, 100), (slot_pos[0], slot_pos[1], 50, 50))

            for equipment in self.game.player.equipment:
                if equipment.equipment_type == equipment_type:
                    image = self.game.equipment_images[equipment_type]
                    image = pygame.transform.scale(image, (50, 50))
                    self.game.screen.blit(image, (slot_pos[0], slot_pos[1]))
                    break

        if self.game.show_game_over:
            game_over_font = pygame.font.Font(None, 50)
            game_over_text = game_over_font.render("Вы  погибли!", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(
                center=(self.game.screen_width // 2, self.game.screen_height // 2)
            )
            self.game.screen.blit(game_over_text, text_rect)

            self.game.ok_button.draw(self.game.screen)

        self.game.inventory_ui.draw()  # <--  Добавьте эту строку, если её нет

        for chest in self.game.chest_group:
            if hasattr(chest, 'chest_open_ui'):
                chest.chest_open_ui.draw()