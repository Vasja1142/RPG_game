import pygame
import random

from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from ui.button import Button
from entities.game_states import MenuState, GameState
from entities.chest import Chest
from entities.equipment import Equipment

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Legend of Mushroom")
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load("assets/images/background.png").convert()

        self.player = Player((50, 50))
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.enemy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.enemy_projectile_group = pygame.sprite.Group()
        self.chest_group = pygame.sprite.Group()

        self.font = pygame.font.Font(None, 20)
        self.MAX_HEALTH = 100

        self.last_enemy_spawn_time = 0
        self.enemy_spawn_cooldown = random.randint(500, 1500)

        self.level = 1
        self.enemies_per_wave = random.randint(7, 10)
        self.enemies_spawned = 0
        self.enemies_killed = 0

        self.show_game_over = False
        self.ok_button = Button(
            "OK",
            self.screen_width // 2 - 50,
            self.screen_height // 2 + 50,
            100,
            40,
            (150, 0, 0),
            (255, 0, 0),
        )

        # Список с описанием доступной экипировки
        self.equipment_list = [
            Equipment("Меч", "weapon", 5),  # +5 к урону
            Equipment("Шлем", "helmet", 10),  # +10 к здоровью
            Equipment("Сапоги", "shoes", 1),  # +1 к скорости
            Equipment("Амулет", "amulet", 5),  # +5 к max_health
            Equipment("Кольцо", "ring", 3),  # +3 к урону
            Equipment("Накидка", "cloak", 2),  # +2 к защите
            Equipment("Доспехи", "armor", 15),  # +15 к защите
            # ... (добавить больше предметов)
        ]

        self.equipment_slots = [
            (10, self.screen_height - 50),  # Оружие
            (80, self.screen_height - 50),  # Шлем
            (150, self.screen_height - 50),  # Обувь
            (220, self.screen_height - 50),  # Амулет
            (290, self.screen_height - 50),  # Кольцо
            (360, self.screen_height - 50),  # Накидка
            (430, self.screen_height - 50),  # Доспехи
            # ... (добавить больше слотов)
        ]

        # Картинки для экипировки
        self.equipment_images = {
            "weapon": pygame.image.load("assets/images/sword.png").convert_alpha(),
            "helmet": pygame.image.load("assets/images/helmet.png").convert_alpha(),
            "shoes": pygame.image.load("assets/images/shoes.png").convert_alpha(),
            "amulet": pygame.image.load("assets/images/amulet.png").convert_alpha(),
            "ring": pygame.image.load("assets/images/ring.png").convert_alpha(),
            "cloak": pygame.image.load("assets/images/cloak.png").convert_alpha(),
            "armor": pygame.image.load("assets/images/armor.png").convert_alpha(),  # Картинка для доспехов
            # ... (добавить больше картинок)
        }

        self.state = MenuState(self)

        self.show_notification = False

    def draw_health_bar(self, health, x, y, width=50, height=10, show_text=True, max_health=100):
        """Рисует полоску здоровья."""
        health_ratio = health / max_health
        green_width = int(width * health_ratio)

        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, green_width, height))
        pygame.draw.rect(self.screen, (255, 0, 0), (x + green_width, y, width - green_width, height))

        if show_text:
            health_text = self.font.render(f"{health}", True, (0, 0, 0))
            text_rect = health_text.get_rect(center=(x + width // 2, y + height // 2))
            self.screen.blit(health_text, text_rect)

    def next_level(self):
        self.level += 1
        self.enemies_per_wave = random.randint(7, 10)
        self.enemies_spawned = 0
        self.enemies_killed = 0
        self.enemy_spawn_cooldown = max(300, self.enemy_spawn_cooldown - 100)

        # Даем сундук с экипировкой при переходе на новый уровень
        new_equipment = self.get_random_equipment()
        new_chest = Chest(self.screen_width // 2 - 25, self.screen_height // 2 - 25, new_equipment, self)
        self.chest_group.add(new_chest)

    def get_random_equipment(self):
        """Выбирает случайный предмет экипировки из списка."""
        return random.choice(self.equipment_list)

    def handle_collisions(self):
        """Обрабатывает столкновения."""
        # Столкновения снарядов игрока и врагов
        for projectile in self.projectile_group:
            collided_enemies = pygame.sprite.spritecollide(projectile, self.enemy_group, False)
            for enemy in collided_enemies:
                enemy.health -= 10
                projectile.kill()
                if enemy.health <= 0:
                    enemy.kill()
                    self.enemies_killed += 1
                    self.player.experience += 10  # Добавляем опыт за убийство врага
                    if self.enemies_killed >= self.enemies_per_wave:
                        self.next_level()

        # Столкновения снарядов врагов и игрока
        for projectile in self.enemy_projectile_group:
            if pygame.sprite.spritecollide(
                projectile, self.player_group, False
            ):
                for enemy in self.enemy_group:
                    if projectile.rect.colliderect(self.player.rect):
                        self.player.health -= enemy.damage
                        projectile.kill()
                        break

    def game_over(self):
        """Понижает уровень и активирует уведомление."""
        self.level = max(1, self.level - 1)
        self.player.health = self.MAX_HEALTH
        self.enemies_per_wave = random.randint(7, 10)
        self.enemies_spawned = 0
        self.enemies_killed = 0
        self.enemy_spawn_cooldown = 1500

        self.show_game_over = True

    def draw(self):
        """Отрисовывает все элементы игры."""
        self.screen.blit(self.bg_image, (0, 0))
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.projectile_group.draw(self.screen)
        self.enemy_projectile_group.draw(self.screen)

        # Индикаторы здоровья
        health_label = self.font.render("Здоровье:", True, (255, 255, 255))
        self.screen.blit(health_label, (10, 10))
        self.draw_health_bar(self.player.health, 100, 10, width=150, height=15)

        for enemy in self.enemy_group:
            enemy_health_x = enemy.rect.centerx - 10
            self.draw_health_bar(enemy.health, enemy_health_x, enemy.rect.y - 15, width=30, height=5, show_text=False,
                                 max_health=enemy.max_health)

        # Отображение уровня
        level_text = self.font.render(f"Уровень: {self.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 30))

        # Отображение уровня и опыта игрока
        player_level_text = self.font.render(f"Уровень игрока: {self.player.level}", True, (255, 255, 255))
        self.screen.blit(player_level_text, (10, 50))
        exp_text = self.font.render(f"Опыт: {self.player.experience}", True, (255, 255, 255))
        self.screen.blit(exp_text, (10, 70))

        # Отображение слотов экипировки
        for i, slot_pos in enumerate(self.equipment_slots):
            pygame.draw.rect(self.screen, (100, 100, 100), (slot_pos[0], slot_pos[1], 50, 50))  # Серый фон слота

            # Отрисовка картинки экипировки
            if i < len(self.player.equipment):
                equipment_type = self.player.equipment[i].equipment_type
                if equipment_type in self.equipment_images:
                    self.screen.blit(self.equipment_images[equipment_type], (slot_pos[0], slot_pos[1]))

        # Отображение уведомлений
        if self.show_notification:
            self.screen.blit(self.notification_text, self.notification_rect)

    def run(self):
        """Запуск игрового цикла"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.state.handle_events(event)

            self.state.update()
            self.state.draw()

            self.chest_group.update()
            self.chest_group.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()