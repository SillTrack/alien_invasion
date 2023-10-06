class GameStats():
    """Отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_game) -> None:
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        # игра Alien Invasion запускается в активном состоянии
        self.game_active = True

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюса в ходе игры"""
        self.ships_left = self.settings.ship_limit
