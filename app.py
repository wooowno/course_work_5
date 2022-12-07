from flask import Flask, request, render_template, redirect

from unit import PlayerUnit, EnemyUnit
from classes import unit_classes
from equipment import Equipment
from base import Arena

app = Flask(__name__)

heroes = {}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(heroes['player'], heroes['enemy'])
    return render_template('fight.html', heroes=heroes, result='Бой начался!')


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
    return render_template('fight.html', heroes=heroes, result=result[0], battle_result=result[1])


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
    return render_template('fight.html', heroes=heroes, result=result[0], battle_result=result[1])


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
    return render_template('fight.html', heroes=heroes, result='Вы пропустили ход', battle_result=result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html")


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    equipment = Equipment()

    if request.method == 'GET':
        result = {
            "header": 'Выберите героя',
            "classes": unit_classes.keys(),
            "weapons": equipment.get_weapons_names(),
            "armors": equipment.get_armors_names()
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        req_form = request.form
        name = req_form.get('name')
        unit_class = unit_classes[req_form.get('unit_class')]

        player = PlayerUnit(name=name, unit_class=unit_class)
        player.equip_armor(equipment.get_armor(req_form.get('armor')))
        player.equip_weapon(equipment.get_weapon(req_form.get('weapon')))

        heroes['player'] = player

        return redirect("/choose-enemy/", code=302)


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    equipment = Equipment()

    if request.method == 'GET':
        result = {
            "header": 'Выберите врага',
            "classes": unit_classes.keys(),
            "weapons": equipment.get_weapons_names(),
            "armors": equipment.get_armors_names()
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        req_form = request.form
        name = req_form.get('name')
        unit_class = unit_classes[req_form.get('unit_class')]

        enemy = EnemyUnit(name=name, unit_class=unit_class)
        enemy.equip_armor(equipment.get_armor(req_form.get('armor')))
        enemy.equip_weapon(equipment.get_weapon(req_form.get('weapon')))

        heroes['enemy'] = enemy

        return redirect("/fight/", code=302)


if __name__ == "__main__":
    app.run()
