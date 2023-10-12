import os


class GameStats():
    """Отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_game) -> None:
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        # игра Alien Invasion запускается в активном состоянии
        self.game_active = False
        # Рекорд не должен сбразываться
        if os.path.exists("record.txt"):
            with open("record.txt", "r") as f:
                self.high_score = int(f.readline())
        else:
            self.high_score = 0

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюса в ходе игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
