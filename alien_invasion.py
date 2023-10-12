import sys
import os
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self) -> None:
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode(
        #     (0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Создание кнопки Play
        self.play_button = Button(self, "Play", "center")
        # bottom left, bottom, bottom_rigth
        self.easy_diff_button = Button(self, "Minimal", "bottomleft")
        self.medium_diff_button = Button(self, "Medium", "midbottom")
        self.hard_diff_button = Button(self, "Hard", "bottomright")

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            if self.stats.game_active == True:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _update_aliens(self):
        """Проверяет достиг ли флот края экрана,
        с последующим обновлением позиций всех пришельцев
        """
        self._check_fleet_edges()
        self.aliens.update()

        # проверка коллизий пришелец корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # проверить добрались ли пришельцы до края экрана
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            # уменьшение ships_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_events(self):
        # отслеживание события клавы и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event=event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event=event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)
# TODO починить сохранение счета

    def save_high_score(self):
        record = 0
        if os.path.exists("record.txt"):
            with open("record.txt", "r") as f:
                record = int(f.readline())
                if self.stats.high_score > record:
                    record = str(self.stats.high_score)

            if type(record) == str:
                with open("record.txt", "w") as f:
                    f.write(record)
        else:
            with open("record.txt", "w") as f:
                f.write(str(self.stats.high_score))

    def _check_difficulty_buttons(self, mouse_pos):
        if not self.stats.game_active:
            button_clicked = self.easy_diff_button.rect.collidepoint(mouse_pos)
            if button_clicked:
                self.settings.speedup_scale = 1.1
                self.start_game()
                return
            button_clicked = self.medium_diff_button.rect.collidepoint(
                mouse_pos)
            if button_clicked:
                self.settings.speedup_scale = 1.25
                self.start_game()
                return
            button_clicked = self.hard_diff_button.rect.collidepoint(mouse_pos)
            if button_clicked:
                self.settings.speedup_scale = 1.4
                self.start_game()
                return

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.start_game()

    def start_game(self):
        """Программа запуска очередной сессии при включенной игре"""

        # Сброс игровых настроек
        self.settings.initialize_dynamic_settings()

        # Сброс игровой статистики
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Очистка списка пришельцев и снарядов
        self.aliens.empty()
        self.bullets.empty()

        # Создание нового флота и размещение корабля в центре
        self._create_fleet()
        self.ship.center_ship()

        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            # переместить корабль вправо
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self.start_game()
        elif event.key == pygame.K_r and self.stats.game_active:
            self.start_game()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавишь"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        # обновление позиций снарядов
        self.bullets.update()

        # удаление снарядов, вышедших за экран
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Обработка коллизий снарядов с пришеьцами"""
        # Удаление снарядов и пришельцев

        # проверка попааданий в пришельцев
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        # при каждом проходе цикла перерисовывает экран
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Вывод информации о счете
        self.sb.show_score()

        # кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_diff_button.draw_button()
            self.medium_diff_button.draw_button()
            self.hard_diff_button.draw_button()

        # отображение последнего отрисованного экрана
        pygame.display.flip()

    def _create_fleet(self):
        """Создание флота вторжения"""
        # Создание пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             3*alien_height - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Создание пришельца и размещение в ряду
                self._create_alien(alien_number=alien_number,
                                   row_number=row_number)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление экрана"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        """Создание прищельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_aliens_bottom(self):
        """проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # происходит то же что и при столкновении пришельца с кораблем
                self._ship_hit()
                break


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
