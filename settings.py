class Settings():
    """Класс для хранения настроек игры Alien Invasion"""

    def __init__(self) -> None:
        """Инициализирует настройку игры"""
        # параметры экрана
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5

        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
