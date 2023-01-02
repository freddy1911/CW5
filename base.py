from unit import BaseUnit


# class BaseSingleton:
# 	_instance = None
#
# 	def __new__(cls, *args, **kwargs):
# 		if cls._instance is None:
# 			cls._instance = super().__new__(cls)
# 		return cls._instance
#
# 	def __del__(self):
# 		BaseSingleton._instance = None
class BaseSingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
	STAMINA_PER_ROUND = 1
	game_is_running = False
	player = None
	enemy = None
	battle_result = None

	def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
		self.player = player
		self.enemy = enemy
		self.game_is_running = True

	def _check_players_hp(self) -> str | None:
		if self.player.hp > 0 and self.enemy.hp > 0:
			return None

		if self.player.hp <= 0 and self.enemy.hp <= 0:
			self.battle_result = "Ничья"
		elif self.player.hp <= 0:
			self.battle_result = "Игрок проиграл битву"
		elif self.enemy.hp <= 0:
			self.battle_result = "Игрок выиграл битву"

		return self._end_game()

	def _end_game(self) -> str:
		self._instance = {}
		self.game_is_running = False
		return self.battle_result

	def _stamina_regeneration(self) -> None:
		if self.player.stamina + self.STAMINA_PER_ROUND > self.player.unit_class.max_stamina:
			self.player.stamina = self.player.unit_class.max_stamina
		else:
			self.player.stamina += self.STAMINA_PER_ROUND

		if self.enemy.stamina + self.STAMINA_PER_ROUND > self.enemy.unit_class.max_stamina:
			self.enemy.stamina = self.enemy.unit_class.max_stamina
		else:
			self.enemy.stamina += self.STAMINA_PER_ROUND

	def next_turn(self) -> str | None:
		result = self._check_players_hp()
		if result is not None:
			return result
		self._stamina_regeneration()
		enemy_hit = self.enemy.hit(self.player)
		return enemy_hit

	def player_use_skill(self) -> str:
		result = self.player.use_skill(self.enemy)
		next_turn = self.next_turn()
		return f'{result}\n{next_turn}'

	def player_hit(self) -> str:
		result = self.player.hit(self.enemy)
		next_turn = self.next_turn()
		return f'{result}\n{next_turn}'
