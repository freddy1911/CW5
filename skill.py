import random
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Skill(ABC):
	user = None
	target = None

	@property
	@abstractmethod
	def name(self):
		pass

	@property
	@abstractmethod
	def damage(self):
		pass

	@property
	@abstractmethod
	def stamina(self):
		pass

	@abstractmethod
	def skill_effect(self):
		pass

	def _is_stamina_enough(self) -> bool:
		return self.user.stamina >= self.stamina

	def use(self, user, target) -> str:
		self.user = user
		self.target = target
		if self._is_stamina_enough():
			return self.skill_effect()
		else:
			return f'{self.user.name} попытался использовать {self.name}, но у него не хватило выносливости.'


class FuryKick(Skill):
	name = "Свирепый пинок"
	stamina = 6
	damage = 12

	def skill_effect(self) -> str:
		self.user.stamina -= self.stamina
		if self.damage > self.target.hp:
			self.target.hp = 0
		else:
			self.target.hp -= self.damage
		return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику.'


class DeadlyPrick(Skill):
	name = "Смертельный укол"
	stamina = 5
	damage = 15

	def skill_effect(self) -> str:
		if random.randint(0, 100) < 8:
			self.damage *= 2

		self.user.stamina -= self.stamina
		if self.damage > self.target.hp:
			self.target.hp = 0
		else:
			self.target.hp -= self.damage

		return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику.'