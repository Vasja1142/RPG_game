import pygame

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color

        self.font = pygame.font.Font(None, 30)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, button_rect)
        else:
            pygame.draw.rect(screen, self.color, button_rect)

        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            return button_rect.collidepoint(mouse_pos)
        return False