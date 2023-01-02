import json
from dataclasses import dataclass
import marshmallow
import marshmallow_dataclass
import random

from constants import EQUIPMENT


@dataclass
class Weapon:
	id: int
	name: str
	min_damage: float
	max_damage: float
	stamina_per_hit: float

	@property
	def damage(self):
		return round(random.uniform(self.min_damage, self.max_damage), 1)


@dataclass
class Armor:
	id: int
	name: str
	defence: float
	stamina_per_turn: float


@dataclass
class EquipmentData:
	weapons: list[Weapon]
	armors: list[Armor]


class Equipment:
	def __init__(self):
		self.equipment = self._get_data()

	def get_weapon(self, weapon_name) -> Weapon:
		for weapon in self.equipment.weapons:
			if weapon.name == weapon_name:
				return weapon

	def get_armor(self, armor_name) -> Armor:
		for armor in self.equipment.armors:
			if armor.name == armor_name:
				return armor

	def get_weapon_names(self) -> list[str]:
		result_list = []
		for weapon in self.equipment.weapons:
			result_list.append(weapon.name)
		return result_list

	def get_armor_names(self) -> list[str]:
		result_list = []
		for armor in self.equipment.armors:
			result_list.append(armor.name)
		return result_list

	@staticmethod
	def _get_data() -> EquipmentData:
		with open(EQUIPMENT, 'r', encoding='utf-8') as file:
			data = json.load(file)
			equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
			try:
				return equipment_schema().load(data)
			except marshmallow.ValidationError:
				raise ValueError
