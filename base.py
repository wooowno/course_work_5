from typing import Optional

from unit import PlayerUnit, EnemyUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit) -> None:
        """ Помещение игрока и врага на арену. Запуск игры """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """ Проверка здоровья игрока и врага """

        if self.player.hp <= 0 or self.enemy.hp <= 0:
            return self._end_game()

    def _stamina_regeneration(self) -> None:
        """ Восстановление выносливости """
        self.player.stamina_recover(self.STAMINA_PER_ROUND)
        self.enemy.stamina_recover(self.STAMINA_PER_ROUND)

    def next_turn(self) -> str:
        """ Проверка здоровья персонажей. Ход врага """
        result = self._check_players_hp()
        if result:
            return result

        self._stamina_regeneration()
        return self.enemy.hit(self.player)

    def _end_game(self) -> str:
        """ Завершение игры. Итог игры """
        self._instances = {}
        self.game_is_running = False

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            return 'Ничья'
        elif self.player.hp > 0:
            return 'Игрок выиграл битву'
        else:
            return 'Игрок проиграл битву'

    def player_hit(self) -> tuple[str, str]:
        """ Кнопка удар игрока """

        hit_res = self.player.hit(self.enemy)
        enemy_res = self.next_turn()
        return hit_res, enemy_res

    def player_use_skill(self) -> tuple[str, str]:
        """ Кнопка игрока использовать умение """

        skill_res = self.player.use_skill(self.enemy)
        enemy_res = self.next_turn()
        return skill_res, enemy_res
