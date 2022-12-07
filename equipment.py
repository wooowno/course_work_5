from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    name: str
    defence: float
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Weapon:
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        for weapon in self.equipment.weapons:
            if weapon_name == weapon.name:
                return weapon

    def get_armor(self, armor_name) -> Armor:
        for armor in self.equipment.armors:
            if armor_name == armor.name:
                return armor

    def get_weapons_names(self) -> list:
        weapons_names = [weapon.name for weapon in self.equipment.weapons]
        return weapons_names

    def get_armors_names(self) -> list:
        armors_names = [armor.name for armor in self.equipment.armors]
        return armors_names

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open("./data/equipment.json", encoding='utf-8') as file:
            data = json.load(file)

        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)

        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
