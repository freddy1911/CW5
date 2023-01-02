from dataclasses import dataclass
from skill import Skill, FuryKick, DeadlyPrick


@dataclass
class UnitClass:
	name: str
	max_health: float
	max_stamina: float
	attack: float
	stamina: float
	armor: float
	skill: Skill


Warrior = UnitClass('Воин', 60, 30, 0.8, 0.9, 1.2, FuryKick())
Theif = UnitClass('Вор', 50, 25, 1.5, 1.2, 1, DeadlyPrick())

unit_classes = {
	Warrior.name: Warrior,
	Theif.name: Theif,
}