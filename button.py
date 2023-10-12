

import pygame.font

# TODO переписать класс таким образом, чтобы можно было выбирать положение создание кнопки


class Button():

    def __init__(self, ai_game, msg, position) -> None:
        """Инициализирует атрибуты кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.button_position = position

        # Назначение параметров и свойств кнопки
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        i = 0

        # Построение объекта rect кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        new_t = ()
        screen_size = self.screen_rect.size
        for size in (getattr(self.screen_rect, self.button_position)):
            if size == screen_size[i]:
                if i == 0:
                    new_t += (int(size - self.width/2),)
                else:
                    new_t += (int(size - self.height/2),)
            elif size == 0:
                if i == 0:
                    new_t += (int(size + self.width/2),)
                else:
                    new_t += (int(size + self.height/2),)
            else:
                new_t += (size,)

            i += 1

        self.rect.center = new_t

        # Сообщение кнопки создается только один раз
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру."""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Отображение пустой кнопки и вывод изображения
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
