from flask import Flask, render_template, redirect, request, url_for

from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import Player, Enemy

app = Flask(__name__)

heroes = {
	"player": ...,
	"enemy": ...,
}

arena = Arena()


@app.route("/")
def menu_page():
	return render_template('index.html')


@app.route("/fight/")
def start_fight():
	arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
	return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
	if arena.game_is_running:
		result = arena.player_hit()
		# result = arena.next_turn()
		return render_template('fight.html', heroes=heroes, result=result)
	result = arena.battle_result
	return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
	result = arena.player.use_skill(heroes['enemy'])
	return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
	result = arena.next_turn()
	return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
	return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
	if request.method == 'GET':
		header = 'Выберите героя'
		classes = unit_classes
		weapons = Equipment().get_weapon_names()
		armors = Equipment().get_armor_names()
		result = {
			"header": header,
			"classes": classes,
			"weapons": weapons,
			"armors": armors,
		}
		return render_template('hero_choosing.html', result=result)
	if request.method == 'POST':
		name = request.form['name']
		weapon_name = request.form['weapon']
		armor_name = request.form['armor']
		unit_class = request.form['unit_class']

		player = Player(name=name, unit_class=unit_classes.get(unit_class))
		player.equip_armor(Equipment().get_armor(armor_name))
		player.equip_weapon(Equipment().get_weapon(weapon_name))
		heroes['player'] = player

		return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
	if request.method == 'GET':
		header = 'Выберите противника'
		classes = unit_classes
		weapons = Equipment().get_weapon_names()
		armors = Equipment().get_armor_names()
		result = {
			"header": header,
			"classes": classes,
			"weapons": weapons,
			"armors": armors,
		}
		return render_template('hero_choosing.html', result=result)
	if request.method == 'POST':
		name = request.form['name']
		weapon_name = request.form['weapon']
		armor_name = request.form['armor']
		unit_class = request.form['unit_class']

		enemy = Enemy(name=name, unit_class=unit_classes.get(unit_class))
		enemy.equip_armor(Equipment().get_armor(armor_name))
		enemy.equip_weapon(Equipment().get_weapon(weapon_name))
		heroes['enemy'] = enemy

		return redirect(url_for('start_fight'))


if __name__ == "__main__":
	app.run(port=8080)
