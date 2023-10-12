import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Класс для управления кораблем"""

    def __init__(self, ai_game) -> None:
        """Инициализирует корабль и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загружаем изображение корабля и получаем прямоугольик
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        # флаг перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет прзицию корабля с учетом флагов"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor

        self.rect.x = self.x

    def blitme(self):
        """Рисует корабль в текущей позиуии"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
