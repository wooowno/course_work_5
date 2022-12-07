from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint

from equipment import Weapon, Armor
from classes import UnitClass
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = Weapon("", 0, 0, 0)
        self.armor = Armor("", 0, 0)
        self._is_skill_used = False

    @property
    def health_points(self):
        self.hp = round(self.hp, 1)
        return self.hp

    @property
    def stamina_points(self):
        self.stamina = round(self.stamina, 1)
        return self.stamina

    def equip_weapon(self, weapon: Weapon):
        """ Экипировка оружия """
        self.weapon: Weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        """ Экипировка брони """
        self.armor: Armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        """ Подсчёт урона """
        damage = self.unit_class.attack * self.weapon.damage
        self.stamina -= self.weapon.stamina_per_hit

        if target.stamina >= target.armor.stamina_per_turn:
            damage = damage - target.armor.defence
            target.stamina -= target.armor.stamina_per_turn

        damage = round(damage, 1)

        target.get_damage(damage)

        return damage

    def get_damage(self, damage: float) -> Optional[float]:
        """ Получение урона (уменьшение здоровья) """
        if damage > 0:
            self.hp -= damage
        return damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """ Метод использования умения. """

        if self._is_skill_used:
            return 'Навык использован'

        self._is_skill_used = True

        return self.unit_class.skill.use(user=self, target=target)

    def stamina_recover(self, stamina_pre_round) -> None:
        """ Восстановление выносливости """
        self.stamina += self.unit_class.stamina * stamina_pre_round
        self.stamina = round(self.stamina, 1)

        if self.stamina > self.unit_class.max_stamina:
            self.stamina = self.unit_class.max_stamina


class PlayerUnit(BaseUnit):
    """
    Класс игрока
    """

    def hit(self, target: BaseUnit) -> str:
        """ Удар игрока """
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)

        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):
    """
    Класс врага
    """

    def hit(self, target: BaseUnit) -> str:
        """ Удар соперника """

        if not self._is_skill_used and randint(1, 10) == 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)

        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
        else:
            f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."




