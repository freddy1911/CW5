import random
from abc import ABC, abstractmethod
from typing import Optional

from classes import UnitClass
from equipment import Weapon, Armor


class BaseUnit(ABC):
	def __init__(self, name: str, unit_class: UnitClass):
		self.name = name
		self.unit_class = unit_class
		self.hp = unit_class.max_health
		self.stamina = unit_class.max_stamina
		self.weapon = ...
		self.armor = ...
		self.is_skill_used = False

	@property
	def health_points(self):
		return round(self.hp, 1)

	@property
	def stamina_points(self):
		return round(self.stamina, 1)

	def equip_weapon(self, weapon: Weapon) -> str:
		self.weapon = weapon
		return f"{self.name} экипирован оружием {self.weapon.name}"

	def equip_armor(self, armor: Armor) -> str:
		self.armor = armor
		return f"{self.name} экипирован броней {self.armor.name}"

	def count_damage(self, target) -> int:

		self.stamina -= self.weapon.stamina_per_hit
		damage = self.weapon.damage * self.unit_class.attack

		# Check if target's stamina enough to use armor
		if target.stamina >= target.armor.stamina_per_turn * target.unit_class.stamina:
			target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
			damage -= target.armor.defence * target.unit_class.armor

		damage = round(damage, 1)

		target.get_damage(damage)

		return damage

	def get_damage(self, damage: int) -> int | None:
		if damage <= 0:
			return None
		if damage > self.hp:
			self.hp = 0
		else:
			self.hp -= damage
		return self.hp

	def use_skill(self, target) -> str:
		if self.is_skill_used:
			return 'Навык использован'
		self.is_skill_used = True
		return self.unit_class.skill.use(user=self, target=target)

	@abstractmethod
	def hit(self, target):
		pass


class Player(BaseUnit):

	def hit(self, target: BaseUnit) -> str:

		if self.stamina < self.weapon.stamina_per_hit:
			return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
		damage = self.count_damage(target)
		if damage > 0:
			return (f"{self.name} используя {self.weapon.name}"
			        f" пробивает {target.armor.name} соперника и наносит {damage} урона.")
		return (f"{self.name} используя {self.weapon.name} наносит "
		        f"удар, но {target.armor.name} cоперника его останавливает.")


class Enemy(BaseUnit):

	def hit(self, target: BaseUnit) -> str:

		if not self.is_skill_used and self.stamina >= self.unit_class.skill.stamina and random.randint(0, 100) < 10:
			return self.use_skill(target)

		if self.stamina < self.weapon.stamina_per_hit:
			return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

		damage = self.count_damage(target)
		if damage > 0:
			return (
				f"{self.name} используя {self.weapon.name} пробивает"
			        f" {target.armor.name} и наносит Вам {damage} урона."
			)
		return (
			f"{self.name} используя {self.weapon.name} наносит удар,"
		        f" но Ваш(а) {target.armor.name} его останавливает."
		)
