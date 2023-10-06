class Settings():
    """Класс для хранения настроек игры Alien Invasion"""

    def __init__(self) -> None:
        """Инициализирует настройку игры"""
        # параметры экрана
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # настройки корабля
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # настройки пули
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 6

        # настройки пришельцев
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево
        self.fleet_direction = 1
