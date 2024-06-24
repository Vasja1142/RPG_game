import pygame
import pygame.locals  # Добавьте эту строку, если её нет
import random

from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from ui.button import Button
from ui.inventory_UI import InventoryUI
from entities.game_states import MenuState, GameState
from entities.chest import Chest
from entities.chest import ChestManager
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
        self.inventory_ui = InventoryUI(self)  # Создаем объект InventoryUI

        self.auto_fire = True  # По умолчанию автоматическая стрельба включена

        self.player = Player((50, 50), self)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.enemy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.enemy_projectile_group = pygame.sprite.Group()
        self.chest_group = pygame.sprite.Group()
        self.chest_manager = ChestManager()

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

        # Слоты для экипировки (3x2)
        self.equipment_slots = {
            "helmet": (100, self.screen_height - 300),  # Шлем  -  выше
            "armor": (100, self.screen_height - 200),  # Доспехи
            "shoes": (100, self.screen_height - 100),  # Сапоги
            "cloak": (200, self.screen_height - 300),  # Плащ  -  дальше  по  горизонтали
            "amulet": (200, self.screen_height - 200),  # Амулет
            "ring": (200, self.screen_height - 100),  # Кольцо
            "weapon": (300, self.screen_height - 200)
        }

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
        self.notification_text = None
        self.notification_rect = None
        self.notification_duration = 2000 # Время отображения уведомления
        self.last_action_time = pygame.time.get_ticks()

    def draw_health_bar(self, health, x, y, width=50, height=10, show_text=True, max_health=100, experience=0,
                        max_experience=100):
        """Рисует полоску здоровья и опыта."""
        health_ratio = health / max_health
        green_width = int(width * health_ratio)

        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, green_width, height))
        pygame.draw.rect(self.screen, (255, 0, 0), (x + green_width, y, width - green_width, height))

        if show_text:
            health_text = self.font.render(f"{health}", True, (0, 0, 0))
            text_rect = health_text.get_rect(center=(x + width // 2, y + height // 2))
            self.screen.blit(health_text, text_rect)

        exp_ratio = experience / max_experience if max_experience > 0 else 0  # Избегаем деления на ноль
        blue_width = int(width * exp_ratio)

        pygame.draw.rect(self.screen, (0, 0, 255), (x, y + height + 5, blue_width, height))
        pygame.draw.rect(self.screen, (100, 100, 100), (x + blue_width, y + height + 5, width - blue_width, height))

        if show_text:
            exp_text = self.font.render(f"{experience}/{max_experience}", True, (0, 0, 0))
            text_rect = exp_text.get_rect(
                center=(x + width // 2, y + height + 5 + height // 2))  # Центрируем текст по шкале опыта
            self.screen.blit(exp_text, text_rect)

    def next_level(self):
        self.level += 1
        self.enemies_per_wave = random.randint(7, 10)
        self.enemies_spawned = 0
        self.enemies_killed = 0
        self.enemy_spawn_cooldown = max(300, self.enemy_spawn_cooldown - 100)

        # Даем сундук с экипировкой при переходе на новый уровень
        new_equipment = self.get_random_equipment()
        new_chest = Chest(self.screen_width // 2 - 25, self.screen_height // 2 - 25 , new_equipment, self)
        self.chest_group.add(new_chest)

    def get_random_equipment(self):
        """Выбирает случайный предмет экипировки из списка и устанавливает уровень."""
        equipment = random.choice(self.equipment_list)
        equipment.level = max(1, self.player.level)
        return equipment

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

    def run(self):
        """Запуск игрового цикла"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.state.handle_events(event)

            # Обновляем время последнего действия только для клавиш движения
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.last_action_time = pygame.time.get_ticks()

            self.state.update()

            self.screen.blit(self.bg_image, (0, 0))  # <--  Очистка  фона
            self.player_group.draw(self.screen)
            self.enemy_group.draw(self.screen)
            self.projectile_group.draw(self.screen)
            self.enemy_projectile_group.draw(self.screen)

            self.chest_group.update()
            self.chest_group.draw(self.screen)  # <--  Рисуем  сундуки

            self.state.draw()  # <--  Затем  отрисовываем  элементы  состояния  игры


            # Отображаем уведомление, если оно есть
            if self.show_notification:
                if pygame.time.get_ticks() - self.notification_start_time >= self.notification_duration:
                    self.show_notification = False  # Скрываем уведомление
                else:
                    self.screen.blit(self.notification_text, self.notification_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()